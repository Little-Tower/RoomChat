import socket
# Una libreria que ayudad a usar el programa en distintas plataformas.
# Garantiza que funcione igual en todos los sistemas operativos.
import select

LONG_CABECERA = 10
IP = "127.0.0.1"
PORT = 5005
# Creación del objeto socket.
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Permite no bloquear el programa por fallo y reconectar.
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# Pasamos los parametros de ip y puerto al objeto.
server_socket.bind((IP, PORT))
# EL objeto socket pasa a estar en escucha.
server_socket.listen()

# MECANISMO DE LISTA DE CLIENTES.
lista_sockets = [server_socket]
lista_clientes = {}


# Funcion para que el servidor reciba mensajes.
def recibir_mensaje(cliente_socket):
    try:
        # Primero recibe un mensaje de cabecera del cliente.
        mensaje_cabecera = cliente_socket.recv(LONG_CABECERA)

        # Comprueba: sino recibe ninguna informacion el servidor cierra la conexion
        if not len(mensaje_cabecera):
            return False

        # Casting para obtener la longitud del mensaje.
        # Previamente lo ha transformado para que le programa lo pueda leer.
        longitud_mensaje = int(mensaje_cabecera.decode("uft-8").strip())
        return {"Cabecera": mensaje_cabecera, "Contenido": cliente_socket.recv(longitud_mensaje)}

    except:
        return False

#BUBLE DE FUNCIONAMIENTO.
print("Arrancando el servidor...")
while True:
    #Esta expresion primero lee el socket, lo escribe (en el array vacio []) y controla los errores.
    leer_socket, _, excepciones_socket = select.select(lista_sockets, [], lista_clientes)

    for notificacion in leer_socket:
        #Aqui acepta cualquier conexion entrante.
        if notificacion == server_socket:
            cliente_socket, cliente_direcc = server_socket.accept()
            #LLamanos a la funcion para recibir el mensaje y le pasamos como parametro la conexion entrante.
            usuario = recibir_mensaje(cliente_socket)
            #Si el usuario se desconecta.
            if usuario is False:
                continue
            #Annade a la lista el cliente para guardarlo.
            lista_sockets.append(cliente_socket)
            lista_clientes[cliente_socket] = usuario

            print(f"Nueva conexion establecida con {cliente_direcc[0]}:{cliente_direcc[1]} --- {usuario['data'].decode('utf-8')}")
        else:
            mensaje = recibir_mensaje(notificacion)
            #En caso de recibir un mensaje vacio
            if mensaje is False:
                print(f"Conexion cerrada con {lista_clientes[notificacion]['data'].decode('utf-8')}")
                lista_sockets.remove(notificacion)
                del lista_sockets[notificacion]
                continue

            #Ejemplo de como funciona la sintaxis de print(f).
            usuario = lista_sockets[notificacion]
            nombre_usuario = usuario['data'].decode('utf-8')
            contenido_mensaje = mensaje[['data'].decode('utf-8')]
            print(f"Mensaje recibido de {nombre_usuario}: {contenido_mensaje}")

            #For para enviar el mensaje a todos los clientes.
            for cliente_socket in lista_clientes:
                #Para no enviar el mensaje al mismo cliente que lo envia.
                if cliente_socket != notificacion:
                    #Finalmente envia la informacion. Header es para saber la informacion de origen y data para el contenido.
                    cliente_socket.send(usuario['header'] + usuario['data'] + mensaje['header'] + mensaje['data'])

    #Controla las excepciones y elimina el cliente que la ha provocado de la lista.
    for notificacion in excepciones_socket:
        lista_sockets.remove(notificacion)
        del lista_sockets[notificacion]