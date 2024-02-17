
import os
from PIL import Image
import platform

def secure_delete_file_plus(filename, passes=9):
    def delete_file_on_linux(filename, passes):
        os.system(f'shred -u -z -n {passes} {filename}')
    
    def delete_file_on_windows(filename, passes):
        os.system(f'sdelete -p {passes} -z {filename}')   
    current_platform = platform.system()

    if current_platform == "Linux" or current_platform == "Unix":
        delete_file_on_linux(filename, passes)
    elif current_platform == "Windows":
        delete_file_on_windows(filename, passes)
    else:
        print("Unsupported platform. Cannot securely delete file.")


def convert_markdown_to_css(markdown_text, width):
    import re
    markdown_pattern = r'\!\[([^]]+)\]\(([^)]+\.(png|jpg|jpeg|gif|svg|webp|bmp|tiff|ico))(?:\s*"([^"]+)")?\)'

    matches = re.findall(markdown_pattern, markdown_text)

    if matches:
        alt_text, image_path, extension, mouseover_text = matches[0]

        supported_extensions = {'png', 'jpg', 'jpeg', 'gif', 'svg', 'webp', 'bmp', 'tiff', 'ico'}
        if extension.lower() not in supported_extensions:
            return f"Unsupported file extension: {extension}"

        css_image = f'<img src="{image_path}" alt="{alt_text}" title="{mouseover_text}" width= "{width}">'

        return css_image
    else:
        return "No match found in the given Markdown text."

def secure_delete_file(filename, passes=9):
    try:
        with open(filename, 'rb+') as f:
            file_size = os.path.getsize(filename)
            for _ in range(passes):
                f.seek(0)
                f.write(os.urandom(file_size))
        os.remove(filename)
    except FileNotFoundError:
        print(f"temp file not found, You are safe.")
    if (passes == 8):
        try:
            secure_delete_file_plus(filename,9)
        except Exception as e:
            print("Error on secure_delete_file_plus")

def remove_files_with_extensions():
    print("remove_files_with_extensions")

    extension = '.enc.flac.GitDiarySync' #unsave
    def remove_files_with_extension(directory, extension):
        for filename in os.listdir(directory):
            if filename.endswith(extension):
                print(os.path.join(directory, filename))
                remove =(os.path.join(directory, filename))

                secure_delete_file(remove)

    current_directory = os.getcwd()
    removefile = current_directory, extension
    remove_files_with_extension(current_directory, extension)

    folder_path = ".enc.GitDiarySync"
    extensions = {'.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp', '.bmp', '.tiff', '.ico'}

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            _, file_extension = os.path.splitext(file_path)
            if file_extension.lower() in extensions:
                secure_delete_file(file_path)
                print(f"Securely deleted: {file_path}")
    ######################


def copy_file(source_file, destination_file):
    try:
        with open(source_file, 'r') as source:
            content = source.read()
        with open(destination_file, 'w') as destination:
            destination.write(content)
    except FileNotFoundError:
        print(f"Error: File '{source_file}' not found.")
    except Exception as e:
        print(f"An error occurred while copying the file: {e}")


def copy_file_to_directoryand_rename_audio(source_file, destination_dir, new_filename):

    #if os.path.exists(file_path) and os.path.getsize(file_path) > 49 * 1024 * 1024:  # 49MB in bytes
        #print("no")
    filename = os.path.basename(source_file)
    destination_path = os.path.join(destination_dir, new_filename)
    with open(source_file, 'rb') as source, open(destination_path, 'wb') as destination:
        destination.write(source.read())
    return destination_path

def copy_file_to_directoryand_rename_file(source_file, destination_dir, new_filename):
    new_filename = os.path.splitext(new_filename)[0] + ".webp"

    #if os.path.exists(file_path) and os.path.getsize(file_path) > 49 * 1024 * 1024:  # 49MB in bytes
        #print("no")
    filename = os.path.basename(source_file)
    destination_path = os.path.join(destination_dir, new_filename)
    with open(source_file, 'rb') as source, open(destination_path, 'wb') as destination:
        destination.write(source.read())
    #return os.path.abspath(destination_path)
    convert_to_webp(destination_path)
    return destination_path



def convert_to_webp(image_path):
    quality = 100
    max_file_size = 44 

    try:
        with Image.open(image_path) as img:
            img.save(image_path, format="WEBP", quality=quality)

        file_size_mb = os.path.getsize(image_path) / (1024 * 1024)

        if file_size_mb > max_file_size and quality > 6:
            quality -= 6
            convert_to_webp(image_path)
        else:
            print(f"Conversion to WebP successful for {image_path}")
    except Exception as e:
        print(f"Error converting {image_path} to WebP: {e}")

def secure_delete_file_plus(filename, passes=9):
    def delete_file_on_linux(filename, passes):
        os.system(f'shred -u -z -n {passes} {filename}')
    
    def delete_file_on_windows(filename, passes):
        os.system(f'sdelete -p {passes} -z {filename}')   
    current_platform = platform.system()

    if current_platform == "Linux" or current_platform == "Unix":
        delete_file_on_linux(filename, passes)
    elif current_platform == "Windows":
        delete_file_on_windows(filename, passes)
    else:
        print("Unsupported platform. Cannot securely delete file.")


def secure_delete_file_non_bin(filename, passes=9):
    try:
        with open(filename, 'r+') as f:
            file_size = os.path.getsize(filename)
            for _ in range(passes):
                f.seek(0)
                f.write(os.urandom(file_size))
        os.remove(filename)
    except FileNotFoundError:
        print(f"temp file not found, You are safe.")
    if (passes == 8):
        try:
            secure_delete_file_plus(filename,9)
        except Exception as e:
            print("Error on secure_delete_file_plus")

def secure_delete_file(filename, passes=9):
    try:
        with open(filename, 'rb+') as f:
            file_size = os.path.getsize(filename)
            for _ in range(passes):
                f.seek(0)
                f.write(os.urandom(file_size))
        os.remove(filename)
    except FileNotFoundError:
        print(f"temp file not found, You are safe.")
    if (passes == 8):
        try:
            secure_delete_file_plus(filename,9)
        except Exception as e:
            print("Error on secure_delete_file_plus")


def copy_file(source_file, destination_file):
    try:
        with open(source_file, 'r') as source:
            content = source.read()
        with open(destination_file, 'w') as destination:
            destination.write(content)
    except FileNotFoundError:
        print(f"Error: File '{source_file}' not found.")
    except Exception as e:
        print(f"An error occurred while copying the file: {e}")


def copy_file_to_directoryand_rename_file(source_file, destination_dir, new_filename):
    new_filename = os.path.splitext(new_filename)[0] + ".webp"

    print(new_filename)
    #if os.path.exists(file_path) and os.path.getsize(file_path) > 49 * 1024 * 1024:  # 49MB in bytes
        #print("no")
    filename = os.path.basename(source_file)
    destination_path = os.path.join(destination_dir, new_filename)
    with open(source_file, 'rb') as source, open(destination_path, 'wb') as destination:
        destination.write(source.read())
    #return os.path.abspath(destination_path)
    convert_to_webp(destination_path)
    return destination_path



def convert_to_webp(image_path):
    quality = 100
    max_file_size = 44 

    try:
        with Image.open(image_path) as img:
            img.save(image_path, format="WEBP", quality=quality)

        file_size_mb = os.path.getsize(image_path) / (1024 * 1024)

        if file_size_mb > max_file_size and quality > 6:
            quality -= 6
            convert_to_webp(image_path)
        else:
            print(f"Conversion to WebP successful for {image_path}")
    except Exception as e:
        print(f"Error converting {image_path} to WebP: {e}")



def audiofile_to_flac_then_decode_then_enc(file_path, passwd):
    from pydub import AudioSegment
    import base64
    from dependencies.VarDataEncryptor import start_var_data_encryptor
    supported_formats = ["mp3", "wav", "ogg", "aac", "m4a", "flac", "wma", "aiff", "alac", "ape", "opus", "mid", "midi"]

    # Extract the file format
    file_format = file_path.split('.')[-1]

    # Check if the file format is supported
    if file_format.lower() not in supported_formats:
        print(f"Unsupported audio format: {file_format}")
        return

    # Load the audio file
    audio_segment = AudioSegment.from_file(file_path, format=file_format)
    # Export as FLAC and read the binary data
    flac_data = audio_segment.export(format="flac").read()


    # Decode with base64 and print
    decoded_data = base64.b64encode(flac_data).decode() #decode for enc
    encrypted_data = start_var_data_encryptor("Enc_Fernet_PBKDF2_HMAC_SHA512", decoded_data, passwd)
    return encrypted_data
