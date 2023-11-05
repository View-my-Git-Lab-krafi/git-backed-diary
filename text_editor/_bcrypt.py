import bcrypt
import getpass

def create_password_hash():
    user_password = getpass.getpass("Enter your password: ")

    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(user_password.encode('utf-8'), salt)
    print("Password hash:", hashed_password.decode('utf-8'))
    print("Salt:", salt.decode('utf-8'))
    return hashed_password, salt

def verify_password():
    stored_hash = input("Enter the stored password hash: ")
    user_password = getpass.getpass("Enter the password to verify: ")
    try:
        if bcrypt.checkpw(user_password.encode('utf-8'), stored_hash.encode('utf-8')):
            print("Correct")
        else:
            print("Wrong")
    except ValueError:
        print("Invalid hash format")

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
