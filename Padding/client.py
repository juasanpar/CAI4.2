#encoding: utf-8
import socket
import hmac
from hashlib import sha256
from random import _urandom
from functions import autenticaCifra, autenticaLuegoCifra, cifraAutentica
from Crypto.PublicKey import RSA
from PaddingOracle import decrypt, INIT_VEC
from base64 import b64decode

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
            
    sock.send(tipoMensaje)
    
    print('El tipo de mensaje a recibir es el '+tipoMensaje+"\n")
    
    claveAES = sock.recv(10000)
    
    print "Recibida claveAES"
    
    mensajeServidor = sock.recv(10000)
    
    print "Recibido mensaje del servidor: "+mensajeServidor
    
    if (tipoMensaje == "1"):
        print "El método de cifrado+hash es Autentica y Cifra"
        
        descifrado = decrypt(b64decode(mensajeServidor.split("----")[0]), b64decode(claveAES), INIT_VEC)
        
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
        
        descifradoMensaje = decrypt(b64decode(mensajeServidor.split("----")[0]), b64decode(claveAES), INIT_VEC)
        descifradoHash = decrypt(b64decode(mensajeServidor.split("----")[1]), b64decode(claveAES), INIT_VEC)
        
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
        
        descifrado = decrypt(b64decode(mensajeServidor.split("----")[0]), b64decode(claveAES), INIT_VEC)
        
        print "El mensaje descifrado es: "+descifrado
        
        hmacCifrado = hmac.new("HmacKey", b64decode(mensajeServidor.split("----")[0]), sha256).hexdigest()
        
        if (hmacCifrado != mensajeServidor.split("----")[1]):
            print "El Mac del mensaje recibido es: "+mensajeServidor.split("----")[1]
            print "El Mac del mensaje recibido es: "+hmacCifrado
            print "El mensaje recibido por el servidor no es integro \n"
            
        else:
            print "Mensaje recibido correctamente \n"
            
    print "----------------ENVIAR NUEVO MENSAJE-------------------"

sock.close()

