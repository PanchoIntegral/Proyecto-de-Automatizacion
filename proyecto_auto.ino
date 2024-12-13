#include <AccelStepper.h>
#include <MultiStepper.h>

// 60 steps = 1cm
AccelStepper stepper1(1, 6, 5); // Motor de extrusión (STEP, DIR)
AccelStepper stepper2(1, 4, 3); // Motor de corte (STEP, DIR)

const int EN1 = 9; // Enable pin para motor 1
const int EN2 = 8; // Enable pin para motor 2

String inputString = "";      // String para almacenar los datos entrantes
boolean stringComplete = false;  // Indica si el string está completo

void setup() {
  Serial.begin(9600);
  inputString.reserve(200);
  
  // Configuración de pines y motores
  pinMode(EN1, OUTPUT);
  pinMode(EN2, OUTPUT);
  
  // Deshabilitar drivers inicialmente
  digitalWrite(EN1, HIGH);
  digitalWrite(EN2, HIGH);
  
  // Configuración de motores
  stepper1.setMaxSpeed(1000);
  stepper1.setAcceleration(800);
  stepper1.setCurrentPosition(0);
  
  stepper2.setMaxSpeed(1000);
  stepper2.setAcceleration(800);
  stepper2.setCurrentPosition(0);
}

void loop() {
  if (stringComplete) {
    procesarComando(inputString);
    inputString = "";
    stringComplete = false;
  }
  
  // Leer datos seriales
  while (Serial.available()) {
    char inChar = (char)Serial.read();
    inputString += inChar;
    if (inChar == '\n') {
      stringComplete = true;
    }
  }
}

void procesarComando(String comando) {
  // Remover espacios en blanco y saltos de línea
  comando.trim();
  
  if (comando.startsWith("CORTAR:")) {
    // Extraer longitud y cantidad de cortes
    int separador = comando.indexOf(',');
    float longitud = comando.substring(7, separador).toFloat();
    int cantidad = comando.substring(separador + 1).toInt();
    
    // Realizar el proceso de corte múltiple
    cortarCables(longitud, cantidad);
    
    // Enviar confirmación
    Serial.println("OK");
  }
  else if (comando == "DETENER") {
    // Detener ambos motores
    stepper1.stop();
    stepper2.stop();
    digitalWrite(EN1, HIGH);
    digitalWrite(EN2, HIGH);
    Serial.println("OK");
  }
}

void extruir(float cm) {
  digitalWrite(EN1, LOW);  // Habilitar driver
  stepper1.runToNewPosition(cm * 60);  // 60 pasos = 1cm
  stepper1.stop();
  digitalWrite(EN1, HIGH);
}

void cortar(int posicion) {
  digitalWrite(EN2, LOW);  // Habilitar driver
  stepper2.runToNewPosition(posicion);
  stepper2.stop();
  digitalWrite(EN2, HIGH);
}

void cortarCables(float longitud, int cantidad) {
  for (int i = 0; i < cantidad; i++) {
    extruir(longitud);
    delay(500);  // Esperar a que termine la extrusión
    cortar(50);  // Realizar el corte
    delay(500);  // Esperar a que termine el corte
    cortar(0);   // Regresar cortador a posición inicial
  }
}
