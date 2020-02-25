#El ciente debe realiar una serie de acciones:
#1 -Indicar al servidor cual es su nombre.
#2 -Entrar en un loop para ir comunicando sus mensajes con el servidor.
import socket
import select
#Para registrar los errores de forma especififca.
import errno
import sys

LONG_CABECERA = 10
IP = "127.0.0.1"
PORT = 5005
#Para poder escribir nuestro nombre.
nombre = input("Escriba su nombre de usuario en el chat: ")
#Objeto de socket para el cliente
cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente_socket.connect((IP, PORT))
#para controlar el bloque de la recepcion. Esta "no bloqueada".
cliente_socket.setblocking(False)

nombre_usuario = nombre.encode("utf-8")
cabecera_nombre = f"{len(nombre_usuario):<{LONG_CABECERA}}".encode("utf-8")
cliente_socket.send(cabecera_nombre + nombre_usuario)
print("Arrancando el cliente...")
while True:
    mensaje = input(f"{nombre} > ")

    #Controlamos que el mensaje no este vacio.
    if mensaje:
        mensaje = mensaje.encode("utf-8")
        cabecera_mensaje = f"{len(mensaje):<{LONG_CABECERA}}".encode("utf-8")
        cliente_socket.send(cabecera_nombre + mensaje)

    #Receptor de mensaje.
    try:
        while True:
            cabecera_nombre = cliente_socket.recv(LONG_CABECERA)
            #en caso de que no tenga la longitud exacta, salta este condicional.
            if not len(cabecera_nombre):
                print("Conecion cerrada por el servidor")
                sys.exit()

            longitud_nombre = int(longitud_nombre.encode("utf-8").strip)
            nombre_cliente = cliente_socket.recv(longitud_nombre).encode("utf-8")

            cabecera_nombre = cliente_socket.recv(LONG_CABECERA).encode("utf-8")
            longitud_mensaje = int(cabecera_nombre.encode("utf-8".strip()))
            mensaje = cliente_socket.recv(longitud_nombre).encode("utf-8")

            print(f"{nombre_cliente} > {mensaje}")
    except IOError as ioe:
        #Errores que suelen saltar cuando no hay más mensaje por recibir.
        #Depenede de los sistemas operativos.
        if ioe.errno != errno.EAGAIN and ioe.errno != errno.EWOULDBLOCK:
            print("Error por no lectura",str(ioe))
            sys.exit()
        continue

    except Exception as e:
        print("Error de recepcion",str(e))
        sys.exit()