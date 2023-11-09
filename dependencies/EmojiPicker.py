from functools import partial
from PySide6 import QtWidgets, QtGui, QtCore

from PySide6.QtWidgets import QApplication, QMainWindow, QTextEdit, QVBoxLayout, QWidget, QPushButton
from PySide6.QtGui import QTextCursor, QFont, QIcon
from PySide6.QtCore import Qt, QPoint

from .emoji_data import categories

class EmojiPicker(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Emoji Picker")

        self.dragging = False
        self.offset = QPoint()

        self.categories = categories # get emoji from  emoji_data.py

        self.current_category = "Smileys"
        layout = QtWidgets.QGridLayout()
        self.setLayout(layout)
        self.init_ui()

    # navigate button press resize effect(emoji)
    def resize_left(self):
        new_size = self.size() + QtCore.QSize(-90, 0)
        self.resize(new_size)

    def resize_right(self):
        new_size = self.size() + QtCore.QSize(90, 0)
        self.resize(new_size)

    def resize_top(self):
        new_size = self.size() + QtCore.QSize(0, -90)
        self.resize(new_size)

    def resize_bottom(self):
        new_size = self.size() + QtCore.QSize(0, 90)
        self.resize(new_size)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.offset = event.pos()

    def mouseMoveEvent(self, event):
        if self.dragging:
            new_pos = self.mapToGlobal(event.pos() - self.offset)
            self.move(new_pos)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = False

    def init_ui(self):
        while self.layout().count() > 0:
            item = self.layout().takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()


        scroll_area = QtWidgets.QScrollArea()
        scroll_content = QtWidgets.QWidget()
        scroll_layout = QtWidgets.QGridLayout(scroll_content)
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(scroll_content)
        self.layout().addWidget(scroll_area)

        # Create floating buttons for resizing in different directions
        self.resize_left_button = QtWidgets.QPushButton("←", self)
        self.resize_right_button = QtWidgets.QPushButton("→", self)
        self.resize_top_button = QtWidgets.QPushButton("↑", self)
        self.resize_bottom_button = QtWidgets.QPushButton("↓", self)

        # Position the buttons at the appropriate corners
        emoji_picker_rect = self.rect()
        button_offset = QtCore.QPoint(-200, 25)
        button_offsett = QtCore.QPoint(-0, 25)
        self.resize_left_button.move(emoji_picker_rect.bottomLeft() - button_offsett)
        self.resize_right_button.move(emoji_picker_rect.bottomRight() - button_offsett)
        self.resize_top_button.move(emoji_picker_rect.bottomLeft() - button_offset)
        self.resize_bottom_button.move(emoji_picker_rect.bottomRight() - button_offset)


        # navigate button press resize effect(emoji)
        self.resize_left_button.clicked.connect(self.resize_left)
        self.resize_right_button.clicked.connect(self.resize_right)
        self.resize_top_button.clicked.connect(self.resize_top)
        self.resize_bottom_button.clicked.connect(self.resize_bottom)
        
        emojis = self.categories[self.current_category]
        num_columns = 8
        row, col = 0, 0
        button_size = 30
        emoji_style = f"font-size: {button_size}px;"
        emoji_font_size = button_size - 10
        blank_space_height = 90

        blank_space = QtWidgets.QWidget()
        blank_space.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        blank_space.setMaximumHeight(blank_space_height)
        scroll_layout.addWidget(blank_space, row, col, 3, num_columns)


        row += 5
        for emoji in emojis:
            button = QtWidgets.QPushButton(emoji)
            button.setStyleSheet(emoji_style)
            button.setFont(QtGui.QFont("twemoji", emoji_font_size))
            button.clicked.connect(partial(self.insert_emoji, emoji))
            scroll_layout.addWidget(button, row, col)
            col += 1
            if col >= num_columns:
                col = 0
                row += 1

        scroll_layout.setColumnStretch(num_columns, 1)



    def insert_emoji(self, emoji):
        cursor = self.parent().text_widget.textCursor()
        cursor.insertText(emoji)
        self.parent().text_widget.setTextCursor(cursor)
