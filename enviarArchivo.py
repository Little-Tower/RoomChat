#Codigo para enviar archivos usan sockets. Cliente
#Proceso:
#Cliente: Envia longitud del archivo.
#Servidor: Comprueba la longitud (numero), y lo compara con el buffer
#Servidor: Si al longitud es correcta, envia un mensaje permitiendo al cliente el archivo
#Cliente: Comprueba que el servidor este listo
#Cliente: Enviar archivo al servidor

import socket

conexion = (socket.gethostname(), 9001)
archivoUno = "go.jpg"

cliente = socket.socket()
cliente.connect(conexion)
contador = 0

#Primero abrimos y leemos el archivo en modo de lectura binaria. ReadBinary o rb
with open(archivoUno, "rb") as archivoDos:
    buffer = archivoDos.read()

while True:
    #Enviamos al servidor la cantidad de bytes.
    cliente.send(str(len(buffer)))
    print("[*].- Enviando cantidad buffer al servidor")
    print(len(buffer))

    #El programa queda a la espera de respuesta
    recibido = cliente.recv(20)

    print(recibido)

    #Si la respuesta es correcta, empieza a enviar el archivo byte a byte
    if recibido == "OK":

        for byte in buffer:
            cliente.send(byte)

        if contador >= buffer:
            exit()

            contador += 1
    else:
        print("No se puede enviar el archivo.")
        exit()
