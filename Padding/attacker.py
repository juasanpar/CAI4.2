#encoding: utf-8
import socket
from time import sleep
import sys
from random import _urandom
from functions import autenticaCifra, autenticaLuegoCifra, cifraAutentica
from Crypto.PublicKey import RSA
from PaddingOracle import paddingAttack
from base64 import b64decode

# Se crea el socket para que se conecte el cliente
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
atacker_address = ('localhost', 10001)
sock.bind(atacker_address)

#Se crea el socket para conectarse al servidor
sock2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 10000)
sock2.connect(server_address)


# Se espera a que el cliente se conecte
sock.listen(1)
print "----------Esperando conexion del cliente-----------"

# connection es un nuevo socket para mandar y recibir. address es la direccion del otro socket en la conexion
connection, address = sock.accept()

while True: 
    handShake = connection.recv(10000)
    tipoMensaje = handShake.split(",")[0]
    
    print "Cliente conectado y credenciales recibidas "+handShake
    
    nuevosBits = raw_input("Confirma que se está produciendo el ataque (Y/N): ")
    
    newHandShake = tipoMensaje
    
    sock2.send(newHandShake)
    
    print('Se ha enviado el tipo de mensaje '+newHandShake+"\n")
    
    claveAES = sock2.recv(10000)
        
    print "Recibida clave AES"
    
    mensajeServidor = sock2.recv(10000)
        
    print "Recibido mensaje del servidor: "+mensajeServidor   
    
    connection.send(claveAES)
    connection.send(mensajeServidor)
    
    print "La clave es "+b64decode(claveAES)
    print "El mensaje cifrado es "+ b64decode(mensajeServidor.split("----")[0])
    
    mensajeClaro = paddingAttack(b64decode(mensajeServidor.split("----")[0]), b64decode(claveAES))
    
    print mensajeClaro
    
    print "---------------ESPERANDO INTERCEPTAR NUEVO MENSAJE-----------------"

connection.close()
