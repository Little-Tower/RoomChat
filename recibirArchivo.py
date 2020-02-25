#codigo para la recepcion del archivo. Servidor
import socket

conexion = (socket.gethostname(), 9001)
servidor = socket.socket()
print("[*].- Esperando conexion...")

servidor.bind(conexion)
servidor.listen(5)

conn, addr = servidor.accept()
print("[*].- Conexion establecida con: ")
print(addr)

#Contador para controlar la salida.
contBuffer = 0

#seccion para la edicion de los buffers
SEND_BUF_SIZE = 40960
RECV_BUF_SIZE = 40960

def modify_buff_size():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #Tamanno del buffer de envio previo
    bufsize = sock.getsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF)
    print ("Tamanno del buffer [previo]: %d" %bufsize)

    sock.setsockopt(socket.SOL_TCP, socket.TCP_NODELAY, 1)

    sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, SEND_BUF_SIZE)

    sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, RECV_BUF_SIZE)

    bufsize = sock.getsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF)
    print ("Tamanno del buffer [modificado]: %d" %bufsize)

    #getsockopt() y setsockopt() son metodos de un objeto socket para reatribuir y modificar las propiedades de dicho objeto.
    #setsockopt() toma tres argumentos: level, optname, value. optname toma el nombre de la opcion a modificar
    #y lo cambia por el valor de value.

modify_buff_size()

while True:
    tamanoFile = conn.recv(1024).strip()

    #Verificamos: que sea un numero y que sea menos que el buffer
    if tamanoFile.isdigit():
        print("[*].- El tamanno del archivo es: ")
        print(tamanoFile)
        conn.send("OK")
        print("[*].- Solicitud de archivo aceptada.")


    #Apertura del archivo en modo de escritura binaria. WriteBinary o wb.
    with open("goes.jpg", "wb") as archivo:
        #Condicionamos la recepcion a la longuitud del buffer
        print("[*].- Comienza la transmision del archivo.")

        while (buffer >= tamanoFile):
            #recepcion de cada byte del archivo en data
            data = conn.recv(1)
            print(contBuffer)

            archivo.write(data)

            #Si el programa no recibe datos se sale
            if contBuffer == tamanoFile:
                print("[*].- Fin  de la transmision.")
                exit()
            #Aumenta el contador del buffer (lonitud del archivo)
            contBuffer += 1

    if contBuffer == tamanoFile:
        print("Archivo descargado con exito.")
    else:
        print("Ha ocurrido un error en la transmision de los datos.")
    exit()
