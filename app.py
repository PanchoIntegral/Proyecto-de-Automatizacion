import tkinter as tk
from tkinter import messagebox, ttk
import serial
import time
import serial.tools.list_ports

class CortadoraCableGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Control - Cortadora de Cable")
        self.root.geometry("600x500")
        self.root.configure(bg='#333333')
        
        # Inicializar arduino como None
        self.arduino = None
        
        # Crear elementos de la interfaz
        self.create_widgets()
        
        # Intentar conectar con Arduino
        self.conectar_arduino()

    def conectar_arduino(self):
    
        
        try:
            # Buscar puertos disponibles
            puertos = list(serial.tools.list_ports.comports())
            for puerto in puertos:
                # Buscar puerto que contenga "Arduino" o intentar cada puerto disponible
                if "Arduino" in puerto.description:
                    try:
                        self.arduino = serial.Serial(puerto.device, 9600, timeout=1)
                        time.sleep(2)  # Esperar a que se establezca la conexión
                        self.actualizar_estado("SISTEMA CONECTADO", '#b3b3b3')
                        self.btn_conectar.config(state="disabled")
                        self.btn_cortar.config(state="normal")
                        self.btn_detener.config(state="normal")
                        self.btn_reiniciar.config(state="normal")
                        print(f"Conexión exitosa en puerto {puerto.device}")
                        return True
                    except serial.SerialException as e:
                        continue
                        
            # Si no se encontró ningún puerto con Arduino, intentar con el primer puerto disponible
            if puertos:
                try:
                    self.arduino = serial.Serial(puertos[0].device, 9600, timeout=1)
                    time.sleep(2)
                    self.actualizar_estado("SISTEMA CONECTADO", '#b3b3b3')
                    self.btn_conectar.config(state="disabled")
                    self.btn_cortar.config(state="normal")
                    self.btn_detener.config(state="normal")
                    self.btn_reiniciar.config(state="normal")
                    print(f"Conexión exitosa en puerto {puertos[0].device}")
                    return True
                except serial.SerialException as e:
                    self.actualizar_estado(f"ERROR DE CONEXIÓN: {str(e)}", '#ff6666')
                    return False
                    
            self.actualizar_estado("NO SE ENCONTRÓ NINGÚN PUERTO DISPONIBLE", '#ff6666')
            return False
            
        except Exception as e:
            self.actualizar_estado(f"ERROR DE SISTEMA: {str(e)}", '#ff6666')
            self.btn_conectar.config(state="normal")
            self.btn_cortar.config(state="disabled")
            self.btn_detener.config(state="disabled")
            self.btn_reiniciar.config(state="disabled")
            print(f"Error al conectar: {str(e)}")
            return False

    def create_widgets(self):
        # Título centrado
        title_label = tk.Label(self.root, text="CONTROL DE CORTADORA",
                               font=('Roboto', 32, 'bold'), fg='#f2f2f2', bg='#333333')
        title_label.pack(pady=20)

        # Estado del sistema
        self.status_label = tk.Label(self.root, text="ESTADO: INICIANDO",
                                     font=('Roboto', 12), fg='#b3b3b3', bg='#333333')
        self.status_label.pack(pady=10)

        # Entrada de longitud de corte
        length_label = tk.Label(self.root, text="LONGITUD DE CORTE (cm)",
                                font=('Roboto', 14), fg='#b3b3b3', bg='#333333')
        length_label.pack(pady=(20, 5))
        
        self.length_entry = tk.Entry(self.root, width=15, font=('Roboto', 14),
                                     justify='center', bg='#404040', fg='white')
        self.length_entry.pack()

        # Entrada de cantidad de cables
        quantity_label = tk.Label(self.root, text="CANTIDAD DE CABLES",
                                  font=('Roboto', 14), fg='#b3b3b3', bg='#333333')
        quantity_label.pack(pady=(20, 5))
        
        self.quantity_entry = tk.Entry(self.root, width=15, font=('Roboto', 14),
                                       justify='center', bg='#404040', fg='white')
        self.quantity_entry.pack()

        # Barra de progreso
        self.progress = ttk.Progressbar(self.root, orient="horizontal", length=400, mode="determinate")
        self.progress.pack(pady=(20, 10))
        
        # Botones
        button_frame = tk.Frame(self.root, bg='#333333')
        button_frame.pack(pady=20)

        # Botón de conectar
        self.btn_conectar = tk.Button(button_frame, text="CONECTAR", 
                                      command=self.conectar_arduino,
                                      font=('Roboto', 14, 'bold'), bg='#4CAF50', fg='white',
                                      activebackground='#66BB6A', activeforeground='white',
                                      width=14)
        self.btn_conectar.grid(row=0, column=0, padx=5)

        # Botón de iniciar corte
        self.btn_cortar = tk.Button(button_frame, text="INICIAR", 
                                    command=self.cortar_cable,
                                    font=('Roboto', 14, 'bold'), bg='#2196F3', fg='white',
                                    activebackground='#64B5F6', activeforeground='white',
                                    width=14, state="disabled")
        self.btn_cortar.grid(row=0, column=1, padx=5)

        # Botón de detener
        self.btn_detener = tk.Button(button_frame, text="DETENER", 
                                     command=self.detener,
                                     font=('Roboto', 14, 'bold'), bg='#F44336', fg='white',
                                     activebackground='#E57373', activeforeground='white',
                                     width=14, state="disabled")
        self.btn_detener.grid(row=0, column=2, padx=5)

        # Botón de reiniciar
        self.btn_reiniciar = tk.Button(button_frame, text="REINICIAR", 
                                       command=self.reiniciar,
                                       font=('Roboto', 14, 'bold'), bg='#FF9800', fg='white',
                                       activebackground='#FFB74D', activeforeground='white',
                                       width=14, state="disabled")
        self.btn_reiniciar.grid(row=1, column=1, pady=10)

        # Mensaje adicional
        self.info_label = tk.Label(self.root, text="LISTO PARA OPERACIÓN",
                                   font=('Roboto', 12), fg='#b3b3b3', bg='#333333')
        self.info_label.pack(pady=20)

    def actualizar_estado(self, mensaje, color='#f2f2f2'):
        self.status_label.config(text=f"ESTADO: {mensaje}", fg=color)
        
    def cortar_cable(self):
        if not self.arduino:
            messagebox.showerror("ERROR", "Sistema no conectado")
            return

        try:
            longitud = float(self.length_entry.get())
            cantidad = int(self.quantity_entry.get())
            
            if longitud <= 0 or cantidad <= 0:
                messagebox.showerror("ERROR", "La longitud y cantidad deben ser mayores a 0")
                return

            # Configuración de la barra de progreso
            self.progress["maximum"] = cantidad
            self.progress["value"] = 0  # Resetear al iniciar

            self.actualizar_estado("CORTANDO...", '#cccccc')
            self.info_label.config(text=f"PROCESANDO CORTE DE {cantidad} CABLES DE {longitud}cm")

            for i in range(cantidad):
                # Modificar el comando para incluir longitud y cantidad
                comando = f"CORTAR:{longitud},{cantidad}\n"
                self.arduino.write(comando.encode())

                respuesta = self.arduino.readline().decode().strip()
                if respuesta != "OK":
                    self.actualizar_estado("ERROR EN CORTE", '#ff6666')
                    self.info_label.config(text="ERROR EN PROCESO DE CORTE")
                    return

                # Actualizar barra de progreso
                self.progress["value"] = i + 1
                self.root.update_idletasks()  # Actualiza la interfaz

            self.actualizar_estado("CORTE COMPLETADO", '#b3b3b3')
            self.info_label.config(text=f"CORTE DE {cantidad} CABLES DE {longitud}cm COMPLETADO")

        except ValueError:
            messagebox.showerror("ERROR", "Ingrese un valor numérico válido")
        except Exception as e:
            self.actualizar_estado(f"ERROR DE COMUNICACIÓN: {e}", '#ff6666')


    def detener(self):
        if not self.arduino:
            messagebox.showerror("ERROR", "Sistema no conectado")
            return
            
        try:
            self.arduino.write("DETENER\n".encode())
            self.actualizar_estado("SISTEMA DETENIDO", '#cccccc')
            self.info_label.config(text="OPERACIÓN DETENIDA POR USUARIO")
            self.progress["value"] = 0  # Reiniciar barra de progreso al detener
        except:
            self.actualizar_estado("ERROR AL DETENER", '#ff6666')
            
    def reiniciar(self):
        if self.arduino:
            self.arduino.close()
            self.arduino = None
        self.length_entry.delete(0, tk.END)
        self.quantity_entry.delete(0, tk.END)
        self.actualizar_estado("SISTEMA REINICIADO", '#cccccc')
        self.info_label.config(text="LISTO PARA OPERACIÓN")
        self.progress["value"] = 0  # Reiniciar barra de progreso
        self.btn_conectar.config(state="normal")
        self.btn_cortar.config(state="disabled")
        self.btn_detener.config(state="disabled")
        self.btn_reiniciar.config(state="disabled")
        print("Sistema reiniciado")

    def __del__(self):
        if self.arduino:
            self.arduino.close()

# Iniciar la aplicación
if __name__ == "__main__":
    root = tk.Tk()
    root.configure(bg='#333333')
    app = CortadoraCableGUI(root)
    root.mainloop()
