# pip install markdown2 pycryptodome PySide2
import os
import json
import platform
import markdown2


from PySide6 import QtWidgets, QtGui
from PySide6.QtWidgets import QMainWindow, QTextEdit, QVBoxLayout, QWidget,  QFileDialog
from PySide6.QtWidgets import QFontComboBox, QToolBar, QMessageBox, QSizePolicy,QPushButton
from PySide6.QtGui import QFont, QIcon, QColor, QPalette
#  local file import
from dependencies.file_manipulation_utils import remove_files_with_extensions
from dependencies.record import RecorderGUI
from dependencies.AudioPlayer import AudioWidget

from dependencies.EmojiPicker import EmojiPicker
'''
from PySide6 import QtCore
from PySide6.QtWidgets import  QApplication,  QLineEdit,QCalendarWidget
from PySide6.QtWidgets import  QLabel, QComboBox, QMenu,  QListWidget
from PySide6.QtGui import QSyntaxHighlighter,  QKeyEvent, QKeySequence, QTextCursor, QTextCharFormat
from PySide6.QtCore import Qt, QRegularExpression, QPoint , QTimer, QDate
from PySide6.QtWidgets import QInputDialog
from PySide6.QtCore import QObject, Signal, QBuffer
#  local file import
#from dependencies.emoji_data import categories
from dependencies.VarDataEncryptor import start_var_data_encryptor
from dependencies.FileEncryptor import start_FileEncryptor
from dependencies.markdown_highlighter import MarkdownHighlighter
from dependencies.HashPasswordAuthenticator import HashPasswdAuthenticator
from dependencies.GitSync import git_commands
from dependencies.file_manipulation_utils import (
    secure_delete_file, 
    remove_files_with_extensions , secure_delete_file, 
    copy_file, copy_file_to_directoryand_rename_file,
    convert_to_webp, copy_file_to_directoryand_rename_file
)
'''


class MagicMemoryMarkTextEditor(QMainWindow):
    def __init__(self,passwd,filepath):
        super().__init__()

        self.audio_widgets = [] 
        self.init_ui(passwd,filepath) #?


    def increase_font_size(self):
        current_font = self.text_widget.currentFont()
        current_font.setPointSize(self.current_font_size)
        self.current_font_size += 6 
        self.text_widget.setCurrentFont(current_font)

    def decrease_font_size(self):
        current_font = self.text_widget.currentFont()
        current_font.setPointSize(self.current_font_size)
        self.current_font_size -= 3  
        self.text_widget.setCurrentFont(current_font)

    def change_font_family(self, font):
        current_font = self.text_widget.currentFont()
        current_font.setFamily(font.family())
        self.text_widget.setCurrentFont(current_font)


    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
    def dropEvent(self, event):
        for url in event.mimeData().urls():
            #print(url)
            image_path = url.toLocalFile()
            if image_path.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp', '.bmp', '.tiff', '.ico')):    
                
                if platform.system() == "Windows":
                    # Adjust formatting for Windows
                    #image_syntax = f"![Image]({image_path.replace('/', '\\\\')})"
                    image_syntax = f"![Image]({os.path.join(*image_path.split('/'))})"
                
                #elif "dolphin" in image_path.lower():
                #    # Extract file path after 'file://'
                #    image_path = image_path[len("file://"):]
                 #   image_syntax = f"![Image]({image_path})"

                else:
                    # Default formatting
                    image_syntax = f"![Image]({image_path})" # works with thunar on linux
                
                current_text = self.text_widget.toPlainText()
                self.text_widget.setPlainText(current_text + '\n' + image_syntax)


    def init_ui(self,passwd,filepath):
        self.passwd = passwd
        self.setWindowTitle("Cool In-Memory Text Editor")
        self.setGeometry(100, 100, 800, 600)

        # Set PeachPuff background color
        self.set_peachpuff_style()

        # Create the text widget
        self.text_widget = QTextEdit()
        self.text_widget.setFontPointSize(18)
        #self.text_widget.setFont(QtGui.QFont("Noto Color Emoji", 18))
        self.current_font_size = 18
        self.text_widget.setFont(QtGui.QFont("DejaVu Sans", self.current_font_size))
        #self.text_widget.setFont(QtGui.QFont("Liberation Sans", 18))
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
        """)
        button_css = """
            QPushButton {
                background-color: #ff6b6b;
                color: white;
                border: none;
                padding: 5px;
                border-radius: 5px;
            }

            QPushButton:hover {
                border-radius: 10px;
                background-color: #3a1c71;
            }
        """
        save_button = QPushButton("Save")
        save_button.clicked.connect(self.saveNexit)
        save_button.setStyleSheet(button_css)
        self.toolbar.addWidget(save_button)



        attach_button = QPushButton("Attach")
        attach_button.clicked.connect(self.open_file_dialog_for_attach)
        attach_button.setStyleSheet(button_css)
        self.toolbar.addWidget(attach_button)


        # Bold Button
        bold_button = QPushButton("Bold")
        bold_button.clicked.connect(self.toggle_bold)
        bold_button.setStyleSheet(button_css)
        self.toolbar.addWidget(bold_button)
        
        bold_button.setIcon(QIcon.fromTheme("format-text-bold"))

        # Set the central widget and layout
        layout = QVBoxLayout()
        layout.addWidget(self.text_widget)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

#####################################################################################################
        #central_widget = QWidget(self)
        #self.setCentralWidget(central_widget)
        #layout = QVBoxLayout(central_widget)
        self.audio_widgets_layout = QVBoxLayout()
        layout.addLayout(self.audio_widgets_layout)

        self.audio_widgets = []
###########################################################################################
        #Markdown Toggle
        self.is_markdown_view = False
        self.save_backup = ""
        self.alraddy_ran_markdown = False
        self.toggle_button = QPushButton("Markdown Toggle", self)
        self.toggle_button.clicked.connect(self.toggle_view)
        self.toggle_button.setStyleSheet(button_css)
        self.toolbar.addWidget(self.toggle_button)

        # Increase Font Size Button
        increase_font_button = QPushButton("+")
        increase_font_button.clicked.connect(self.increase_font_size)
        increase_font_button.setIcon(QIcon.fromTheme("format-font-size-less"))
        increase_font_button.setStyleSheet(button_css)
        self.toolbar.addWidget(increase_font_button)

        # Decrease Font Size Button
        decrease_font_button = QPushButton("-")
        decrease_font_button.clicked.connect(self.decrease_font_size)
        decrease_font_button.setIcon(QIcon.fromTheme("format-font-size-less"))
        decrease_font_button.setStyleSheet(button_css)
        self.toolbar.addWidget(decrease_font_button)


        # Add a stretchable space
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        spacer.setStyleSheet(button_css)
        self.toolbar.addWidget(spacer)


        exit_button = QPushButton("Exit")
        exit_button.clicked.connect(self.Exit_without_save)
        exit_button.setStyleSheet(button_css)
        self.toolbar.addWidget(exit_button)
  
        # Record Button
        self.record_picker =  RecorderGUI(passwd, parent=self)
        self.record_picker.setGeometry(80, 80, 700, 400)
        self.record_picker.hide()



        # Record Button
        emoji_button = QPushButton("Record")
        emoji_button.clicked.connect(self.toggle_record)
        emoji_button.setIcon(QIcon.fromTheme("smile"))
        emoji_button.setStyleSheet(button_css)
        self.toolbar.addWidget(emoji_button)





        self.emoji_picker = EmojiPicker(parent=self)
        self.emoji_picker.setGeometry(80, 80, 700, 400)
        self.emoji_picker.hide()


        # Emoji Button
        emoji_button = QPushButton("😊 Emoji")
        emoji_button.clicked.connect(self.toggle_emoji_picker)
        emoji_button.setIcon(QIcon.fromTheme("smile"))
        emoji_button.setStyleSheet(button_css)
        self.toolbar.addWidget(emoji_button)


        # Add the toolbar to the main window
        self.addToolBar(self.toolbar)

        self.close_button = QtWidgets.QPushButton("❌", self.emoji_picker)
        self.close_button.setGeometry(450, 5, 30, 30)
        self.close_button.setFont(QtGui.QFont("Arial", 18))
        self.close_button.clicked.connect(self.emoji_picker.hide)

        # Add a stretchable space
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.toolbar.addWidget(spacer)

        # Change the Font Family
        self.font_family_combobox = QFontComboBox(self)
        self.font_family_combobox.currentFontChanged.connect(self.change_font_family)
        self.font_family_combobox.setStyleSheet(button_css)
        self.toolbar.addWidget(self.font_family_combobox)
        self.text_widget.setFontPointSize(18)

###########################################################################################################

        def find_page_number(json_file, target_full_path):
            with open(json_file, 'r') as file:
                data = json.load(file)

            for page_number, page_info in data.items():
                if page_info.get("Main Full path") == target_full_path:
                    return page_number

            return None


























############################

            
        print("filepath",filepath)
        if filepath == None :
            print("Skip Database Check(NEW)")
        else:
            if platform.system() == "Windows":
                filepath = filepath.replace("\\", "/")
            # Example usage
            desired_path = os.path.dirname(filepath)
            
            json_file_path = desired_path + "/Database_Lieutenant.json"
            print("jsopn path", json_file_path)
            target_path_to_find = filepath
            print(json_file_path, target_path_to_find)
            page_number_found = find_page_number(json_file_path, target_path_to_find)
            print(page_number_found)
            print("=====================")
            if page_number_found is not None:
                print(f"{page_number_found}")
            else:
                print(f"No page found for the given path.")

#########################


            # Read the JSON file
            with open(json_file_path, 'r') as file:
                data = json.load(file)
                
            # Access the audio link and store it in a variable
            Day = str(page_number_found)
            default_audio_file_paths = data[Day]['Links']['Audio Link']
            print("default_audio_file_paths",default_audio_file_paths)
            self.insert_default_audio(default_audio_file_paths)


        self.toggle_audio_panel_button = QPushButton("Toggle Audio Panel", self)
        self.toggle_audio_panel_button.setCheckable(True)
        self.toggle_audio_panel_button.toggled.connect(self.toggle_audio_panel)
        self.toggle_audio_panel_button.setStyleSheet(button_css)
        self.toolbar.addWidget(self.toggle_audio_panel_button)
        self.is_typing_hello = False


    def insert_default_audio(self,file_paths):
        #file_paths
        for file_path in file_paths:
            print(file_path)
            audio_widget = AudioWidget(file_path, self.passwd)
            self.audio_widgets.append(audio_widget)
            self.audio_widgets_layout.addWidget(audio_widget)


    def toggle_audio_panel(self, checked):
        for i in range(self.audio_widgets_layout.count()):
            self.audio_widgets_layout.itemAt(i).widget().setVisible(checked)


    def open_file_dialog_for_attach(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_dialog = QFileDialog()
        file_dialog.setOptions(options)
        selected_file, _ = file_dialog.getOpenFileName(self, "Open File", "", "Audio and Image Files (*.mp3 *.wav *.ogg *.aac *.m4a *.flac *.wma *.aiff *.alac *.ape *.opus *.mid *.midi *.png *.jpg *.jpeg *.gif *.svg *.webp *.bmp *.tiff *.ico)")
        if selected_file:
            markdown_text = f"![ Attach ]({selected_file})"
            # append
            current_text = self.text_widget.toPlainText()
            self.text_widget.setPlainText(current_text + "\n" +  markdown_text + "\n")




###########################################################################################################
    def toggle_record(self):
        if self.record_picker.isVisible():
            self.record_picker.hide()
            print("hide")
        else:
            self.record_picker.show()
            print("show")

    def toggle_emoji_picker(self):
        if self.emoji_picker.isVisible():
            self.emoji_picker.hide()
            print("hide")
        else:
            self.emoji_picker.show()
            print("show")

    def change_emoji_category(self, index): # twitter-twemoji-fonts
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

    def toggle_view(self):
        if self.is_markdown_view:
            if self.alraddy_ran_markdown:
                self.text_widget.setPlainText(self.save_backup)
        else:

            self.save_backup = self.text_widget.toPlainText()
            html_content = markdown2.markdown(self.text_widget.toPlainText())
            self.text_widget.setHtml(html_content)
            self.alraddy_ran_markdown = True

        self.is_markdown_view = not self.is_markdown_view

    def var_to_editor(self, content):
        self.text_widget.setPlainText(content)

    def save_text(self):  # forward text
        self.close()
        text = self.text_widget.toPlainText()

        #remove_files_with_extensions() # remove all photo:
        return text

    def saveNexit(self):
        reply = QMessageBox.question(self, "Save Confirmation", "Are you sure you want to Save?", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:

            #remove_files_with_extensions() # remove all photo:
            self.save = True
            self.close()

    def Exit_without_save(self):
        reply = QMessageBox.question(self, "Exit Confirmation", "Are you sure you want to Exit without save?", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:

            remove_files_with_extensions() # remove all photo:
            self.save = False
            self.close()
