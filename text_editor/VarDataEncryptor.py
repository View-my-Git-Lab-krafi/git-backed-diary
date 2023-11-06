import sys
import hashlib
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2

import getpass
import bcrypt
from passlib.hash import pbkdf2_sha512
import secrets
import getpass

def derive_key(password, salt, key_length):
    return PBKDF2(password, salt, dkLen=key_length, count=100000)


def pad(data, block_size):
    padding = block_size - len(data) % block_size
    return data + bytes([padding] * padding)


def unpad(data):
    padding = data[-1]
    return data[:-padding]

def encrypt_data(data, password):
    salt = get_random_bytes(16)
    key = derive_key(password, salt, 32)
    password = None 
    iv = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = data.encode()
    padded_plaintext = pad(plaintext, 16)
    encrypted_data = cipher.encrypt(padded_plaintext)
    enc_binary_data = b'ENCRYPTED:' + salt + iv + encrypted_data
    encrypted_hex = enc_binary_data.hex()
    return encrypted_hex

def decrypt_data(encrypted_data, password):
    encrypted_binary_data = bytes.fromhex(encrypted_data)
    if not encrypted_binary_data.startswith(b'ENCRYPTED:'):
        raise ValueError("The data is not encrypted with this program.")
    encrypted_binary_data = encrypted_binary_data[len(b'ENCRYPTED:'):]
    salt = encrypted_binary_data[:16]
    iv = encrypted_binary_data[16:32]
    ciphertext = encrypted_binary_data[32:]
    key = derive_key(password, salt, 32)
    #password = None #secure mode maybe i will add this feature in future.
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_data = unpad(cipher.decrypt(ciphertext))
    return decrypted_data.decode()


def start_var_data_encryptor(worktype, data, passwd):
    if worktype == "enc":
        enc = encrypt_data(data, passwd)
        #print(enc)
        return enc
    else:
        dec = decrypt_data(data, passwd)
        #print(dec)
        return dec


