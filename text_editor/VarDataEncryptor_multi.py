import getpass
import bcrypt
from passlib.hash import pbkdf2_sha512
import secrets
import getpass

def create_password_hash(method_choice):
    user_password = getpass.getpass("Enter your password: ")
    
    if method_choice == '1':
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(user_password.encode('utf-8'), salt)
        print("Password hash:", hashed_password.decode('utf-8'))
        print("Salt:", salt.decode('utf-8'))
    elif method_choice == '2':
        salt = secrets.token_bytes(99)
        hashed_password = pbkdf2_sha512.using(salt=salt).hash(user_password)
        print("Password hash:", hashed_password)
        print("Salt:", salt)
    else:
        print("Invalid choice. Please select 1 or 2.")

def verify_password(method_choice):
    stored_hash = input("Enter the stored password hash: ")
    user_password = input("Enter the password to verify: ")

    if method_choice == '1':
        try:
            if bcrypt.checkpw(user_password.encode('utf-8'), stored_hash.encode('utf-8')):
                print("Correct")
            else:
                print("Wrong")
        except ValueError:
            print("Invalid hash format")
    elif method_choice == '2':
        try:
            if pbkdf2_sha512.verify(user_password, stored_hash):
                print("Correct")
            else:
                print("Wrong")
        except ValueError:
            print("Invalid hash format")
    else:
        print("Invalid choice. Please select 1 or 2.")

print("Choose a password hashing method:")
print("1. Bcrypt (recommended)")
print("2. PBKDF2")
method_choice = input("Enter your choice (1/2): ")

while True:
    print("1. Create Password Hash")
    print("2. Verify Password")
    print("3. Exit")
    choice = input("Enter your choice (1/2/3): ")
    
    if choice == '1':
        create_password_hash(method_choice)
    elif choice == '2':
        verify_password(method_choice)
    elif choice == '3':
        break
    else:
        print("Invalid choice. Please select 1, 2, or 3.")
