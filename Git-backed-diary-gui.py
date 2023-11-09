# pip install markdown2 pycryptodome PySide2

import re
import os
import io
import sys
import random
import hashlib
import threading
import markdown2
import subprocess
import webbrowser
import http.server
import socketserver
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, simpledialog, filedialog, messagebox, scrolledtext
from functools import partial
from datetime import datetime

#Crypto 1.4.1

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes
#from dependencies.Crypto.Cipher import AES
#from dependencies.Crypto.Util.Padding import pad
#from dependencies.Crypto.Random import get_random_bytes

from PySide6.QtWidgets import QApplication, QMainWindow, QMenu, QMenuBar # QAction,
from PySide6 import QtWidgets, QtGui
from PySide6.QtWidgets import (QApplication, QMainWindow, QTextEdit, QVBoxLayout, QWidget,  QFileDialog, QLineEdit,QCalendarWidget)
from PySide6.QtWidgets import (QFontComboBox, QToolBar, QMessageBox, QSizePolicy, QLabel, QComboBox, QMenu, QPushButton, QListWidget)
from PySide6.QtGui import QFont, QSyntaxHighlighter, QIcon, QKeyEvent, QKeySequence, QColor, QPalette, QTextCursor, QTextCharFormat
from PySide6.QtCore import Qt, QRegularExpression, QPoint , QTimer, QDate
from PySide6 import QtWidgets, QtGui, QtCore

#  local file import
#from dependencies.emoji_data import categories
from dependencies.EmojiPicker import EmojiPicker
from dependencies.VarDataEncryptor import start_var_data_encryptor
from dependencies.markdown_highlighter import MarkdownHighlighter
from dependencies.HashPasswordAuthenticator import HashPasswdAuthenticator
from dependencies.GitSync import git_commands

class MagicMemoryMarkTextEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.http_server = None

    def increase_font_size(self):
        current_font = self.text_widget.currentFont()
        point_size = current_font.pointSize()
        current_font.setPointSize(point_size + 6)
        self.text_widget.setCurrentFont(current_font)

    def decrease_font_size(self):
        current_font = self.text_widget.currentFont()
        point_size = current_font.pointSize()
        current_font.setPointSize(point_size - 3)
        self.text_widget.setCurrentFont(current_font)

    def close_editor(self):
        self.close()

    def change_font_family(self, font):
        current_font = self.text_widget.currentFont()
        current_font.setFamily(font.family())
        self.text_widget.setCurrentFont(current_font)

    def close_emoji_picker(self):
        self.emoji_picker.hide()

    def handle_category_change(self, cat):
        self.change_emoji_category(cat)

    def init_ui(self):
        self.setWindowTitle("Cool In-Memory Text Editor")
        self.setGeometry(100, 100, 800, 600)

        # Set PeachPuff background color
        self.set_peachpuff_style()

        # Create the text widget
        self.text_widget = QTextEdit()
        self.text_widget.setFontPointSize(18)
        self.text_widget.setFont(QtGui.QFont("Noto Color Emoji", 18))
        # self.text_widget.setFont(QtGui.QFont("Noto", 18))
        self.save = False


        # Create the toolbar
        self.toolbar = QToolBar("Toolbar")
        self.toolbar.setStyleSheet("""
            QToolBar {
                background-color: peachpuff;
                border: 2px solid white;
                border-radius: 5px;
                padding: 5px;
            }

            QToolButton {
                background-color: #ff6b6b;
                color: white;
                border: none;
                padding: 5px;
                border-radius: 5px;
            }

            QToolButton:hover {
                border-radius: 10px;
                background-color: #3a1c71;
            }
        """)

        # Create actions for the toolbar and menu


        # Save Button
        save_button = QPushButton("Save")
        save_button.clicked.connect(self.saveNexit)
        save_button.setIcon(QIcon.fromTheme("application-exit"))
        self.toolbar.addWidget(save_button)



        open_button = QPushButton("Open")
        open_button.clicked.connect(self.open_file)
        self.toolbar.addWidget(open_button)
        #open_button.setStyleSheet("background-color: peachpuff; color: white; border: none; padding: 5px; border-radius: 5px;")
        open_button.setStyleSheet(self.toolbar.styleSheet())



        # Bold Button
        bold_button = QPushButton("Bold")
        bold_button.clicked.connect(self.toggle_bold)
        self.toolbar.addWidget(bold_button)
        bold_button.setIcon(QIcon.fromTheme("format-text-bold"))


        # Set the central widget and layout
        layout = QVBoxLayout()
        layout.addWidget(self.text_widget)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Bold Button
        bold_button = QPushButton("Bold")
        bold_button.clicked.connect(self.toggle_bold)
        self.toolbar.addWidget(bold_button)
        bold_button.setIcon(QIcon.fromTheme("format-text-bold"))

        # Markdown Preview Button
        preview_button = QPushButton("Markdown Preview")
        preview_button.clicked.connect(self.preview_markdown)
        self.toolbar.addWidget(preview_button)
        preview_button.setIcon(QIcon.fromTheme("text-html"))


        # Increase Font Size Button
        increase_font_button = QPushButton("+")
        increase_font_button.clicked.connect(self.increase_font_size)
        increase_font_button.setIcon(QIcon.fromTheme("format-font-size-less"))
        self.toolbar.addWidget(increase_font_button)

        # Decrease Font Size Button
        decrease_font_button = QPushButton("-")
        decrease_font_button.clicked.connect(self.decrease_font_size)
        decrease_font_button.setIcon(QIcon.fromTheme("format-font-size-less"))
        self.toolbar.addWidget(decrease_font_button)


        # Add a stretchable space
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.toolbar.addWidget(spacer)



        exit_button = QPushButton("Exit")
        exit_button.clicked.connect(self.Exit_without_save)
        self.toolbar.addWidget(exit_button)
        #exit_button.setStyleSheet("background-color: peachpuff; color: white; border: none; padding: 5px; border-radius: 5px;")
        exit_button.setStyleSheet(self.toolbar.styleSheet())



        self.emoji_picker = EmojiPicker(parent=self)
        self.emoji_picker.setGeometry(10, 50, 500, 400)
        self.emoji_picker.hide()


        # Emoji Button
        emoji_button = QPushButton("😊 Emoji")
        emoji_button.clicked.connect(self.toggle_emoji_picker)
        emoji_button.setIcon(QIcon.fromTheme("smile"))
        self.toolbar.addWidget(emoji_button)

        # Add the toolbar to the main window
        self.addToolBar(self.toolbar)


        self.category_button = QtWidgets.QComboBox(self)
        self.category_button.addItems(list(self.emoji_picker.categories.keys()))
        self.category_button.currentIndexChanged.connect(self.change_emoji_category)
        self.toolbar.addWidget(self.category_button)
        self.category_dropdown_visible = False
        self.close_button = QtWidgets.QPushButton("❌", self.emoji_picker)

        self.close_button.setGeometry(450, 5, 30, 30)
        self.close_button.setFont(QtGui.QFont("Arial", 18))
        self.close_button.clicked.connect(self.close_emoji_picker)

        # Add a stretchable space
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.toolbar.addWidget(spacer)

        # Change the Font Family
        self.font_family_combobox = QFontComboBox(self)
        self.font_family_combobox.currentFontChanged.connect(self.change_font_family)
        self.toolbar.addWidget(self.font_family_combobox)
        self.text_widget.setFontPointSize(18)

    def toggle_emoji_picker(self):
        if self.emoji_picker.isVisible():
            self.emoji_picker.hide()
        else:
            self.emoji_picker.show()

    def change_emoji_category(self, index):
        category = list(self.emoji_picker.categories.keys())[index]
        self.emoji_picker.current_category = category
        self.emoji_picker.init_ui()

    def set_peachpuff_style(self):
        peachpuff_color = QColor(255, 218, 185)
        palette = self.palette()
        palette.setColor(QPalette.Window, peachpuff_color)
        self.setPalette(palette)

    def toggle_bold(self):
        fmt = self.text_widget.currentCharFormat()
        fmt.setFontWeight(QFont.Bold if fmt.fontWeight() == QFont.Normal else QFont.Normal)
        self.text_widget.mergeCurrentCharFormat(fmt)

    def open_file(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Text Files (*.txt);;All Files (*)", options=options)

        if file_name:
            try:
                with open(file_name, "r") as file:
                    self.text_widget.setPlainText(file.read())
            except Exception as e:
                print(f"Error opening file: {str(e)}")

    def preview_markdown(self):
        reply = QMessageBox.question(self, "Warning", "Your note will be served on a local HTTP server. Are you sure you want to proceed?", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            markdown_text = self.text_widget.toPlainText()
            html_content = markdown2.markdown(markdown_text)

            server_thread = threading.Thread(target=self.serve_html_content, args=(html_content,))
            server_thread.daemon = True
            server_thread.start()
        else:
            pass
    def serve_html_content(self, html_content):
        class InMemoryRequestHandler(http.server.SimpleHTTPRequestHandler):
            def do_GET(self):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.send_header('Content-length', len(html_content))
                self.end_headers()
                self.wfile.write(html_content.encode('utf-8'))

        with socketserver.TCPServer(("localhost", 0), InMemoryRequestHandler) as httpd:
            self.http_server = httpd
            port = httpd.server_address[1]
            url = f"http://localhost:{port}/index.html"
            webbrowser.open(url)
            httpd.serve_forever()

    def var_to_editor(self, content):
        self.text_widget.setPlainText(content)

    def save_text(self):  # forward text
        self.close()
        text = self.text_widget.toPlainText()
        return text

    def saveNexit(self):
        reply = QMessageBox.question(self, "Save Confirmation", "Are you sure you want to Save?", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.save = True
            self.close()

    def Exit_without_save(self):
        reply = QMessageBox.question(self, "Exit Confirmation", "Are you sure you want to Exit without save?", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.save = False
            self.close()

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
            decrypt_data = start_var_data_encryptor("dec", binary_data, passwd)
            p = subprocess.Popen(["less"], stdin=subprocess.PIPE)
            p.communicate(input=decrypt_data.encode())

            file_to_delete = ".tmp"
            secure_delete_file(file_to_delete)

        else:
            print("Invalid choice. Please try again.")

    except ValueError:
        print("Invalid input. Please enter a number.")


def start_magic_memory_mark_editor():
    global app
    if not app:
        app = QApplication(sys.argv) #  Create the QApplication instance
    editor = MagicMemoryMarkTextEditor()
    editor.show()
    app.exec_()
    app.quit()
    print(editor.save)
    if editor.save:    
        return editor




def create_entry(passwd):
    now = datetime.now()
    entry_date = now.strftime("%Y-%m-%d")
    entry_time = now.strftime("%H:%M:%S")
    entry_datetime = f"{entry_date} \n{entry_time}\n"  # new one
    note = start_magic_memory_mark_editor()
    saved_text = note.save_text()

    join_date_and_note = f"\n{entry_datetime}\n{saved_text}"

    file_name_input = simpledialog.askstring("File Name", "Enter a file name for the diary entry:")

    if file_name_input:
        print("File name entered:", file_name_input)
    else: 
        file_name_input = simpledialog.askstring("File Name", "Enter a file name for the diary entry:")
    sanitized_file_name = "".join(c if c.isalnum() else "-" for c in file_name_input.lower())
    filename = f"{entry_date}-{sanitized_file_name}.enc.GitDiarySync"
    write_path = (".enc.GitDiarySync/" + now.strftime("%b-%Y") + "/" + now.strftime("%d"))
    if not os.path.exists(write_path):
        os.makedirs(write_path)

    entry_file_path = os.path.join(write_path, filename)
    enc_note = start_var_data_encryptor("enc", join_date_and_note, passwd)

    with open(entry_file_path, "w") as file:  # error
        file.write(enc_note)
    print(f"Diary entry saved to {entry_file_path}")


def get_md_files_recursively(directory="."):
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
    for file_path in file_dict.values(): # split date
        date = file_path.split('/')[-1][:10]
        dates.append(date)

    for file in md_files:
        #list_widget.addItem(file)  # Get with Full path
        filename = file.split("/")[-1] # filename 
        if file.endswith('.enc.GitDiarySync'):
            filtered_files.append(filename) # ['filename']
            list_widget.addItem(filename)  # Add only the file name (bin)
            file_dict[filename] = file #file is full path

            #lets lighlight whatever date found 
            date = filename.split('/')[-1][:10]  # "2023-11-03"
            year, month, day = map(int, date.split('-'))
            highlighted_dates.append(QDate(year, month, day))

    #print("md_files:", md_files)
    #print("filtered_files:", filtered_files)
    #print("File Dictionary:", file_dict)

    layout.addWidget(list_widget)
	
    def print_selected_date(selected_date):

        year = selected_date.year()
        month = selected_date.month()
        day = selected_date.day()
        filenamer = f"{year}-{month:02d}-{day:02d}"
        filenamestr = str(filenamer)

        list_widget.clear()
        for file in md_files:
            #list_widget.addItem(file)  # Get with Full path
            filename = file.split("/")[-1] # filename 
            if filename.endswith('.enc.GitDiarySync') and filename.startswith(filenamestr):
                filtered_files.append(filename) # ['filename']
                list_widget.addItem(filename)  # Add only the file name (bin)
                file_dict[filename] = file #file is full path
                
                #lets lighlight whatever date found 
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
        selected_file_name = list_widget.selectedItems()[0].text()
        selected_file = file_dict.get(selected_file_name, None)
        if selected_file is None:
            QMessageBox.warning(choose_root, "Warning", "File not found.")
        else:
            choose_root.close()

    select_button.clicked.connect(on_select)
    choose_root.setLayout(layout)

    choose_root.show()
    app.exec_()
    
    print(selected_file)
    return selected_file
    
def edit_n_view_mode(passwd, edit_mode):
    md_files = get_md_files_recursively()
    if not md_files:

        global app
        if not app:
            app = QApplication(sys.argv)

        message_box = QMessageBox()
        message_box.setWindowTitle("Information")
        message_box.setText("No .enc.GitDiarySync files found in the current directory or its subdirectories. Add a Diary page")
        message_box.setIcon(QMessageBox.Information)
        message_box.exec_()
        #print("No .enc.GitDiarySync files found in the current directory or its subdirectories.")
        return

    selected_file = choose_file(md_files)
    if selected_file:
        temp_decrypted_file = ".tmp"
        copy_file(selected_file, temp_decrypted_file)
        with open(temp_decrypted_file, "r") as file:
            bytes_data = file.read()
        bytes_data_to_str = start_var_data_encryptor("dec", bytes_data, passwd)
        #global app
        if not app:
            app = QApplication(sys.argv)
        if not edit_mode:  # view_mode
            read_only_warning = QMessageBox()
            read_only_warning.setWindowTitle("Read-Only Mode")
            read_only_warning.setIcon(QMessageBox.Warning)
            read_only_warning.setText(
                "Note: You have opened this file in read-only mode. Any attempt to save will not be successful.")
            read_only_warning.exec_()

        filetoeditor = MagicMemoryMarkTextEditor()
        filetoeditor.var_to_editor(bytes_data_to_str)
        filetoeditor.show()
        app.exec_()
        app.quit() # !?!?
        print(filetoeditor.save)
        if filetoeditor.save:    
            if edit_mode:
                dec_note = filetoeditor
                the_saved_text = dec_note.save_text()
                last_modified_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                last_modified_date_string = f"\n\nLast modified: {last_modified_date}\n"
                total_note = f"{the_saved_text} {last_modified_date_string}"
                enc_note = start_var_data_encryptor("enc", total_note, passwd)

                with open(temp_decrypted_file, "w") as file:
                    file.write(enc_note)
                copy_file(temp_decrypted_file, selected_file)

        secure_delete_file(temp_decrypted_file)



def commit_to_git():
    #from dependencies.GitSync import git_commands
    git_commands()
    
def input_passwd(FirstTime):
    global app
    if not app:
        app = QApplication(sys.argv) #  Create the QApplication instance
        print("Create the QApplication instance")
    if app:
        app = QApplication.instance() # retrieves the instance
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

    entered_passwd = "" 

    def on_button_click():
        passwd = passwd_entry.text()
        window.close()
        if FirstTime:
            hash_note = HashPasswdAuthenticator("BcryptEnc", passwd , "NoHash")
            print(hash_note)
            with open("enc.GitDiarySync", 'w') as file:
                file.write(hash_note)
            msg_box = QMessageBox()
            msg_box.setText("Setup completed. Start the program again.")
            msg_box.exec_()
            sys.exit()
        else:
            pass
            

    check_button.clicked.connect(on_button_click)
    passwd_entry.returnPressed.connect(on_button_click)
    window.show()
    app.exec_()

    passwd = passwd_entry.text()
    return passwd_entry.text()


def input_pass_now_first_time(wel_root):

    wel_root.hide()
    #wel_root.close()
    #app.quit()
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
    sys.exit(app.exec_())

def close_window(window):
    window.destroy()


def main():
    global app
    app = None
    #if not app:
    #    app = QApplication(sys.argv)
    if not os.path.exists("enc.GitDiarySync"):
        first_time_welcome_screen()
    print("\n\nWelcome to the Git-backed-diary application!\n")
    #global password
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
        success_message.exec_()

    else:

        error_message = QMessageBox()
        error_message.setIcon(QMessageBox.Critical)
        error_message.setWindowTitle("Password Error")
        error_message.setText("Your password appears to be incorrect.\n"
                            "If you wish to reset it, delete the 'enc.GitDiarySync' file and run this program again to create a new one.\n"
                            "Please note that you will lose access to your old notes if you set a new password.\n"
                            "However, if you can recall your old correct password, you can regain access to your files.\n"
                            "Tips: If you remove the 'enc.GitDiarySync' and set your old password again, you can access your old content.")
        error_message.exec_()
        sys.exit()
    while True:
        secure_delete_file(".tmp")

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
                 #view mode
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
        root.wm_attributes("-type", "splash")  # WM
        root.wm_attributes("-topmost", 1)  # WM

        style = ttk.Style() 
        style.theme_use('clam')
        
        style.configure('TFrame', background='#ffdab9') # corner part
        root.configure(background='#ffdab9') #background
        style.configure('.', background='#ffe2c6') #button

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
