#encoding: utf-8
import hmac
from hashlib import sha256
from random import _urandom
from Crypto import Random
from Crypto.PublicKey import RSA
from PaddingOracle import encrypt, INIT_VEC, numberify
from base64 import b64encode, b64decode

def autenticaCifra (mensaje, clave):
    keyHMac = "HmacKey"

    hash = hmac.new(keyHMac, mensaje, sha256).hexdigest()
    cifrado = AES_CBC(mensaje, clave)
    
    return b64encode(cifrado)+"----"+hash

def autenticaLuegoCifra (mensaje, clave):
    keyHMac = "HmacKey"
    
    hash = hmac.new(keyHMac, mensaje, sha256).hexdigest()
    cifrado = AES_CBC(mensaje, clave)
    cifradoHash = AES_CBC(hash, clave)
    
    return b64encode(cifrado)+"----"+b64encode(cifradoHash)

def cifraAutentica (mensaje, clave):
    keyHMac = "HmacKey"

    cifrado = AES_CBC(mensaje, clave)
    hash = hmac.new(keyHMac, b64encode(cifrado), sha256).hexdigest()
    
    return b64encode(cifrado)+"----"+hash

def AES_CBC(datos, clave):
    return encrypt(datos, clave, INIT_VEC)

