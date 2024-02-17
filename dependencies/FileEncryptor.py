import os

from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64


def key_derivation(password, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA512(),
        iterations=100000,
        salt=salt,
        length=32,
        backend=default_backend()
    )
    key = kdf.derive(password.encode('utf-8'))
    return base64.urlsafe_b64encode(key)


def Enc_Fernet_PBKDF2_HMAC_SHA512(input_file, output_file, password):
    salt = os.urandom(16)
    key = key_derivation(password, salt)

    cipher = Fernet(key)

    with open(input_file, 'rb') as file:
        plaintext = file.read()

    encrypted_data = cipher.encrypt(plaintext)

    with open(output_file, 'wb') as file:
        file.write(salt + b'\0' + encrypted_data)



def Dec_Fernet_PBKDF2_HMAC_SHA512(input_file, output_file, password):
    with open(input_file, 'rb') as file:
        data = file.read()
    
    salt = data[:16]
    ciphertext = data[16:]


    key = key_derivation(password, salt)

    cipher = Fernet(key)
    decrypted_data = cipher.decrypt(ciphertext)

    with open(output_file, 'wb') as file:
        file.write(decrypted_data)




def start_FileEncryptor(worktype, input_file_path, output_file_path, password):


    if worktype == "encrypt_file":
        Enc_Fernet_PBKDF2_HMAC_SHA512(input_file_path, output_file_path, password)
    elif worktype == "decrypt_file":
        Dec_Fernet_PBKDF2_HMAC_SHA512(input_file_path, output_file_path, password)
    else:
        print("Invalid worktype. Use 'encrypt_file' or 'decrypt_file'.")


#start_FileEncryptor("encrypt_file", "ac.png", "gg5.png", 'MySecurePassword123!')
#start_FileEncryptor("decrypt_file", "gg5.png", "dd.png", 'MySecurePassword123!')
