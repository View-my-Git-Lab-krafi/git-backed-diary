
import getpass
import bcrypt
from passlib.hash import pbkdf2_sha512
import secrets
import getpass

def create_password_hash(method_choice, passwd):
    
    if method_choice == "BcryptEnc":
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(passwd.encode('utf-8'), salt)
        passwd = hashed_password.decode('utf-8')
        #print("Password hash:", passwd)
        #print("Salt:", salt.decode('utf-8'))
        return passwd
    elif method_choice == "Pbkdf2tEnc":
        salt = secrets.token_bytes(99)
        hashed_password = pbkdf2_sha512.using(salt=salt).hash(passwd)
        #print("Password hash:", hashed_password)
        #print("Salt:", salt)
        return passwd
    else:
        create_password_hash(method_choice, passwd)

def verify_password(method_choice, passwd, hashed_password):

    if method_choice == "BcryptDec":
        try:
            if bcrypt.checkpw(passwd.encode('utf-8'), hashed_password.encode('utf-8')):
                PasswdResult = True
                return PasswdResult
            else:
                PasswdResult = False
                return PasswdResult
        except ValueError:
            print("Invalid hash format")
    elif method_choice == "Pbkdf2Dec":
        try:
            if pbkdf2_sha512.verify(passwd, hashed_password):
                PasswdResult = True
                return PasswdResult
            else:
                PasswdResult = False
                return PasswdResult
        except ValueError:
            print("Invalid hash format")
    else:
        print("Invalid choice. Please select 1 or 2.")
def HashPasswdAuthenticator(method_choice, passwd, hash_passwd):
    if method_choice == "BcryptEnc":
        passwd = create_password_hash(method_choice, passwd)
        return passwd
    elif method_choice == "BcryptDec":
        passwd = verify_password(method_choice, passwd, hash_passwd)
        return passwd
    elif method_choice == "Pbkdf2tEnc":
        result = create_password_hash(method_choice, passwd)
        return result
    elif method_choice == "Pbkdf2Dec":
        result = verify_password(method_choice, passwd, hashed_password)
        return result

