import os
import subprocess
from datetime import datetime
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import hashlib
import random

def secure_delete_file(filename, passes=9):
    try:
        with open(filename, 'rb+') as f:
            file_size = os.path.getsize(filename)
            for _ in range(passes):
                f.seek(0)
                f.write(os.urandom(file_size))
        os.remove(filename)
        print(f"File '{filename}' securely deleted.")
    except FileNotFoundError:
        print(f"temp file not found, You are safe.")

def copy_file(source_file, destination_file): # binary mode
    try:
        with open(source_file, 'rb') as source:
            content = source.read()
        with open(destination_file, 'wb') as destination:
            destination.write(content)
        #print(f"File '{source_file}' copied to '{destination_file}' successfully.")
    except FileNotFoundError:
        print(f"Error: File '{source_file}' not found.")
    except Exception as e:
        print(f"An error occurred while copying the file: {e}")


def print_file_content(filename):
    try:
        subprocess.run(['less', filename], check=True)
    except subprocess.CalledProcessError:
        print(f"Error: File '{filename}' not found or unable to read.")
def view_mode_less():
    md_files = get_md_files_recursively()

    if not md_files:
        print("No .md files found in the current directory or its subdirectories.")
        return

    md_files.sort()

    print("Select a file to view (less mode):")
    for idx, file in enumerate(md_files, start=1):
        print(f"{idx}. {os.path.basename(file)}")

    try:
        choice = int(input("Enter the number of the file you want to view (0 to cancel): "))
        if choice == 0:
            return
        if 1 <= choice <= len(md_files):
            selected_file = md_files[choice - 1]

            source_filename = selected_file
            destination_filename = '.tmp.txt'
            copy_file(source_filename, destination_filename)
            decrypt_file(destination_filename, password)
            print_file_content(destination_filename)
            # subprocess.run(["less", destination_filename])
            file_to_delete = ".tmp.txt"
            secure_delete_file(file_to_delete)

        else:
            print("Invalid choice. Please try again.")

    except ValueError:
        print("Invalid input. Please enter a number.")

def decrypt_file(filename, password):
    block_size = 16
    key = hashlib.sha256(password.encode()).digest()

    with open(filename, 'rb') as file:
        data = file.read()
    if not data.startswith(b'ENCRYPTED:'):
        raise ValueError("The file is not encrypted with this program.")

    data = data[len(b'ENCRYPTED:'):]
    iv = data[:block_size]
    ciphertext = data[block_size:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_data = unpad(cipher.decrypt(ciphertext))
#
    with open(filename, 'wb') as file:
        file.write(decrypted_data)

def pad(data, block_size):
    padding = block_size - len(data) % block_size
    return data + bytes([padding] * padding)

def unpad(data):
    padding = data[-1]
    return data[:-padding]

def encrypt_file(filename, password):
    block_size = 16
    key = hashlib.sha256(password.encode()).digest()
    iv = get_random_bytes(block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)

    with open(filename, 'rb') as file:
        plaintext = file.read()
    padded_plaintext = pad(plaintext, block_size)
    encrypted_data = cipher.encrypt(padded_plaintext)

    with open(filename, 'wb') as file:
        file.write(b'ENCRYPTED:' + iv + encrypted_data)


#################################################################
def create_entry():
    now = datetime.now()
    entry_date = now.strftime("%Y-%m-%d")
    entry_time = now.strftime("%H:%M:%S")

    file_name_input = input("Enter a file name for the diary entry: ") # New file name
    sanitized_file_name = "".join(c if c.isalnum() else "-" for c in file_name_input.lower())
    filename = f"{entry_date}-{sanitized_file_name}.md"

    month_year_dir = now.strftime("%b-%Y")

    if not os.path.exists(month_year_dir):
        os.makedirs(month_year_dir)
    entry_file_path = os.path.join(month_year_dir, filename)

    with open(entry_file_path, "w") as file:
        file.write(f"Date: {entry_date}\nTime: {entry_time}\n\n")

    editor = os.environ.get("EDITOR", "vim")
    subprocess.run([editor, entry_file_path])

    print(f"Diary entry saved to {entry_file_path}")

    wana_encrypt = input("Do you want to encrypt the file ? (y/n)").lower()
    if ( len(wana_encrypt) == 0 or wana_encrypt == "y"):


        encrypt_file(entry_file_path, password)
        source_file = entry_file_path

        filename = f"{entry_date}-{sanitized_file_name}-enc.md"
        enc_entry_file_path = os.path.join(month_year_dir, filename)
        with open(enc_entry_file_path, "w") as file:
            print("created new enc one")

        destination_file = enc_entry_file_path
        copy_file(source_file, destination_file)
        secure_delete_file(entry_file_path)
        print("File encrypted successfully.")
    else:
        print("your file is not encrypt!")


def get_md_files_recursively(directory="."):
    md_files = []
    for root, _, files in os.walk(directory):
        md_files.extend([os.path.join(root, file) for file in files if file.endswith(".md")])
    return md_files

def edit_mode():
    md_files = get_md_files_recursively()

    if not md_files:
        print("No .md files found in the current directory or its subdirectories.")
        return

    print("Select a file to edit:")
    for idx, file in enumerate(md_files, start=1):
        print(f"{idx}. {file}")

    try:
        choice = int(input("Enter the number of the file you want to edit (0 to cancel): "))
        if choice == 0:
            return
        selected_file = md_files[choice - 1]
        ##########
        temp_decrypted_file = ".tmp_decrypted.txt"
        copy_file(selected_file, temp_decrypted_file)
        decrypt_file(temp_decrypted_file, password)

        ##########
        editor = os.environ.get("EDITOR", "vim")
        subprocess.run([editor, temp_decrypted_file])

        now = datetime.now()
        last_modified_date = now.strftime("%Y-%m-%d %H:%M:%S")
        with open(temp_decrypted_file, "a") as file:
            file.write(f"\n\nLast modified: {last_modified_date}\n")
        encrypt_file(temp_decrypted_file, password)
        copy_file(temp_decrypted_file, selected_file)

        secure_delete_file(temp_decrypted_file)

        print(f"File '{selected_file}' edited and saved.")
    except (ValueError, IndexError):
        print("Invalid choice. Please try again.")


def set_editor():
    print("Linux/macOS/termux: \n export EDITOR=vim")
    print("Windows Command Prompt: \n set EDITOR=vim")
    print('Windows PowerShell: \n $env:EDITOR = "vim"')

def commit_to_git():
    commit_message = input("Enter a commit message for Git:\n")
    subprocess.run(["git", "add", "*.md"])
    subprocess.run(["git", "commit", "-m", commit_message])
    subprocess.run(["git", "push"])

    print("Changes committed and pushed to Git repository.")
def first_time_welcome_screen():
    print("Welcome to the program for the first time!")
    first_time_message = "Your password is correct."
    passwd = input("Lets set out passowd do not forget your password you cant recover! Remove passwd.txt file to reset\n Please set your password: ")
    with open(".passwd.txt", 'w') as file:
        file.write("\n<================================================>\n[========Your password is correct. Great!========]\n<================================================>\n\n")
    with open(".passwd_test.txt", 'w') as file:
        pass
    encrypt_file(".passwd.txt", passwd)
    print("Now everytime you open the program you should able to see, 'Your password is correct. Great!' this message  \n that means your passwd is correct")
    print("Now start the program again")
    exit()
def main():

    if not os.path.exists(".passwd.txt"):
        first_time_welcome_screen()
    print("\n\nWelcome to the Git-backed-diary application!\n")
    global password

    password = input("Enter your password: ")
    print("\n")
    copy_file(".passwd.txt", ".passwd_test.txt")


    decrypt_file('.passwd_test.txt', password)

    try:
        with open(".passwd_test.txt", 'r', encoding='utf-8') as file:
            for line in file:
                print(line, end='')
    except UnicodeDecodeError:
        print("Your password looks incorrect because the file contains non-text (binary) data.")
        exit()
    while True:
        file_to_delete = ".tmp.txt"
        secure_delete_file(file_to_delete)
        print("\n1. Create a new diary entry\n2. Commit to Git repository\n3. Edit Mode\n4. Set editor\n5. View Mode (less)\n6. Exit")
        choice = input("Enter your choice (1/2/3/4/5/6): ")

        if choice == "1":
            create_entry()
        elif choice == "2":
            commit_to_git()
        elif choice == "3":
            edit_mode()
        elif choice == "4":
            set_editor()
        elif choice == "5":
            view_mode_less()
        elif choice == "6":
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
