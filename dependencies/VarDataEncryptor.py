
import os
import base64
'''
#  pip install cryptography
#import getpass
#import sys
#import hashlib 
#import getpass
#import bcrypt
#from passlib.hash import pbkdf2_sha512
#import secrets
#import getpass
def pad(data, block_size):
    padding = block_size - len(data) % block_size
    return data + bytes([padding] * padding)

def unpad(data):
    padding = data[-1]
    return data[:-padding]

def Enc_AES_CBC(data, password):
    salt = get_random_bytes(16)
    key = PBKDF2(password, salt, 32, 100000)

    iv = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = data.encode()
    padded_plaintext = pad(plaintext, 16)
    encrypted_data = cipher.encrypt(padded_plaintext)
    enc_binary_data = b'ENCRYPTED:' + salt + iv + encrypted_data
    encrypted_hex = enc_binary_data.hex()
    return encrypted_hex

def Dec_AES_CBC(encrypted_data, password):
    encrypted_binary_data = bytes.fromhex(encrypted_data)
    if not encrypted_binary_data.startswith(b'ENCRYPTED:'):
        raise ValueError("The data is not encrypted with this program.")
    encrypted_binary_data = encrypted_binary_data[len(b'ENCRYPTED:'):]
    salt = encrypted_binary_data[:16]
    iv = encrypted_binary_data[16:32]
    ciphertext = encrypted_binary_data[32:]
    key = PBKDF2(password, salt, 32, 100000)
    #password = None #secure mode maybe i will add this feature in future.
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_data = unpad(cipher.decrypt(ciphertext))
    return decrypted_data.decode()


############################################################################

# AES encryption in CFB mode along with PBKDF2, HMAC, and SHA-512 

def ASE_CFB_derive_key(password, salt):
    
    from cryptography.hazmat.primitives import hashes, hmac
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

    from cryptography.hazmat.backends import default_backend
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA512(),
        iterations=100000,
        salt=salt,
        length=32,
        backend=default_backend()
    )
    return kdf.derive(password.encode())

def Enc_ASE_CFB_PBKDF2_HMAC_SHA512(data, passwd):

    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    from cryptography.hazmat.primitives import serialization
    from cryptography.hazmat.backends import default_backend
    from cryptography.fernet import Fernet

    salt = os.urandom(16)
    key = ASE_CFB_derive_key(passwd, salt)
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted_text = encryptor.update(data.encode()) + encryptor.finalize()
    enc_binary_data =  salt + iv + encrypted_text
    encrypted_hex = enc_binary_data.hex()
    return encrypted_hex

def Dec_ASE_CFB_PBKDF2_HMAC_SHA512(encrypted_data, passwd):

    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives import serialization
    from cryptography.fernet import Fernet

    encrypted_data = bytes.fromhex(encrypted_data)
    salt = encrypted_data[:16]
    iv = encrypted_data[16:32]
    cipher_text = encrypted_data[32:]    
    key = ASE_CFB_derive_key(passwd, salt)
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_text = decryptor.update(cipher_text) + decryptor.finalize()
    return decrypted_text.decode()

'''
############################################################################
#  Fernet symmetric encryption with a key derived from a password using PBKDF2HMAC with SHA512.




def Fernet_derive_key(password, salt):
    
    from cryptography.hazmat.primitives import hashes, hmac
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    from cryptography.hazmat.backends import default_backend

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA512(),
        iterations=100000,
        salt=salt,
        length=32,
        backend=default_backend()
    )
    return kdf.derive(password.encode())

def Enc_Fernet_PBKDF2_HMAC_SHA512(data, passwd):
    from cryptography.fernet import Fernet

    salt = os.urandom(16)
    key = Fernet_derive_key(passwd, salt)
    cipher = Fernet(base64.urlsafe_b64encode(key))
    encrypted_text = cipher.encrypt(data.encode())
    enc_binary_data =  salt + encrypted_text
    encrypted_hex = enc_binary_data.hex()
    return encrypted_hex

def Dec_Fernet_PBKDF2_HMAC_SHA512(encrypted_data, passwd):

    from cryptography.fernet import Fernet
    encrypted_data = bytes.fromhex(encrypted_data)
    salt = encrypted_data[:16]
    cipher_text = encrypted_data[16:]    
    key = Fernet_derive_key(passwd, salt)
    cipher = Fernet(base64.urlsafe_b64encode(key))
    decrypted_text = cipher.decrypt(cipher_text)
    return decrypted_text.decode()

############################################################################



def start_var_data_encryptor(worktype, data, passwd):    
    if worktype == "Enc_AES_CBC":
        # AES (Advanced Encryption Standard) in CBC (Cipher Block Chaining) mode
        from Crypto.Cipher import AES
        from Crypto.Random import get_random_bytes
        from Crypto.Protocol.KDF import PBKDF2
        enc = Enc_AES_CBC(data, passwd)
        #print(enc)
        return enc
    elif worktype == "Dec_AES_CBC":
        # AES (Advanced Encryption Standard) in CBC (Cipher Block Chaining) mode
        from Crypto.Cipher import AES
        from Crypto.Random import get_random_bytes
        from Crypto.Protocol.KDF import PBKDF2
        dec = Dec_AES_CBC(data, passwd)
        #print(dec)
        return dec
    elif worktype == "Enc_Fernet_PBKDF2_HMAC_SHA512":
        
        enc = Enc_Fernet_PBKDF2_HMAC_SHA512(data, passwd)
        #print(dec)
        return enc
    elif worktype == "Dec_Fernet_PBKDF2_HMAC_SHA512":
        dec = Dec_Fernet_PBKDF2_HMAC_SHA512(data, passwd)
        #print(dec)
        return dec
'''
#testing 
enc = start_var_data_encryptor("Enc_Fernet_PBKDF2_HMAC_SHA512", "hello", "hi")    
print(enc)
dec = start_var_data_encryptor("Dec_Fernet_PBKDF2_HMAC_SHA512", enc, "hi")    
print(dec)
'''
