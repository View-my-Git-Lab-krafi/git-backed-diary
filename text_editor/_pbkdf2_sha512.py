from passlib.hash import pbkdf2_sha512 
import secrets
import getpass
def create_password_hash():
    user_password = getpass.getpass("Enter your password: ")

    salt = secrets.token_bytes(99)
    hashed_password = pbkdf2_sha512.using(salt=salt).hash(user_password)
    print("Password hash:", hashed_password)
    print("Salt:", salt)
    return hashed_password, salt


def verify_password():
    stored_hash = input("Enter the stored password hash: ")
    user_password = input("Enter the password to verify: ")
    try:
        if pbkdf2_sha512.verify(user_password, stored_hash):
            print("correct")
        else:
            print("wrong.")
    except ValueError:
        print("Invalid hash format.")

while True:
    print("1. Create Password Hash")
    print("2. Verify Password")
    print("3. Exit")
    choice = input("Enter your choice (1/2/3): ")
    
    if choice == '1':
        create_password_hash()
    elif choice == '2':
        verify_password()
    elif choice == '3':
        break
    else:
        print("Invalid choice. Please select 1, 2, or 3.")
