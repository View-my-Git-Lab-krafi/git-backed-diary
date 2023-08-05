import os
import subprocess
from datetime import datetime
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import hashlib
import random
##############################################

#pip install PySide2 markdown2
import sys
import webbrowser
import io
import markdown2
import http.server
import socketserver
import threading

from PySide2.QtWidgets import QApplication, QMainWindow, QTextEdit, QVBoxLayout, QWidget, QAction, QFileDialog, QFontComboBox, QToolBar, QMessageBox, QSizePolicy

from PySide2.QtGui import QKeySequence, QColor, QPalette, QTextCursor, QTextCharFormat, QFont, QSyntaxHighlighter, QIcon, QKeyEvent

from PySide2.QtCore import Qt, QRegularExpression
from PySide2.QtGui import QTextCharFormat

import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
from tkinter import filedialog, messagebox
from tkinter import scrolledtext
import hashlib
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad

#app = QApplication(sys.argv)

class Magic_Memory_Mark_TextEditor(QMainWindow):
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
##############
    def close_editor(self):
        self.close()
##############
    def change_font_family(self, font):
        current_font = self.text_widget.currentFont()
        current_font.setFamily(font.family())
        self.text_widget.setCurrentFont(current_font)

    def init_ui(self):
        self.setWindowTitle("Cool In-Memory Text Editor")
        self.setGeometry(100, 100, 800, 600)

        # Set PeachPuff background color
        self.set_peachpuff_style()

        # Create the text widget
        self.text_widget = QTextEdit()
        self.text_widget.setFontPointSize(18)

        # Create actions for the toolbar and menu
        self.save_action = QAction(QIcon.fromTheme("document-save"), "Save", self)
        self.save_action.triggered.connect(self.save_text)
        self.save_action.setShortcut(QKeySequence.Save)
        self.save_action.setShortcut(QKeySequence(Qt.CTRL + Qt.Key_S))

        #self.save_action.setShortcut(QKeySequence.Save)
        self.save_action.triggered.connect(self.confirm_save_exit)
        self.save_action.setShortcut(QKeySequence.Quit)
        #self.toolbar.addAction(self.exit_action)

        self.open_action = QAction(QIcon.fromTheme("document-open"), "Open", self)
        self.open_action.triggered.connect(self.open_file)
        self.open_action.setShortcut(QKeySequence.Open)

        # Create the toolbar
        self.toolbar = QToolBar("Toolbar")
        self.toolbar.setStyleSheet(
    """
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
    """
)
        self.toolbar.addAction(self.save_action)
        self.toolbar.addAction(self.open_action)

        # Change the Font Family
        self.font_family_combobox = QFontComboBox(self)
        self.font_family_combobox.currentFontChanged.connect(self.change_font_family)
        self.toolbar.addWidget(self.font_family_combobox)
        self.text_widget.setFontPointSize(18)

        # Bold Button
        self.bold_action = QAction(QIcon.fromTheme("format-text-bold"), "Bold", self)
        self.bold_action.triggered.connect(self.toggle_bold)
        self.bold_action.setShortcut(QKeySequence.Bold)
        self.toolbar.addAction(self.bold_action)
        self.addToolBar(self.toolbar)

        # Set the central widget and layout
        layout = QVBoxLayout()
        layout.addWidget(self.text_widget)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Markdown Preview Button
        self.preview_action = QAction(QIcon.fromTheme("text-html"), "Markdown Preview", self)
        self.preview_action.triggered.connect(self.preview_markdown)
        self.toolbar.addAction(self.preview_action)
        self.addToolBar(self.toolbar)


        # Markdown syntax highlighting
        self.highlighter = MarkdownHighlighter(self.text_widget.document())


        # Increase Font Size Button
        self.increase_font_action = QAction(QIcon.fromTheme("format-font-size-more"), "+", self)
        self.increase_font_action.triggered.connect(self.increase_font_size)
        self.increase_font_action.setShortcut(QKeySequence("Ctrl++"))  # Set a keyboard shortcut (Ctrl++)
        self.toolbar.addAction(self.increase_font_action)

        # Decrease Font Size Button
        self.decrease_font_action = QAction(QIcon.fromTheme("format-font-size-less"), "-", self)
        self.decrease_font_action.triggered.connect(self.decrease_font_size)
        self.decrease_font_action.setShortcut(QKeySequence("Ctrl+-"))  # Set a keyboard shortcut (Ctrl+-)
        self.toolbar.addAction(self.decrease_font_action)

        # Add a stretchable space
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.toolbar.addWidget(spacer)

        # Exit Button
        self.exit_action = QAction(QIcon.fromTheme("application-exit"), "Exit", self)
        self.exit_action.triggered.connect(self.confirm_exit)
        self.exit_action.setShortcut(QKeySequence.Quit)
        self.toolbar.addAction(self.exit_action)



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
        reply = tk.messagebox.askyesno("Warning", "Your note will be served on a local HTTP server. Are you sure you want to proceed?")
        if reply:
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
                self.send_header('Content-type', 'text/html')#
                self.send_header('Content-length', len(html_content))
                self.end_headers()
                self.wfile.write(html_content.encode('utf-8'))

        with socketserver.TCPServer(("localhost", 0), InMemoryRequestHandler) as httpd:
            self.http_server = httpd
            port = httpd.server_address[1]
            url = f"http://localhost:{port}/index.html"#
            webbrowser.open(url)
            httpd.serve_forever()
    def var_to_editor(self, content):
        self.text_widget.setPlainText(content)
    def save_text(self):
        global text
        text = self.text_widget.toPlainText()
        #print("Text in memory:")
        #print(text)
        return text

    def confirm_exit(self):
        reply = tk.messagebox.askyesno("Exit Confirmation", "Are you sure you want to exit?")
        if reply:
            self.close()
    def confirm_save_exit(self):
        reply = tk.messagebox.askyesno("Exit Confirmation", "Are you sure you want to return to program? \n Press 'no' if you still want to edit.")
        if reply:
            self.close()

########################################################################################################3
class MarkdownHighlighter(QSyntaxHighlighter):
    def __init__(self, parent):
        super().__init__(parent)
        self.highlighting_rules = []

        # Heading
        heading_format = QTextCharFormat()
        heading_format.setFontWeight(QFont.Bold)
        heading_format.setForeground(Qt.darkMagenta)
        self.highlighting_rules.append((QRegularExpression(r'^#{1,6}\s.*$'), heading_format))

        # Italic
        italic_format = QTextCharFormat()
        italic_format.setFontItalic(True)
        italic_format.setForeground(Qt.darkGreen)
        self.highlighting_rules.append((QRegularExpression(r'_(.*?)_'), italic_format))
        self.highlighting_rules.append((QRegularExpression(r'\*(.*?)\*'), italic_format))

        # Bold
        bold_format = QTextCharFormat()
        bold_format.setFontWeight(QFont.Bold)
        bold_format.setForeground(Qt.darkRed)
        self.highlighting_rules.append((QRegularExpression(r'__(.*?)__'), bold_format))
        self.highlighting_rules.append((QRegularExpression(r'\*\*(.*?)\*\*'), bold_format))

        # Strikethrough
        strikethrough_format = QTextCharFormat()
        strikethrough_format.setFontStrikeOut(True)
        strikethrough_format.setForeground(Qt.darkGray)
        self.highlighting_rules.append((QRegularExpression(r'~~(.*?)~~'), strikethrough_format))

        # Code Block
        code_block_format = QTextCharFormat()
        code_block_format.setFontFamily("Courier New")
        code_block_format.setBackground(Qt.lightGray)
        self.highlighting_rules.append((QRegularExpression(r'```[\s\S]*?```'), code_block_format))

        # Inline Code
        inline_code_format = QTextCharFormat()
        inline_code_format.setFontFamily("Courier New")
        inline_code_format.setForeground(Qt.darkBlue)
        self.highlighting_rules.append((QRegularExpression(r'`.*?`'), inline_code_format))

        # Links
        link_format = QTextCharFormat()
        link_format.setForeground(Qt.blue)
        self.highlighting_rules.append((QRegularExpression(r'\[.*?\]\(.*?\)'), link_format))

        # Lists
        list_format = QTextCharFormat()
        list_format.setForeground(Qt.darkCyan)
        self.highlighting_rules.append((QRegularExpression(r'^\s*[-*+]\s.*$'), list_format))

        # Ordered List
        ordered_list_format = QTextCharFormat()
        ordered_list_format.setForeground(Qt.darkCyan)
        self.highlighting_rules.append((QRegularExpression(r'^\s*\d+\.\s.*$'), ordered_list_format))


        # Blockquotes
        quote_format = QTextCharFormat()
        quote_format.setForeground(Qt.darkGreen)
        self.highlighting_rules.append((QRegularExpression(r'^\s*>.*$'), quote_format))

        # Horizontal Rule
        hr_format = QTextCharFormat()
        hr_format.setForeground(Qt.darkGray)
        self.highlighting_rules.append((QRegularExpression(r'^\s*[-*_]{3,}\s*$'), hr_format))


        # Table
        table_format = QTextCharFormat()
        table_format.setForeground(Qt.darkYellow)
        self.highlighting_rules.append((QRegularExpression(r'^\s*(\|.*\|)+\s*$'), table_format))

        # Footnote
        footnote_format = QTextCharFormat()
        footnote_format.setForeground(Qt.darkRed)
        self.highlighting_rules.append((QRegularExpression(r'\[\^\S+\]'), footnote_format))

        # Definition List
        definition_format = QTextCharFormat()
        definition_format.setForeground(Qt.darkMagenta)
        self.highlighting_rules.append((QRegularExpression(r'^\s*.*:\s.*$'), definition_format))

        # Emoji
        emoji_format = QTextCharFormat()
        emoji_format.setForeground(Qt.darkCyan)
        self.highlighting_rules.append((QRegularExpression(r':[a-zA-Z0-9_+-]+:'), emoji_format))

        # Highlight
        highlight_format = QTextCharFormat()
        highlight_format.setBackground(Qt.yellow)
        self.highlighting_rules.append((QRegularExpression(r'==.*?=='), highlight_format))

        # Task Lists
        task_list_format = QTextCharFormat()
        task_list_format.setForeground(Qt.darkCyan)
        self.highlighting_rules.append((QRegularExpression(r'^\s*\[([ xX])\]\s.*$'), task_list_format))

        # Strikethrough (Tilde Syntax)
        tilde_strikethrough_format = QTextCharFormat()
        tilde_strikethrough_format.setFontStrikeOut(True)
        tilde_strikethrough_format.setForeground(Qt.darkGray)
        self.highlighting_rules.append((QRegularExpression(r'~(.*?)~'), tilde_strikethrough_format))

        # Autolinks
        autolink_format = QTextCharFormat()
        autolink_format.setForeground(Qt.blue)
        self.highlighting_rules.append((QRegularExpression(r'<(?:https?://[^>]+)>'), autolink_format))

        # Mentions or References
        mention_format = QTextCharFormat()
        mention_format.setForeground(Qt.darkGreen)
        self.highlighting_rules.append((QRegularExpression(r'@[\w.-]+'), mention_format))

        # Footnote Links in Text
        footnote_link_format = QTextCharFormat()
        footnote_link_format.setForeground(Qt.darkRed)
        self.highlighting_rules.append((QRegularExpression(r'\[\^\S+\]'), footnote_link_format))


    def highlightBlock(self, text):
        for pattern, format in self.highlighting_rules:
            expression = QRegularExpression(pattern)
            it = expression.globalMatch(text)
            while it.hasNext():
                match = it.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), format)

#################################################################################


def secure_delete_file(filename, passes=9):
    try:
        with open(filename, 'rb+') as f:
            file_size = os.path.getsize(filename)
            for _ in range(passes):
                f.seek(0)
                f.write(os.urandom(file_size))
        os.remove(filename)
        #print(f"File '{filename}' securely deleted.")
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



def view_mode_less():
    md_files = get_md_files_recursively()

    if not md_files:
        print("No .enc files found in the current directory or its subdirectories.")
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
            ###
            binary_data = None

            with open(destination_filename, 'rb') as binary_file:
                binary_data = binary_file.read()
            decrypt_data = decrypt_var_data(binary_data, password)
            p = subprocess.Popen(["less"], stdin=subprocess.PIPE)
            p.communicate(input=decrypt_data.encode())

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

def encrypt_var_data(data, password):
    block_size = 16
    key = hashlib.sha256(password.encode()).digest()
    iv = get_random_bytes(block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)

    # string to bytes
    plaintext = data.encode()

    # Pad the plaintext
    padded_plaintext = pad(plaintext, block_size)

    # Encrypt the data
    encrypted_data = cipher.encrypt(padded_plaintext)

    # Return the IV and encrypted data as bytes
    return b'ENCRYPTED:' + iv + encrypted_data


def decrypt_var_data(encrypted_data, password):
    block_size = 16
    key = hashlib.sha256(password.encode()).digest()

    if not encrypted_data.startswith(b'ENCRYPTED:'):
        raise ValueError("The data is not encrypted with this program.")

    encrypted_data = encrypted_data[len(b'ENCRYPTED:'):]
    iv = encrypted_data[:block_size]
    ciphertext = encrypted_data[block_size:]
    cipher = AES.new(key, AES.MODE_CBC, iv)

    #decrypted_data = unpad(cipher.decrypt(ciphertext), block_size)
    decrypted_data = unpad(cipher.decrypt(ciphertext))
    # Convert the bytes to string before returning
    return decrypted_data.decode()
#################################################################
def start_magic_memory_mark_editor():
    global app
    #app = QApplication(sys.argv)
    if not app:
        app = QApplication(sys.argv)
    editor = Magic_Memory_Mark_TextEditor()
    editor.show()
    app.exec_()
    app.quit()
    #app = None
    return editor

def create_entry():
    now = datetime.now()
    entry_date = now.strftime("%Y-%m-%d")
    entry_time = now.strftime("%H:%M:%S")
    entry_datetime = f"{entry_date} \n{entry_time}\n" # new one
    (f"Date: {entry_date}\nTime: {entry_time}\n\n".encode())
    note = start_magic_memory_mark_editor()
    saved_text = note.save_text()
    #print(saved_text)
    #print(type(saved_text)) # str

    join_date_and_note = f"{entry_datetime}\n{saved_text}"
    #print(saved_text)

    rootz = tk.Tk()
    rootz.withdraw()  # Hide the main window

    file_name_input = simpledialog.askstring("File Name", "Enter a file name for the diary entry:")

    if file_name_input:
        print("File name entered:", file_name_input)
    else:
        print("No file name entered.")
    sanitized_file_name = "".join(c if c.isalnum() else "-" for c in file_name_input.lower())
    filename = f"{entry_date}-{sanitized_file_name}.enc"
    month_year_dir = now.strftime("%b-%Y")
    if not os.path.exists(month_year_dir):
        os.makedirs(month_year_dir)
    entry_file_path = os.path.join(month_year_dir, filename)
    #enc_note = encrypt_var_data(saved_text, password)

    enc_note = encrypt_var_data(join_date_and_note, password)  # Encode the string before encryption
    with open(entry_file_path, "wb") as file: # error
        #file.write(f"Date: {entry_date}\nTime: {entry_time}\n\n".encode())
        file.write(enc_note)
    print(f"Diary entry saved to {entry_file_path}")



def editmode_magic_memory_mark_editor(bytes_data_to_str):
    global app
    if not app:
        app = QApplication(sys.argv)
    editor = Magic_Memory_Mark_TextEditor()
    editor.var_to_editor(bytes_data_to_str)
    editor.show()
    app.exec_()
    return editor


def get_md_files_recursively(directory="."):
    md_files = []
    for root, _, files in os.walk(directory):
        md_files.extend([os.path.join(root, file) for file in files if file.endswith(".enc")])
    return md_files

def choose_file(md_files):
    choose_root = tk.Tk()
    choose_root.title("Select File")
    choose_root.geometry("700x700")
    scrollbar = tk.Scrollbar(choose_root)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    choose_root.wm_attributes("-type", "splash")  # WM
    choose_root.wm_attributes("-topmost", 1)  # WM

    listbox = tk.Listbox(choose_root, width=80, height=30, yscrollcommand=scrollbar.set)  # Adjust width and height as needed

    listbox.pack()

    scrollbar.config(command=listbox.yview)

    for idx, file in enumerate(md_files, start=1):
        listbox.insert(idx, file)

    tk.Button(choose_root, text="Select", command=choose_root.quit).pack()

    choose_root.mainloop()

    choice = listbox.curselection()

    if not choice:
        choose_root.destroy()
        return None

    selected_file = md_files[choice[0]]
    choose_root.destroy()
    return selected_file


def edit_mode():
    md_files = get_md_files_recursively()

    if not md_files:
        print("No .enc files found in the current directory or its subdirectories.")
        return
    else:

        selected_file = choose_file(md_files)
        if selected_file:
            temp_decrypted_file = ".tmp_decrypted.txt"
            copy_file(selected_file, temp_decrypted_file)
            # Other code to continue with file editing


            with open(temp_decrypted_file, "rb") as file:
                bytes_data = file.read()
            bytes_data_to_str = decrypt_var_data(bytes_data, password)

            #print(bytes_data_to_str) # read file

            the_note = editmode_magic_memory_mark_editor(bytes_data_to_str)
            the_saved_text = the_note.save_text()

            #print(the_saved_text)

            now = datetime.now()
            last_modified_date = now.strftime("%Y-%m-%d %H:%M:%S")
            total_string = f"\n\nLast modified: {last_modified_date}\n"

            total_note = f"{the_saved_text} {total_string}"


            #print(total_note)
            enc_note = encrypt_var_data(total_note, password)
            #print(enc_note)

            with open(temp_decrypted_file, "wb") as file: # error
            #file.write(f"Date: {entry_date}\nTime: {entry_time}\n\n".encode())
                file.write(enc_note)
            print(f"Diary entry saved to {temp_decrypted_file}")
            copy_file(temp_decrypted_file, selected_file)
            secure_delete_file(temp_decrypted_file)
            print(f"File '{selected_file}' edited and saved.")

def view_mode_gui():
    md_files = get_md_files_recursively()

    if not md_files:
        print("No .enc files found in the current directory or its subdirectories.")
        return
    else:
        selected_file = choose_file(md_files)
        if selected_file:
            source_filename = selected_file
            destination_filename = '.tmp.txt'
            copy_file(source_filename, destination_filename)
            with open(destination_filename, "rb") as file:
                bytes_data = file.read()
            bytes_data_to_str = decrypt_var_data(bytes_data, password)
            #print(bytes_data_to_str)

            root = tk.Tk()
            root.title("Read-Only Warning")
            root.wm_attributes("-type", "splash")  # WM
            root.wm_attributes("-topmost", 1)  # WM
            root.geometry("400x150")
            warning_message = "Note: You have opened this file in read-only mode. Any attempt to save will not be successful."
            messagebox.showwarning("Read-Only Mode", warning_message)
            root.destroy()
            global app
            #app = QApplication(sys.argv)
            if not app:
                app = QApplication(sys.argv)
            editor = Magic_Memory_Mark_TextEditor()
            editor.var_to_editor(bytes_data_to_str)
            editor.show()
            app.exec_()
            #return editor

            file_to_delete = ".tmp.txt"
            secure_delete_file(file_to_delete)



def commit_to_git():
    commit_message = input("Enter a commit message for Git:\n")
    subprocess.run(["git", "add", "*.enc"])
    subprocess.run(["git", "commit", "-m", commit_message])
#    git config --global credential.helper store

    subprocess.run(["git", "config", "--global", "credential.helper", "store"])
    subprocess.run(["git", "push"])

    print("Changes committed and pushed to Git repository.")
def input_password_using_tkinter():
    roots = tk.Tk()
    roots.title("Personal Diary")
    roots.wm_attributes("-type", "splash")  # WM
    roots.wm_attributes("-topmost", 1)  # WM

    #roots.attributes("-topmost", True)
    roots.geometry("400x200")
    roots.configure(bg="#f2f2f2")

    custom_font = ("Arial", 14, "bold")

    title_label = tk.Label(roots, text="Welcome to Personal Diary", font=("Arial", 18, "bold"), fg="blue", bg="#f2f2f2")
    title_label.pack(pady=10)

    password_label = tk.Label(roots, text="Enter Password:", font=custom_font, fg="black", bg="#f2f2f2")
    password_label.pack()

    password_entry = tk.Entry(roots, show="*", font=custom_font)
    password_entry.pack(pady=10)

    check_button = tk.Button(roots, text="Unlock Diary", font=custom_font, bg="green", fg="white", command=roots.quit)
    check_button.pack(pady=10)
    password_entry.focus_set()

    roots.bind('<Return>', lambda event: check_button.invoke())

    roots.mainloop()
    entered_password = password_entry.get()
    close_window(roots)
    return entered_password

def stop_code():
    exit()

def input_pass_now(wel_root):
    wel_root.destroy()
    passwd = input_password_using_tkinter()
    lock = ("\n<================================================>\n[========Your password is correct. Great!========]\n<================================================>\n\n")
    enc_note = encrypt_var_data(lock, passwd)


    with open(".passwd.txt", 'wb') as file:
        file.write(enc_note)


    wel_roott = tk.Tk()
    wel_roott.title("Git-backed-diary Password Verification")
    wel_roott.wm_attributes("-type", "splash")  # WM
    wel_roott.wm_attributes("-topmost", 1)  # WM

    welcome_label = tk.Label(wel_roott, text="Now everytime you open the program you should able to see, 'Your password is correct. Great!' this message  \n that means your passwd is correct \n Now start the program again! \n thanks")
    welcome_label.pack()

    start_button = tk.Button(wel_roott, text="close the program", command=stop_code)
    start_button.pack()

    wel_roott.mainloop()


def first_time_welcome_screen():

    wel_root = tk.Tk()
    wel_root.title("Git-backed-diary Password Verification")
    wel_root.wm_attributes("-type", "splash")  # WM
    wel_root.wm_attributes("-topmost", 1)  # WM

    welcome_label = tk.Label(wel_root, text="Welcome to the Git-backed-diary application! \n \n For security reasons, please set a strong password for your diary. \n Keep in mind that once set, the password cannot be recovered, so make sure to remember it. \n If you ever wish to reset the password, delete the 'passwd.txt' file and create a new one. \n Keep your password safe and secure as it will protect your diary entries from unauthorized access.\n\n Please enter your password")
    welcome_label.pack()


    start_button = tk.Button(wel_root, text="ready for input password", command=lambda: input_pass_now(wel_root))
    start_button.pack()

    wel_root.mainloop()


    #print("Now everytime you open the program you should able to see, 'Your password is correct. Great!' this message  \n that means your passwd is correct")
    #print("Now start the program again")


def close_window(window):
    window.destroy()


def main():

    if not os.path.exists(".passwd.txt"):
        first_time_welcome_screen()
    print("\n\nWelcome to the Git-backed-diary application!\n")
    global password

    password = input_password_using_tkinter()
    print("\n")
    copy_file(".passwd.txt", ".passwd_test.txt")
    decrypt_file('.passwd_test.txt', password)

    try:
        with open(".passwd_test.txt", 'r', encoding='utf-8') as file:
            content = ""
            for line in file:
                content += line


        def close_window():
            pass_suc.destroy()

        pass_suc = tk.Tk()
        pass_suc.title("File Content")
        #pass_suc.attributes("-topmost", True)
        pass_suc.wm_attributes("-type", "splash")  # WM
        pass_suc.wm_attributes("-topmost", 1)  # WM
        text_widget = tk.Text(pass_suc)
        text_widget.insert(tk.END, content)
        text_widget.pack()
        ok_button = tk.Button(pass_suc, text="OK", command=close_window)
        ok_button.focus_set()
        pass_suc.bind('<Return>', lambda event=None: ok_button.invoke())
        ok_button.pack()
        pass_suc.mainloop()

    except UnicodeDecodeError:
        messagebox.showerror("Password Error", "Your password looks incorrect because the file contains non-text (binary) data.\n"
                                          "If you want to reset remove .passwd_test.txt and .passwd.txt, "
                                          "also remember that you will become unable to access your old notes.\n"
                                          "If you are able to set your old correct password you will able to access your file again")
        exit()


    while True:

        file_to_delete = ".tmp.txt"
        secure_delete_file(file_to_delete)
        def handle_choice(event):
            choice = event.char
            if choice in ["1", "2", "3", "4", "5", "6"]:
                handle_button_click(choice)

        def handle_button_click(choice):
            if choice == "1":
                create_entry()
            elif choice == "2":
                commit_to_git()
            elif choice == "3":
                edit_mode()
            elif choice == "4":
                view_mode_gui()
            elif choice == "5":
                view_mode_less()
            elif choice == "6":
                root.quit()
                exit()
            else:
                output_label.config(text="Invalid choice. Please try again.")

        root = tk.Tk()
        root.title("Menu")
        root.wm_attributes("-type", "splash")  # WM
        root.wm_attributes("-topmost", 1)  # WM

        prompt_label = tk.Label(root, text="Press a number key (1/2/3/4/5/6):")
        prompt_label.pack()
        output_label = tk.Label(root, text="")
        output_label.pack()

        root.bind("<Key>", handle_choice)

        button_frame = tk.Frame(root)
        button_frame.pack()

        button_labels = {
            "1": "Create Entry",
            "2": "Commit to Git",
            "3": "Edit Mode",
            "4": "View Mode (GUI)",
            "5": "View Mode (Less)",
            "6": "Quit"
}


        for i in range(1, 7):
            button = tk.Button(button_frame, text=str(i) + " - " + button_labels[str(i)], command=lambda i=i: handle_button_click(str(i)))
            button.pack(side="top")

        root.mainloop()

if __name__ == "__main__":
    global app
    app = None
    main()
