#encoding: utf-8
import socket
import hmac
from hashlib import sha256
from random import _urandom
from functions import autenticaCifra, autenticaLuegoCifra, cifraAutentica, decrypt_RSA
from Crypto.PublicKey import RSA

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#sock2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 10000)
atacker_addess = ('localhost', 10001)
sock.connect(atacker_addess)
#sock2.connect(atacker_addess)

print('-----------------Estableciendo conexion como cliente-----------------')

# Manda el mensaje al servidor #
tipoMensaje = ""
bitsRSA = ""

while True:     
    tipoMensaje = raw_input("Introduce como quieres enviar el mensaje (1, 2, 3): ")
    bitsRSA = raw_input("Introduce el tamano de clave que quieres emplear en el cifrado(1024, 1280, 1536, 1792, 2048): ")
            
    sock.send(tipoMensaje+","+bitsRSA)
    
    print('El tipo de mensaje a recibir es el '+tipoMensaje+" y el número de bits de la clave RSA esperado es "+bitsRSA+"\n")
    
    claveRSA = sock.recv(10000)
    
    print "Recibida clave RSA"
    
    mensajeServidor = sock.recv(10000)
    
    print "Recibido mensaje del servidor: "+mensajeServidor
    
    if (tipoMensaje == "1"):
        print "El método de cifrado+hash es Autentica y Cifra"
        
        descifrado = decrypt_RSA(mensajeServidor.split("----")[0], RSA.importKey(claveRSA))
        
        print "El mensaje descifrado es: "+descifrado
        
        hmacDescifrado = hmac.new("HmacKey", descifrado, sha256).hexdigest()
        
        if (hmacDescifrado != mensajeServidor.split("----")[1]):
            print "El Mac del mensaje recibido es: "+mensajeServidor.split("----")[1]
            print "El Mac del mensaje recibido es: "+hmacDescifrado
            print "El mensaje recibido por el servidor no es integro \n"
            
        else:
            print "Mensaje recibido correctamente \n"
    
    elif (tipoMensaje == "2"):
        print "El método de cifrado+hash es Autentica y Luego Cifra"
        
        descifradoMensaje = decrypt_RSA(mensajeServidor.split("----")[0], RSA.importKey(claveRSA))
        descifradoHash = decrypt_RSA(mensajeServidor.split("----")[1], RSA.importKey(claveRSA))
        
        print "El mensaje descifrado es: "+descifradoMensaje
        print "El hash descifrado es: "+descifradoHash
        
        hmacDescifrado = hmac.new("HmacKey", descifradoMensaje, sha256).hexdigest()
        
        if (hmacDescifrado != descifradoHash):
            print "El Mac del mensaje recibido es: "+mensajeServidor.split(",")[1]
            print "El Mac del mensaje recibido es: "+hmacDescifrado
            print "El mensaje recibido por el servidor no es integro \n"
            
        else:
            print "Mensaje recibido correctamente \n"
    
    elif (tipoMensaje == "3"):
        print "El método de cifrado+hash es Cifra y Autentica"
        
        descifrado = decrypt_RSA(mensajeServidor.split("----")[0], RSA.importKey(claveRSA))
        
        print "El mensaje descifrado es: "+descifrado
        
        hmacCifrado = hmac.new("HmacKey", mensajeServidor.split("----")[0], sha256).hexdigest()
        
        if (hmacCifrado != mensajeServidor.split("----")[1]):
            print "El Mac del mensaje recibido es: "+mensajeServidor.split("----")[1]
            print "El Mac del mensaje recibido es: "+hmacCifrado
            print "El mensaje recibido por el servidor no es integro \n"
            
        else:
            print "Mensaje recibido correctamente \n"
            
    print "----------------ENVIAR NUEVO MENSAJE-------------------"

sock.close()

