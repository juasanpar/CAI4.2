#encoding: utf-8
import hmac
from hashlib import sha256
from random import _urandom
from Crypto import Random
from Crypto.PublicKey import RSA
from base64 import b64encode, b64decode

def generarClaveRSA (bits):
    RSAKey = RSA.generate(bits).exportKey()

    return RSAKey

def autenticaCifra (mensaje, clave):
    keyHMac = "HmacKey"

    hash = hmac.new(keyHMac, mensaje, sha256).hexdigest()
    cifrado = RSA_2048_CBC(mensaje, clave)
    
    return b64encode(cifrado)+"----"+hash

def autenticaLuegoCifra (mensaje, clave):
    keyHMac = "HmacKey"
    
    hash = hmac.new(keyHMac, mensaje, sha256).hexdigest()
    cifrado = RSA_2048_CBC(mensaje, clave)
    cifradoHash = RSA_2048_CBC(hash, clave)
    
    return b64encode(cifrado)+"----"+b64encode(cifradoHash)

def cifraAutentica (mensaje, clave):
    keyHMac = "HmacKey"

    cifrado = RSA_2048_CBC(mensaje, clave)
    hash = hmac.new(keyHMac, b64encode(cifrado), sha256).hexdigest()
    
    return b64encode(cifrado)+"----"+hash

def RSA_2048_CBC(datos, clave):
    key = clave
    binPrivKey = key.exportKey('DER')
    binPubKey =  key.publickey().exportKey('DER')
    privKeyObj = RSA.importKey(binPrivKey)
    pubKeyObj =  RSA.importKey(binPubKey)
    emsg = pubKeyObj.encrypt(datos, 'x')[0]
    dmsg = privKeyObj.decrypt(emsg)
    
    return emsg

def decrypt_RSA (message, clave):
    mensaje = b64decode(message)
    key = clave
    binPrivKey = key.exportKey('DER')
    privKeyObj = RSA.importKey(binPrivKey)
    dmsg = privKeyObj.decrypt(mensaje)
    
    return dmsg

