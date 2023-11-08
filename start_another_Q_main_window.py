# pip install markdown2 pycryptodome PySide2

import sys

from PySide2.QtWidgets import (QApplication, QMainWindow, QTextEdit, QVBoxLayout, QWidget, QAction, QFileDialog, QLineEdit,QCalendarWidget)
from PySide2.QtWidgets import (QFontComboBox, QToolBar, QMessageBox, QSizePolicy, QLabel, QComboBox, QMenu, QPushButton, QListWidget)
from PySide2.QtGui import QKeySequence, QColor, QPalette, QTextCursor, QTextCharFormat
from PySide2.QtGui import QFont, QSyntaxHighlighter, QIcon, QKeyEvent
from PySide2.QtCore import Qt, QRegularExpression, QPoint , QTimer, QDate
from PySide2.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton
from PySide2.QtGui import QKeySequence
from PySide2.QtCore import QObject, Signal

global app
app = None 
class MagicMemoryMarkTextEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
    def init_ui(self):
        self.setWindowTitle("Cool In-Memory Text Editor")
        self.setGeometry(100, 100, 800, 600)

        self.text_widget = QTextEdit()

        self.save_action = QAction(QIcon.fromTheme("document-save"), "Save", self)
        self.save_action.triggered.connect(self.save_text)
        self.save_action.setShortcut(QKeySequence.Save)

        save_button = QPushButton("Save", self)
        save_button.clicked.connect(self.save_text)

        self.open_action = QAction(QIcon.fromTheme("document-open"), "Open", self)
        self.open_action.triggered.connect(self.open_file)
        self.open_action.setShortcut(QKeySequence.Open)

        layout = QVBoxLayout()
        layout.addWidget(self.text_widget)
        layout.addWidget(save_button) 
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)


    def save_text(self):
        text = self.text_widget.toPlainText()
        print("from text editor",text)
        self.close()
        Process(text)
        #return text


    def open_file(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Text Files (*.txt);;All Files (*)", options=options)

        if file_name:
            try:
                with open(file_name, "r") as file:
                    self.text_widget.setPlainText(file.read())
            except Exception as e:
                print(f"Error opening file: {str(e)}")

def Process(a):
    print("process",a)
    #print(a)

class MenuApp(QMainWindow):
    def __init__(self, passwd):
        super().__init__()
        self.passwd = passwd
        self.setWindowTitle("Menu")
        self.setGeometry(100, 100, 800, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        self.editor = None

        prompt_label = QLabel("hi")
        self.output_label = QLabel()

        def start_editor():
            if self.editor is None:
                self.editor = MagicMemoryMarkTextEditor()
                self.editor.show()
                print("++++")
                print("from menuapp", self.editor)
                print("====")

        button = QPushButton("Open Editor")
        button.clicked.connect(start_editor)

        layout.addWidget(prompt_label)
        layout.addWidget(self.output_label)
        layout.addWidget(button)
if __name__ == "__main__":
    
    app = QApplication(sys.argv)
    menu_app = MenuApp("your_password")
    menu_app.show()
    sys.exit(app.exec_())