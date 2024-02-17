# pip install markdown2 pycryptodome PySide2
#
#from email.mime import audio
#from fileinput import filename
import re
import os
import sys
import platform
import subprocess
import tkinter as tk
from tkinter import ttk
from datetime import datetime
import shutil
from PySide6.QtWidgets import QApplication, QMainWindow 

from PySide6.QtWidgets import (QApplication, QMainWindow,  QVBoxLayout, QWidget, 
                               QLineEdit, QCalendarWidget, QMessageBox, QLabel,
                               QPushButton, QListWidget, QInputDialog
                               ) 
from PySide6.QtGui import (QFont, QColor) 
from PySide6.QtCore import Qt, QTimer, QDate


#from PySide6.QtWidgets import  QMenu, QMenuBar
#from PySide6 import QtWidgets, QtGui
#from PySide6.QtGui import QSyntaxHighlighter, QIcon, QKeyEvent, QKeySequence, QPalette, QTextCursor, QTextCharFormat
#from PySide6.QtCore import QRegularExpression, QPoint
#from PySide6 import QtWidgets, QtGui, QtCore
# from PySide6.QtWidgets import QFontComboBox, QToolBar, QComboBox, QMenu, QTextEdit, QFileDialog,QSizePolicy

#  local file import
#  from dependencies.emoji_data import categories
from dependencies.EmojiPicker import EmojiPicker
from dependencies.VarDataEncryptor import start_var_data_encryptor
from dependencies.FileEncryptor import start_FileEncryptor
from dependencies.HashPasswordAuthenticator import HashPasswdAuthenticator
from dependencies.GitSync import git_commands
from dependencies.JSON_Database import Json_Database_Initialization, Add_Page, modify_and_save_json, read_json, find_page_number, clear_and_input_new_data
from dependencies.file_manipulation_utils import (
    secure_delete_file, 
    remove_files_with_extensions, secure_delete_file,
    copy_file, copy_file_to_directoryand_rename_file,
    copy_file_to_directoryand_rename_file,
    audiofile_to_flac_then_decode_then_enc,
    copy_file_to_directoryand_rename_audio,
    convert_markdown_to_css
    
)
from dependencies.Magic_Memory_Mark import MagicMemoryMarkTextEditor



def start_magic_memory_mark_editor(passwd):
    global app
    if not app:
        app = QApplication(sys.argv)
    editor = MagicMemoryMarkTextEditor(passwd, None)
    editor.show()
    app.exec()
    app.quit()
    if editor.save:    
        return editor


def create_entry(passwd):
    now = datetime.now()
    entry_date = now.strftime("%Y-%m-%d")
    entry_start_time = now.strftime("%H:%M:%S")
    entry_datetime = f"{entry_date} \n{entry_start_time}\n"  # new one
    Audio_List = []  # For json database
    write_path = (".enc.GitDiarySync/" + now.strftime("%b-%Y") + "/" + now.strftime("%d"))
    if not os.path.exists(write_path):
        os.makedirs(write_path) # just create the path
    print("00")
    note = start_magic_memory_mark_editor(passwd)
    print("0")
    def show_error_message(message):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setText(message)
        msg_box.setWindowTitle("Error")
        msg_box.exec_()

    try:
        saved_text = note.save_text()
    except AttributeError as e:
        show_error_message("Exit without saving new diary page!")
        return
        

    print("1")
################################## If audio added move it to correct path
    md_audio_pattern = re.compile(r'\[.*\]\((.*?)/([^/]+\.(mp3|wav|ogg|aac|m4a|flac|wma|aiff|alac|ape|opus|mid|midi))\)')
    matchs = md_audio_pattern.findall(saved_text)
    print("2")
    for match in matchs:  # Audio detector
        if match:
            print("match ", match)
            file_location = match[0]  # pure name without
            file_name = match[1]  # ext
            
            current_time = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
            AudioFileDirLocation = f"{file_location}/{file_name}"
            AudioFileDirLocation = AudioFileDirLocation.lstrip()  #  remove space

            pure_file_name, file_extension = file_name.rsplit('.', 1)   #  split filename and extensions for changing filename
            new_file_name = f"{pure_file_name}-{current_time}.{file_extension}"
            new_file_name = new_file_name + ".enc.flac.GitDiarySync"

            print("3")
            encrypted_data = audiofile_to_flac_then_decode_then_enc(AudioFileDirLocation, passwd)

            with open("encrypted_img.tmp", "w") as file:
                file.write(encrypted_data)

            audio_file_path = "encrypted_img.tmp"
            write_path_and_newname = write_path
            max_file_size = 49 * 1024 * 1024

            if os.path.getsize(audio_file_path) > max_file_size:
                os.remove(audio_file_path)
                warning_message = (
                    "Alert: The audio file cannot be added because its size exceeds 49MB. "
                    "Please remove the corresponding URL markdown in edit mode. "
                    "This file will not be included in Database_Lieutenant.json, "
                    "So , The audio GUI will not display it."
                )
                QMessageBox.warning(None, "Warning",warning_message )
            else:
                print("4")
                #shutil.move(audio_file_path, write_path_and_newname)

                write_path_and_newname = write_path + "/" + (file_name)

                if platform.system() == "Windows":
                    print("1")
                    abs_source_path = os.path.abspath("encrypted_img.tmp")
                    abs_dest_path = os.path.abspath(write_path_and_newname)
                    try:
                        if os.path.exists(abs_source_path):
                            print("11")
                            print(abs_source_path, abs_dest_path)
                            shutil.move(abs_source_path, abs_dest_path)
                            print("File moved successfully.")
                        else:
                            print("Source file does not exist.")
                    except Exception as e:
                        print(f"Error: {e}")
                else: # linux
                    print("2")
                    shutil.move("encrypted_img.tmp", write_path_and_newname )
                    
                write_path_and_newname = (write_path) + "/" + (file_name)
                Audio_List.append(write_path_and_newname)

                #  "Now, let's modify our entire text, basically replacing."
                md_pattern = re.escape(match[0]) + r"/" + re.escape(match[1])
                saved_text = re.sub(md_pattern, f"{write_path_and_newname}", saved_text)
        else:
            print("5")
            QMessageBox.warning(None, "Warning", "No audio found")
            ##############################
        
################################## If audio added move it to correct path
    md_audio_pattern = re.compile(r'\[.*\]\((.*?)/([^/]+\.(enc\.flac\.GitDiarySync))\)')
    matchs = md_audio_pattern.findall(saved_text)
    for match in matchs:  # Audio detector
        if match:
            file_location = match[0]  # pure name without
            file_name = match[1]  # ext
            
            current_time = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
            AudioDirLocation = f"{file_location}/{file_name}"
            AudioDirLocation = AudioDirLocation.lstrip()  # remove space

            # pure_file_name, file_extension = file_name.rsplit('.', 1)   # split filename and extensions for changing filename
            # new_file_name = f"{pure_file_name}-{current_time}.{file_extension}"
            # new_file_name = new_file_name + "enc.flac.GitDiarySync"

            if platform.system() == "Windows":
                print (AudioDirLocation, ">====>" ,write_path)


                # Get the current working directory
                current_directory = os.getcwd()

                # List the contents of the current working directory
                contents = os.listdir(current_directory)

                # Print the contents
                print("Current Working Directory:", current_directory)
                print("Contents:")
                for item in contents:
                    print(item)

                def check_file_existence(file_path):
                    if os.path.exists(file_path):
                        print(f"The file '{file_path}' exists.")
                    else:
                        print(f"The file '{file_path}' does not exist.")

                # Call the function with the specified source_path
                check_file_existence(AudioDirLocation)
                
                shutil.move(AudioDirLocation, write_path)

            else:
                shutil.move(AudioDirLocation, write_path)

            final_filepath = f'{write_path}{AudioDirLocation[1:]}'
            print("final path ", final_filepath)
            Audio_List.append(final_filepath)

            #  "Now, let's modify our entire text, basically replacing."
            md_pattern = re.escape(match[0]) + r"/" + re.escape(match[1])
            saved_text = re.sub(md_pattern, f"{final_filepath}", saved_text)
        else:
            QMessageBox.warning(None, "Warning", "No audio found")
            ##############################
    md_image_pattern = re.compile(r'!\[.*\]\((.*?)/([^/]+\.(png|jpg|jpeg|gif|svg|webp|bmp|tiff|ico))\)')
    matchs = md_image_pattern.findall(saved_text)
    Photo_List = []  # For json database (It will be useful in future update)
    for match in matchs:  # photo detector
        if match:
            file_location = match[0]  # pure name without
            file_name = match[1]  # ext
            
            current_time = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
            ImgDirLocation = f"{file_location}/{file_name}"


            pure_file_name, file_extension = file_name.rsplit('.', 1) # split filename and extensions for changing filename
            new_file_name = f"{pure_file_name}-{current_time}.{file_extension}"

            #  copy image to our ".enc.GitDiarySync/" dir also give it a new name adding current_time
            final_filepath = copy_file_to_directoryand_rename_file(ImgDirLocation, write_path, new_file_name)
 

            #  Now let encrypt our image with renaming to  ".enc.img.GitDiarySync"
            final_enc_filepath = final_filepath + ".enc.img.GitDiarySync"
            Photo_List.append(final_enc_filepath.replace("\\", "/"))
            
            start_FileEncryptor("encrypt_file", final_filepath, final_enc_filepath, passwd)


            #  "Now, let's modify our entire text, basically replacing."
            md_pattern = re.escape(match[0]) + r"/" + re.escape(match[1])
            print("md_pattern", md_pattern)
            md_pattern = md_pattern.replace("\\", "/")

################
            print("filepath")
            print(final_filepath)
            final_filepath = final_filepath.replace("\\", "/")

            saved_text = re.sub(md_pattern, f"{final_filepath}", saved_text)
            print("saved_tex" ,saved_text)
            print("===================")
            width = 900
            css_image = convert_markdown_to_css(saved_text, width)
            print("css", css_image)
            print("--------------")



            def replace_markdown_with_css(text):
                pattern = r'!\[.*?\]\((.*?\.(png|jpg|jpeg|gif|svg|webp|bmp|tiff|ico))\)'
                replacement = r'<img src="\1" alt=" Attach " title="" width="900">'
                result = re.sub(pattern, replacement, text)
                return result


            saved_text = replace_markdown_with_css(saved_text)

            print(saved_text)



        else:
            QMessageBox.warning(None, "Warning", "No image found")
###############################################



#############################################
    join_date_and_note = f"\n{entry_datetime}\n{saved_text}"
    file_name_input, ok = QInputDialog.getText(None, "File Name", "Enter a file name for the diary entry:", QLineEdit.Normal, "")
    if ok:
        sanitized_file_name = "".join(c if c.isalnum() else "-" for c in file_name_input.lower())
        filename = f"{entry_date}-{sanitized_file_name}.enc.GitDiarySync"
        
        #  filename_without_ext = f"{entry_date}-{sanitized_file_name}"
        Main_Name = sanitized_file_name
        entry_file_path = os.path.join(write_path, filename)
        write_path_Full_Path = entry_file_path
        write_path_Full_Path = write_path_Full_Path.replace("\\", "/")
        #Photo_List = Photo_List.replace("\\", "/")
        Database_Lieutenant_Path = write_path + '/' + 'Database_Lieutenant.json'
        if os.path.exists(Database_Lieutenant_Path):
            original_data = read_json(Database_Lieutenant_Path)
            check_int = 1
            while True:
                Total = str("Page" + str(check_int))
                if Total in original_data:
                    check_int = check_int + 1
                else:
                    break

            data = original_data 
            Page_name = "Page" + str(check_int)
            Add_Page(data, Page_name,
                     Main_Name, write_path_Full_Path,
                     entry_date, entry_start_time,
                     Photo_List, Audio_List,
                     Database_Lieutenant_Path)

            modify_and_save_json(Database_Lieutenant_Path, original_data)

            print("JSON file modified and saved successfully.")

        else:
            Json_Database_Initialization(Main_Name, write_path_Full_Path,
                             entry_date, entry_start_time,
                             Photo_List, Audio_List,
                             Database_Lieutenant_Path)


        enc_note = start_var_data_encryptor("Enc_Fernet_PBKDF2_HMAC_SHA512", join_date_and_note, passwd)

        with open(entry_file_path, "w") as file:  # error
            file.write(enc_note)
        print(f"Diary entry saved to {entry_file_path}")
        remove_files_with_extensions()
    else:
         QMessageBox.warning(None, "Warning", "Failed to create a diary entry. User canceled the operation.")


#Sergeant < lieutenant < captain < major < colonel < general 


def get_md_files_recursively(directory=".enc.GitDiarySync"):
    md_files = []
    for root, _, files in os.walk(directory):
        md_files.extend([os.path.join(root, file) for file in files if file.endswith(".enc.GitDiarySync")])
    return md_files

def choose_file(md_files):
    #app = QApplication([])

    choose_root = QWidget()
    choose_root.setWindowTitle("Select File")
    choose_root.setGeometry(100, 100, 700, 700)

    layout = QVBoxLayout()

    list_widget = QListWidget()
    list_widget.setFixedWidth(400)
    list_widget.setFixedHeight(400)
    font = QFont()
    font.setPointSize(20)
    #font.setBold(True) 

    filtered_files = []
    file_dict = {}

    highlighted_dates = []
    dates = []
    for file_path in file_dict.values():  #  split date
        if platform.system() == "Windows":
            date = file_path.split('\\')[-1][:10]
        else:
            date = file_path.split('/')[-1][:10]
        dates.append(date)

    for file in md_files:
        #  list_widget.addItem(file)  # Get with Full path
        
        if platform.system() == "Windows":
            filename = file.split("\\")[-1]  # filename
        else:
            filename = file.split("/")[-1]  # filename

        if file.endswith('.enc.GitDiarySync'):
            filtered_files.append(filename)  # ['filename']
            list_widget.addItem(filename)  # Add only the file name (bin)
            file_dict[filename] = file  # file is full path

            # lets lightweight whatever date found
            if platform.system() == "Windows":
                date = filename.split('\\')[-1][:10]
            else:
                date = filename.split('/')[-1][:10]  # "2023-11-03"
            year, month, day = map(int, date.split('-'))
            highlighted_dates.append(QDate(year, month, day))

    layout.addWidget(list_widget)
	
    def print_selected_date(selected_date):

        year = selected_date.year()
        month = selected_date.month()
        day = selected_date.day()
        filenamer = f"{year}-{month:02d}-{day:02d}"
        filenamestr = str(filenamer)

        list_widget.clear()
        for file in md_files:
            if platform.system() == "Windows":
                filename = file.split("\\")[-1]
            else:
                filename = file.split("/")[-1]  # filename
            if filename.endswith('.enc.GitDiarySync') and filename.startswith(filenamestr):
                filtered_files.append(filename)  # ['filename']
                list_widget.addItem(filename)  # Add only the file name (bin)
                file_dict[filename] = file  # file is full path
                
                # lets lightweight whatever date found
                if platform.system() == "Windows":
                    date = filename.split('\\')[-1][:10]  # "2023-11-03"
                else:
                    date = filename.split('/')[-1][:10]  # "2023-11-03"
                year, month, day = map(int, date.split('-'))
                highlighted_dates.append(QDate(year, month, day))

    calendar_widget = QCalendarWidget()
    
    for date in highlighted_dates:
        date_format = calendar_widget.dateTextFormat(date)
        semiTransparentYellows = [
            QColor(255, 255, 0, 51),
            QColor(255, 255, 0, 102),
            QColor(255, 255, 0, 153),
            QColor(255, 255, 0, 204),
            QColor(255, 255, 0, 255)
        ]
        current_color = date_format.background().color().rgba()
        for i, color in enumerate(semiTransparentYellows):
            if current_color == color.rgba():
                next_index = (i + 1) % len(semiTransparentYellows)
                date_format.setBackground(semiTransparentYellows[next_index])
                break
        else:
            date_format.setBackground(semiTransparentYellows[0])

        calendar_widget.setDateTextFormat(date, date_format)

    layout.addWidget(calendar_widget)
    select_button = QPushButton("Select")
    layout.addWidget(select_button)
    calendar_widget.clicked.connect(lambda date: print_selected_date(date))

    selected_file = None 

    def on_select():
        nonlocal selected_file
        
        try:
            selected_file_name = list_widget.selectedItems()[0].text()
            selected_file = file_dict.get(selected_file_name, None)
        except IndexError:
            QMessageBox.warning(choose_root, "Warning", "No item selected.")
            return

        if selected_file is None:
            QMessageBox.warning(choose_root, "Warning", "File not found.")
        else:
            choose_root.close()

    select_button.clicked.connect(on_select)
    choose_root.setLayout(layout)

    choose_root.show()
    app.exec()

    return selected_file
    
def edit_n_view_mode(passwd, edit_mode):
    md_files = get_md_files_recursively()
    if not md_files:

        #  global app
        #  if not app:
           #  app = QApplication(sys.argv)

        message_box = QMessageBox()
        message_box.setWindowTitle("Information")
        message_box.setText("No .enc.GitDiarySync files found in the current directory or its subdirectories. Add a Diary page")
        message_box.setIcon(QMessageBox.Information)
        message_box.exec()
        return

    selected_file = choose_file(md_files)

    if selected_file:  # selected_file is the text file
        now = datetime.now()
        edit_start_time = now.strftime("%H:%M:%S")

        print("the selected file", selected_file)
        file_dir = os.path.dirname(selected_file)  # text file location
        all_files = os.listdir(file_dir)  # all other files like image
        matching_files = [file for file in all_files if file.endswith(".enc.img.GitDiarySync")]  # list only enc image

        for file in matching_files:  # enc image to normal image for view
            enc_file = (os.path.join(file_dir, file))
            remove_enc_ext = enc_file.replace(".enc.img.GitDiarySync", "")           
            start_FileEncryptor("decrypt_file", enc_file, remove_enc_ext, passwd)


        temp_decrypted_file = ".tmp"
        copy_file(selected_file, temp_decrypted_file)
        with open(temp_decrypted_file, "r") as file:
            bytes_data = file.read()
        bytes_data_to_str = start_var_data_encryptor("Dec_Fernet_PBKDF2_HMAC_SHA512", bytes_data, passwd)

        if not edit_mode:  # view_mode
            read_only_warning = QMessageBox()
            read_only_warning.setWindowTitle("Read-Only Mode")
            read_only_warning.setIcon(QMessageBox.Warning)
            read_only_warning.setText(
                "Note: You have opened this file in read-only mode. Any attempt to save will not be successful.")
            read_only_warning.exec()

        filetoeditor = MagicMemoryMarkTextEditor(passwd, selected_file)
        filetoeditor.var_to_editor(bytes_data_to_str)
        filetoeditor.show()
        app.exec()
        app.quit()
        dec_note = filetoeditor
        the_saved_text = dec_note.save_text()
####################################
        Photo_List = []
        Audio_List = []  # For json database


    ################################## If audio added move it to correct path
        md_audio_pattern = re.compile(r'\[.*\]\((.*?)/([^/]+\.(mp3|wav|ogg|aac|m4a|flac|wma|aiff|alac|ape|opus|mid|midi))\)')
        matchs = md_audio_pattern.findall(the_saved_text)
        for match in matchs:  # Audio detector
            if match:
                print("match ", match)
                file_location = match[0]  # pure name without
                file_name = match[1]  # ext
                
                current_time = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
                AudioFileDirLocation = f"{file_location}/{file_name}"
                AudioFileDirLocation = AudioFileDirLocation.lstrip()  #  remove space

                pure_file_name, file_extension = file_name.rsplit('.', 1)   #  split filename and extensions for changing filename
                new_file_name = f"{pure_file_name}-{current_time}.{file_extension}"
                new_file_name = new_file_name + ".enc.flac.GitDiarySync"

                encrypted_data = audiofile_to_flac_then_decode_then_enc(AudioFileDirLocation, passwd)

                with open("encrypted_img.tmp", "w") as file:
                    file.write(encrypted_data)

                audio_file_path = "encrypted_img.tmp"
                write_path_and_newname = file_dir



                
                max_file_size = 49 * 1024 * 1024

                if os.path.getsize(audio_file_path) > max_file_size:
                    os.remove(audio_file_path)
                    warning_message = (
                        "Alert: The audio file cannot be added because its size exceeds 49MB. "
                        "Please remove the corresponding URL markdown in edit mode. "
                        "This file will not be included in Database_Lieutenant.json, "
                        "So , The audio GUI will not display it."
                    )
                    QMessageBox.warning(None, "Warning",warning_message )
                else:
                    #shutil.move(audio_file_path, write_path_and_newname)

                    write_path_and_newname = file_dir + "/" + (file_name)

                    if platform.system() == "Windows":
                        abs_source_path = os.path.abspath("encrypted_img.tmp")
                        abs_dest_path = os.path.abspath(write_path_and_newname)
                        try:
                            if os.path.exists(abs_source_path):
                                print(abs_source_path, abs_dest_path)
                                shutil.move(abs_source_path, abs_dest_path)
                                print("File moved successfully.")
                            else:
                                print("Source file does not exist.")
                        except Exception as e:
                            print(f"Error: {e}")
                    else: # linux
                        shutil.move("encrypted_img.tmp", write_path_and_newname )
                        
                    write_path_and_newname = (file_dir) + "/" + (file_name)
                    write_path_and_newname = (write_path_and_newname.replace("\\", "/"))
                    


                    

                    print("------------>>?", the_saved_text)
                    #  "Now, let's modify our entire text, basically replacing."
                    print("< ",(match[0]),(match[1]), ">")
                    escape = (match[0]) + r"/" + (match[1]) 
                    print("escape",escape) # C:/Users/88019/Downloads/asdasd.wav
                    md_pattern = re.escape(escape) # escape special characters in a string 
                    print("write_path_and_newname > ",write_path_and_newname)
                    Audio_List.append(write_path_and_newname)
                    the_saved_text = re.sub(md_pattern, f"{write_path_and_newname}", the_saved_text)
                    print("+++++++++++++")
                    the_saved_text = (the_saved_text.replace("\\", "/"))

                    
            else:
                QMessageBox.warning(None, "Warning", "No audio found")
                ##############################
    ################################## If audio added move it to correct path
        md_audio_pattern = re.compile(r'\[.*\]\((.*?)/([^/]+\.(enc\.flac\.GitDiarySync))\)')
        matchs = md_audio_pattern.findall(the_saved_text)
        for match in matchs:  # Audio detector
            if match:
                file_location = match[0]  # pure name without
                file_name = match[1]  # ext
                
                AudioDirLocation = f"{file_location}/{file_name}"
                AudioDirLocation = AudioDirLocation.lstrip()  # remove space

                write_path = os.path.dirname(selected_file) 
                file_name = os.path.basename(selected_file)
                basenameofaudio = os.path.basename(AudioDirLocation)

                if AudioDirLocation.startswith(".enc.GitDiarySync/"): # Dont do anything with old one 
                    Audio_List.append(AudioDirLocation)
                else:

                    shutil.move(AudioDirLocation, write_path)
                    final_filepath = f'{write_path}{AudioDirLocation[1:]}'
                    
                    final_filepath = final_filepath.replace("\\", "/")
                    #final_filepath = copy_file_to_directoryand_rename_audio(AudioDirLocation, write_path, basenameofaudio)
                    print("final path ", final_filepath)
                    Audio_List.append(final_filepath)

                    #  "Now, let's modify our entire text, basically replacing."
                    md_pattern = re.escape(match[0]) + r"/" + re.escape(match[1])

                    the_saved_text = re.sub(md_pattern, f"{final_filepath}", the_saved_text)
            else:
                QMessageBox.warning(None, "Warning", "No audio found")
                ##############################

################################## If photo added move it to correct path
        # if photo is inside .enc.GitDiarySync directory ignore that file .
        md_image_pattern = re.compile(r'!\[.*\]\((?!.*\.enc\.GitDiarySync)(.*?)/([^/]+\.(png|jpg|jpeg|gif|svg|webp|bmp|tiff|ico))\)')

        matchs = md_image_pattern.findall(the_saved_text)

        

        for match in matchs:
            # Check if a match is found and print file location and name
            if match:
                file_location = match[0]  # match.group(1)
                file_name = match[1]  #  match.group(2)
                current_time = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
                WhereTheImageIs = f"{file_location}/{file_name}"

                file_name, file_extension = file_name.rsplit('.', 1)  #  for changing filename
                new_file_name = f"{file_name}-{current_time}.{file_extension}"
        
                write_path = os.path.dirname(selected_file)  #  text file location
                # all_files = os.listdir(file_dir) # all other files like image

                print("============", new_file_name)                
                final_filepath = copy_file_to_directoryand_rename_file(WhereTheImageIs, write_path, new_file_name)
                final_enc_filepath = final_filepath + ".enc.img.GitDiarySync"
                start_FileEncryptor("encrypt_file", final_filepath, final_enc_filepath, passwd)
                final_filepath = final_filepath.replace("\\", "/")
                final_enc_filepath = final_enc_filepath.replace("\\", "/")
                Photo_List.append(final_enc_filepath)
                md_pattern = re.escape(match[0]) + r"/" + re.escape(match[1])
                the_saved_text = re.sub(md_pattern, f"{final_filepath}", the_saved_text)
            else:
                print("No image found")



###############################################
        if filetoeditor.save:    
            if edit_mode:
                last_modified_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                last_modified_date_string = f"\n\nLast modified: {last_modified_date}\n"
                total_note = f"{the_saved_text} {last_modified_date_string}"
                enc_note = start_var_data_encryptor("Enc_Fernet_PBKDF2_HMAC_SHA512", total_note, passwd)

                
                ##################
                Database_Lieutenant_Path = file_dir + '/' + 'Database_Lieutenant.json'
                if os.path.exists(Database_Lieutenant_Path):
                    original_data = read_json(Database_Lieutenant_Path)
                    data = original_data 

                    target_path_to_find = selected_file

                    Database_Lieutenant_Path = Database_Lieutenant_Path.replace("\\", "/")
                    target_path_to_find = target_path_to_find.replace("\\", "/")

                    page_number_found = find_page_number(Database_Lieutenant_Path, target_path_to_find)
                    print(page_number_found, Database_Lieutenant_Path, target_path_to_find)

                    if page_number_found is not None:
                        print(f"{page_number_found}")
                    else:
                        print(f"No page found for the given path.")

                    Page = page_number_found #"Page" + str(check_int)
                    print(page_number_found)

                    modify_and_save_json(Database_Lieutenant_Path, original_data)

                    print("JSON file modified and saved successfully.")
                    file_name = os.path.basename(selected_file)
                    print("selected file ", selected_file)


                    Main_Name_Full_Path = selected_file
                    
                    Main_Name_Full_Path = Main_Name_Full_Path.replace("\\", "/")

                    Main_Name = file_name
                    entry_file_path = os.path.join(file_dir, file_name)
                    write_path_Full_Path = entry_file_path


                    Database_Lieutenant_Path = file_dir + '/' + 'Database_Lieutenant.json'
                    now = datetime.now()
                    edit_end_time = now.strftime("%H:%M:%S")
                    last_entry_date =last_modified_date

                    
                    clear_and_input_new_data(data, Page ,
                                            Main_Name, Main_Name_Full_Path,
                                            edit_start_time, edit_end_time,
                                            last_entry_date, Photo_List, Audio_List, 
                                        Database_Lieutenant_Path)

                else:
                    print("error")
                
                #####################################
                





                with open(temp_decrypted_file, "w") as file:
                    file.write(enc_note)
                copy_file(temp_decrypted_file, selected_file)

        secure_delete_file(temp_decrypted_file)
# 
def view_mode_less(passwd, edit_mode):
    md_files = get_md_files_recursively()

    if not md_files:
        print("No .enc.GitDiarySync files found in the current directory or its subdirectories.")
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
            destination_filename = '.tmp'
            copy_file(source_filename, destination_filename)
            # binary_data = None

            with open(destination_filename, 'r') as binary_file:
                binary_data = binary_file.read()
            decrypt_data = start_var_data_encryptor("Dec_Fernet_PBKDF2_HMAC_SHA512", binary_data, passwd)
            p = subprocess.Popen(["less"], stdin=subprocess.PIPE)
            p.communicate(input=decrypt_data.encode())

            file_to_delete = ".tmp"
            secure_delete_file(file_to_delete)

        else:
            print("Invalid choice. Please try again.")

    except ValueError:
        print("Invalid input. Please enter a number.")

def commit_to_git():
    git_commands()
    
def input_passwd(FirstTime):
    global app
    if not app:
        app = QApplication(sys.argv)   #  Create the QApplication instance
        print("Create the QApplication instance")
    if app:
        app = QApplication.instance()  # retrieves the instance
        print("retrieves the instance")
    #app = QApplication([])
    window = QMainWindow()
    window.setWindowTitle("Personal Diary")

    window.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)
    window.setWindowFlags(Qt.Dialog)
    
    screen_resolution = app.primaryScreen().geometry()
    #screen_resolution = app.desktop().screenGeometry()
    
    width, height = 400, 200
    x = (screen_resolution.width() - width) // 2
    y = (screen_resolution.height() - height) // 2

    window.setGeometry(x, y, width, height)
    central_widget = QWidget()
    window.setCentralWidget(central_widget)
    layout = QVBoxLayout(central_widget)

    title_label = QLabel("Welcome to Personal Diary")
    title_label.setFont(QFont("Arial", 18, QFont.Bold))
    title_label.setStyleSheet("color: blue;")
    layout.addWidget(title_label)

    passwd_label = QLabel("Enter Password:")
    passwd_label.setFont(QFont("Arial", 14, QFont.Bold))
    layout.addWidget(passwd_label)

    passwd_entry = QLineEdit()
    passwd_entry.setEchoMode(QLineEdit.Password)
    passwd_entry.setFont(QFont("Arial", 14, QFont.Bold))
    layout.addWidget(passwd_entry)

    check_button = QPushButton("Unlock Diary")
    check_button.setFont(QFont("Arial", 14, QFont.Bold))
    layout.addWidget(check_button)

    #entered_passwd = "" 

    def on_button_click():
        passwd = passwd_entry.text()
        window.close()
        if FirstTime:
            hash_note = HashPasswdAuthenticator("BcryptEnc", passwd, "NoHash")
            print(hash_note)
            with open("enc.GitDiarySync", 'w') as file:
                file.write(hash_note)
            msg_box = QMessageBox()
            msg_box.setText("Setup completed. Start the program again.")
            msg_box.exec()
            sys.exit()
        else:
            pass
            

    check_button.clicked.connect(on_button_click)
    passwd_entry.returnPressed.connect(on_button_click)
    window.show()
    app.exec()

    # passwd = passwd_entry.text()
    return passwd_entry.text()


def input_pass_now_first_time(wel_root):

    wel_root.hide()
    FirstTime = True
    input_passwd(FirstTime)

def first_time_welcome_screen():
    global app
    app = QApplication(sys.argv)
    wel_root = QMainWindow()
    wel_root.setWindowTitle("Git-backed-diary Password Verification")

    central_widget = QWidget()
    layout = QVBoxLayout()

    welcome_label = QLabel()
    welcome_label.setText("Welcome to the Git-backed diary application!\n\nFor security reasons, please set a strong password for your diary.\nKeep in mind that once set, the password cannot be recovered, so be sure to remember it.\nIf you ever wish to reset the password, delete the 'enc.GitDiarySync' file and run this program again to create a new one.\n Keep your password safe and secure, as it will protect your diary entries from unauthorized access.\n\n Tips: If you remove the 'enc.GitDiarySync' and set your old password again, you can access your old content. \n\nPlease enter your password")
    layout.addWidget(welcome_label)

    wel_root.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)
    wel_root.setWindowFlags(Qt.Dialog)

    start_button = QPushButton("Ready for input password")
    start_button.clicked.connect(lambda: input_pass_now_first_time(wel_root))
    layout.addWidget(start_button)

    central_widget.setLayout(layout)
    wel_root.setCentralWidget(central_widget)
    wel_root.show()
    sys.exit(app.exec())

def close_window(window):
    window.destroy()


def main():
    global app
    app = None
    if not os.path.exists("enc.GitDiarySync"):
        first_time_welcome_screen()
    print("\n\nWelcome to the Git-backed-diary application!\n")
    FirstTime = False
    passwd = input_passwd(FirstTime)
    print("\n")
    copy_file("enc.GitDiarySync", ".tmp")
    with open(".tmp", 'r') as file:
        encrypted_data = file.read()

    # login password check section  QMessageBox()
    content = HashPasswdAuthenticator("BcryptDec", passwd, encrypted_data)  # you can also try Pbkdf2tEnc
    if content:
        close_timer = QTimer()
        success_message = QMessageBox()
        success_message.setWindowTitle("File Content")
        success_message.setText("Your password is correct. Great!")
        success_message.setIcon(QMessageBox.Information)
        success_message.setStandardButtons(QMessageBox.Ok)
        close_timer.timeout.connect(success_message.accept)
        close_timer.start(2000) 
        success_message.exec()

    else:

        error_message = QMessageBox()
        error_message.setIcon(QMessageBox.Critical)
        error_message.setWindowTitle("Password Error")
        error_message.setText("Your password appears to be incorrect.\n"
                            "If you wish to reset it, delete the 'enc.GitDiarySync' file and run this program again to create a new one.\n"
                            "Please note that you will lose access to your old notes if you set a new password.\n"
                            "However, if you can recall your old correct password, you can regain access to your files.\n"
                            "Tips: If you remove the 'enc.GitDiarySync' and set your old password again, you can access your old content.")
        error_message.exec()
        sys.exit()
    while True:
        secure_delete_file(".tmp")
        remove_files_with_extensions() # remove all photo:
        def handle_choice(event):
            choice = event.char
            if choice in ["1", "2", "3", "4", "5", "6"]:
                handle_button_click(choice)

        def handle_button_click(choice):
            if choice == "1":
                create_entry(passwd)
            elif choice == "2":
                commit_to_git()
            elif choice == "3":                
                edit_n_view_mode(passwd, edit_mode=True)
            elif choice == "4":
                edit_n_view_mode(passwd, edit_mode=False)
            elif choice == "5":
                view_mode_less(passwd, edit_mode=False)
            elif choice == "6":
                root.quit()
                sys.exit()
            else:
                output_label.config(text="Invalid choice. Please try again.")

        root = tk.Tk()
        root.title("Menu")
        
        if platform.system() == "Linux":
            print("Great, You are a linux user!")
            root.wm_attributes("-type", "splash")  # WM    
            root.wm_attributes("-topmost", 1)  # WM
        style = ttk.Style() 
        style.theme_use('clam')
        
        style.configure('TFrame', background='#ffdab9') # corner part
        root.configure(background='#ffdab9')  # background
        style.configure('.', background='#ffe2c6')  # button

        prompt_label = ttk.Label(root, text="Press a number key (1/2/3/4/5/6):")
        prompt_label.pack()
        output_label = ttk.Label(root, text="")
        output_label.pack()
        
        root.bind("<Key>", handle_choice)
        button_frame = ttk.Frame(root)
        button_frame.pack()
        button_labels = {
            "1": "Add Diary Page",
            "2": "Sync with Git",
            "3": "Edit Mode",
            "4": "View Mode",
            "5": "View Mode (CLI)",
            "6": "Quit"}
        for i in range(1, 7):
            button = ttk.Button(button_frame, text=str(i) + " - " + button_labels[str(i)], command=lambda i=i: handle_button_click(str(i)))            
            button.pack(side="top")
        root.mainloop()
if __name__ == "__main__":
    main()
