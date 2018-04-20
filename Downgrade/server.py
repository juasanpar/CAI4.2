import socket
from time import sleep
import sys
from random import _urandom
from functions import autenticaCifra, autenticaLuegoCifra, cifraAutentica, generarClaveRSA
from Crypto.PublicKey import RSA

# Se crea objeto socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Se obtiene el nombre local de la maquina
server_address = ('localhost', 10000)
# Se reserva un puerto para el socket
sock.bind(server_address)

# Se espera a que el cliente se conecte
sock.listen(1)
print "----------Esperando conexion del cliente-----------"

# connection es un nuevo socket para mandar y recibir. address es la direccion del otro socket en la conexion
connection, address = sock.accept()

while True: 
    handShake = connection.recv(10000)
    tipoMensaje = int(handShake.split(",")[0])
    bitsRSA = int(handShake.split(",")[1])
    
    print "Cliente conectado y credenciales recibidas "+handShake
    
    claveRSA = generarClaveRSA(bitsRSA)
    connection.send(claveRSA)
        
    key = "HmacKey"
    mensaje = raw_input("Introduce un mensaje a enviar: ")
    enviar = ""
            
    if (tipoMensaje == 1):
        enviar = autenticaCifra(mensaje, RSA.importKey(claveRSA))
                    
    elif (tipoMensaje == 2):
        enviar = autenticaLuegoCifra(mensaje, RSA.importKey(claveRSA))
                    
    elif (tipoMensaje == 3): 
        enviar = cifraAutentica(mensaje, RSA.importKey(claveRSA))
                
    connection.send(enviar)
        
    print('Se ha enviado el mensaje '+enviar+"\n")
    
    print "-----------ESPERANDO NUEVO MENSAJE-----------------"
   
connection.close()
