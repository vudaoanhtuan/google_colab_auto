import base64
import hashlib
from Crypto import Random
from Crypto.Cipher import AES

def pad(s, bs=32):
    return s + bytes([bs - len(s) % bs] * (bs - len(s) % bs))

def unpad(s):
    return s[0:-s[-1]]

def encrypt(raw, key):
    bs = 32
    key = hashlib.sha256(key.encode()).digest()
    raw = pad(raw)
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return base64.b64encode(iv + cipher.encrypt(raw))

def decrypt(enc, key):
    bs = 32
    key = hashlib.sha256(key.encode()).digest()
    enc = base64.b64decode(enc)
    iv = enc[:AES.block_size]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(enc[AES.block_size:]))