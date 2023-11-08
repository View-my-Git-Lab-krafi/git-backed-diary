import sys
from PySide2.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QPushButton, QTextEdit, QAction, QFileDialog

class MenuApp(QMainWindow):
    def __init__(self, passwd):
        super().__init__()
        self.passwd = passwd
        self.setWindowTitle("Menu")
        self.setGeometry(100, 100, 800, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.container = central_widget 
        layout = QVBoxLayout(central_widget)

        prompt_label = QLabel("hi")
        self.output_label = QLabel()

        def start_editor():
            self.text_widget = QTextEdit()
            self.setCentralWidget(self.text_widget)
            self.text_widget.setPlainText("Start typing here...")

            menu_bar = self.menuBar()
            file_menu = menu_bar.addMenu("File")

            save_action = QAction("Save", self)
            save_action.setShortcut("Ctrl+S")
            save_action.triggered.connect(self.save_text)
            file_menu.addAction(save_action)

            back_action = QAction("Back to Menu", self)
            back_action.setShortcut("Ctrl+Q")
            back_action.triggered.connect(self.back_to_menu)
            file_menu.addAction(back_action)

            self.output_label.setText("Text editor is active. Use 'Ctrl+S' to save and 'Ctrl+Q' to go back to the menu.")

            self.setWindowTitle("Text Editor")

        button = QPushButton("Start the text editor")  
        button.clicked.connect(start_editor)

        layout.addWidget(prompt_label)
        layout.addWidget(self.output_label)
        layout.addWidget(button)

    def save_text(self):
        text = self.text_widget.toPlainText()
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.AnyFile)
        file_path, _ = file_dialog.getSaveFileName(self, "Save Text File", "", "Text Files (*.txt)")

        if file_path:
            with open(file_path, "w") as file:
                file.write(text)

    def back_to_menu(self):
        # Restore the main menu
        self.text_widget.deleteLater()
        self.setWindowTitle("Menu")
        self.setCentralWidget(container)
        self.output_label.clear()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    menu_app = MenuApp("your_password")
    menu_app.show()
    sys.exit(app.exec_())
