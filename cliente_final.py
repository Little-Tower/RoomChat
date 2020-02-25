import queue
import threading
import tkinter as tk
from tkinter import ttk
# El ciente debe realiar una serie de acciones:
# 1 -Indicar al servidor cual es su nombre.
# 2 -Entrar en un loop para ir comunicando sus mensajes con el servidor.
import socket
import select
# Para registrar los errores de forma especififca.
import errno
import sys

# Variable del mensaje para enviar
messageToSend = ""
messageToRecieve = ""

# Clase para la ejecución del hilo del cliente.
class mecanimos_cliente(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        LONG_CABECERA = 10
        IP = "127.0.0.1"
        PORT = 5005
        # Para poder escribir nuestro nombre.
        nombre = input("Escriba su nombre de usuario en el chat: ")
        # Objeto de socket para el cliente
        cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cliente_socket.connect((IP, PORT))
        # para controlar el bloque de la recepcion. Esta "no bloqueada".
        cliente_socket.setblocking(False)

        nombre_usuario = nombre.encode("utf-8")
        cabecera_nombre = f"{len(nombre_usuario):<{LONG_CABECERA}}".encode("utf-8")
        cliente_socket.send(cabecera_nombre + nombre_usuario)
        print("Arrancando el cliente...")
        while True:
            mensaje = messageToSend.get()

            # Controlamos que el mensaje no este vacio.
            if mensaje:
                mensaje = mensaje.encode("utf-8")
                cabecera_mensaje = f"{len(mensaje):<{LONG_CABECERA}}".encode("utf-8")
                cliente_socket.send(cabecera_mensaje + mensaje)
                messageToSend = cabecera_mensaje + mensaje
                print(messageToSend)
                messageToSend.empty()

            # Receptor de mensaje.
            try:
                while True:
                    cabecera_nombre = cliente_socket.recv(LONG_CABECERA)
                    # en caso de que no tenga la longitud exacta, salta este condicional.
                    if not len(cabecera_nombre):
                        print("Conecion cerrada por el servidor")
                        sys.exit()

                    longitud_nombre = int(longitud_nombre.encode("utf-8").strip)
                    nombre_cliente = cliente_socket.recv(longitud_nombre).encode("utf-8")

                    cabecera_nombre = cliente_socket.recv(LONG_CABECERA).encode("utf-8")
                    longitud_mensaje = int(cabecera_nombre.encode("utf-8".strip()))
                    mensaje = cliente_socket.recv(longitud_mensaje).encode("utf-8")

                    print(f"{nombre_cliente} > {mensaje}")
                    messageToSend = (f"{nombre_cliente} > {mensaje}")
            except IOError as ioe:
                # Errores que suelen saltar cuando no hay más mensaje por recibir.
                # Depenede de los sistemas operativos.
                if ioe.errno != errno.EAGAIN and ioe.errno != errno.EWOULDBLOCK:
                    print("Error por no lectura", str(ioe))
                    sys.exit()
                continue

            except Exception as e:
                print("Error de recepcion", str(e))
                sys.exit()


# Clase para la ejecucion de la interfaz
class gui(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)



    def run(self):
        # Funcion para crear el contenido dentro de la pestanna chat.
        class Chat(ttk.Frame):

            # Funcion que limpia el input cuando envia el mensaje
            def sendMessageClick(self, event, entrada_mensaje):
                messageToRecieve = entrada_mensaje
                entrada_mensaje.delete(0, "end")

            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)

                self.lb_mensajes = ttk.Label(self)
                self.lb_mensajes.configure(text="Mensajes del chat.", font=("Arial Bold", 16))
                self.lb_mensajes.pack(side='top')

                self.ver_mensajes = tk.Text(self, width=40, height=15)
                self.ver_mensajes.config(fg="green")
                self.ver_mensajes.pack(fill="x")

                self.entrada_mensaje = ttk.Entry(self)
                self.entrada_mensaje.pack(fill="x")

                self.btn_enviar = ttk.Button(self, text="Enviar")
                self.btn_enviar.pack(fill="x")
                self.btn_enviar.bind("<Button-1>", lambda event: self.sendMessageClick(event, self.entrada_mensaje))

                if messageToRecieve:
                    self.ver_mensajes.insert("1.0",messageToRecieve)

        # Funcion para crear el contenido dentro de la pestanna chat.
        class Clientes(ttk.Frame):

            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)

                self.lb_clientes = ttk.Label(self)
                self.lb_clientes.configure(text="Usuarios conectados.", font=("Arial Bold", 16))
                self.lb_clientes.pack(side='top')

                self.ver_clientes = tk.Text(self, width=40, height=20)
                self.ver_clientes.config(bg="white")
                self.ver_clientes.pack(fill="x")

        # Funcion para crear el contenido dentro de la pestanna chat.
        class Ajustes(ttk.Frame):

            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)

                self.lb_clientes = ttk.Label(self)
                self.lb_clientes.configure(text="Introduza su nombre")
                self.lb_clientes.pack(side='top')

                self.set_nombre = ttk.Entry(self)
                self.set_nombre.pack()

                self.btn_nombre = ttk.Button(
                    self, text="Conectar")
                self.btn_nombre.pack()

                self.btn_desconectar = ttk.Button(
                    self, text="Desconectar")
                self.btn_desconectar.pack()

        class Application(ttk.Frame):

            def __init__(self, main_window):
                super().__init__(main_window)
                main_window.title("Python Chat.")
                main_window.geometry('800x500')
                main_window.config(bg="white")
                main_window.resizable(0, 0)

                # Crear el panel de pestañas.
                self.notebook = ttk.Notebook(self)
                self.notebook.config(width="800", height="500")

                # CONTENIDO DE LAS PESTANNAS.
                # MENSAJES.
                self.chat = Chat(self.notebook)
                self.notebook.add(
                    self.chat, text="Chat", padding=5)

                # CLIENTES.
                self.clientes = Clientes(self.notebook)
                self.notebook.add(
                    self.clientes, text="Clientes", padding=5)

                # CONECTAR.
                self.ajustes = Ajustes(self.notebook)
                self.notebook.add(
                    self.ajustes, text="Conectar", padding=5)

                # Añadirlas al panel con su respectivo texto.
                self.notebook.enable_traversal()
                self.notebook.add(self.chat, text="Chat", padding=40)
                self.notebook.add(self.clientes, text="clientes", padding=40)
                self.notebook.add(self.ajustes, text="Ajustes", padding=40)

                self.notebook.pack(padx=10, pady=10)
                self.pack()

        main_window = tk.Tk()
        app = Application(main_window)
        app.mainloop()



# HILO GRAFICO
# Se crean los hilo desde cada una de las clases.
hilo_gráfico = gui()
# Se inicializa el hilo
hilo_gráfico.start()

# HILO MECANISMOS CLIENTE
hilo_cliente = mecanimos_cliente()
# Este hilo se ejecuta como demonio.
hilo_cliente.daemon = True
hilo_cliente.start()
