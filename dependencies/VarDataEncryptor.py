import sys
import hashlib 

#Crypto 1.4.1
#from Crypto.Cipher import AES
#from Crypto.Random import get_random_bytes
#from Crypto.Protocol.KDF import PBKDF2

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


'''
#  Fernet symmetric encryption with a key derived from a password using PBKDF2HMAC with SHA512.
#  pip install cryptography

import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
import base64
import getpass
def generate_fernet_key():
    return Fernet.generate_key()

def generate_key_from_password(password, salt=None):
    if salt is None:
        salt = os.urandom(16)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA512(),
        iterations=900000,
        salt=salt,
        length=32
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    return key, salt

def initialize_fernet(key):
    return Fernet(key)

def encrypt_data(data, key):
    f = initialize_fernet(key)
    encrypted_data = f.encrypt(data.encode())
    encrypted_hex_string = ''.join(['{:02x}'.format(byte) for byte in encrypted_data]) 
    return encrypted_hex_string

def decrypt_data(encrypted_data, key):
    hex_to_bytes_encrypted = bytes.fromhex(encrypted_data)
    f = initialize_fernet(key)
    decrypted_data = f.decrypt(hex_to_bytes_encrypted)
    return decrypted_data.decode()

def start_var_data_encryptor(worktype, data, key):
    if worktype == "enc":
        enc = encrypt_data(data, key)
        return enc
    else:
        dec = decrypt_data(data, key)
        return dec

# Get the password securely from the user
password = getpass.getpass("Enter your password: ") 

key, salt = generate_key_from_password(password)
print("Generated key:", key)
print("Salt:", salt)
the_message_you_want_to_encrypt= input("Enter your message :")
# Encrypt data
encrypted_data = start_var_data_encryptor("enc", the_message_you_want_to_encrypt, key)
print("Encrypted data:", encrypted_data)

# Decrypt data
decrypted_data = start_var_data_encryptor("dec", encrypted_data, key)
print("Decrypted data:", decrypted_data)

'''
