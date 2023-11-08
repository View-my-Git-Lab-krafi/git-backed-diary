
from PySide6 import QtWidgets, QtGui
from PySide6 import QtWidgets, QtGui, QtCore
from PySide6.QtWidgets import (QApplication, QMainWindow, QTextEdit, QVBoxLayout, QWidget, QAction, QFileDialog)
from PySide6.QtWidgets import (QFontComboBox, QToolBar, QMessageBox, QSizePolicy, QLabel, QComboBox, QMenu, QPushButton)
from PySide6.QtGui import QKeySequence, QColor, QPalette, QTextCursor, QTextCharFormat
from PySide6.QtGui import QFont, QSyntaxHighlighter, QIcon, QKeyEvent
from PySide6.QtCore import Qt, QRegularExpression, QPoint


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

    def highlightBlock(self, text):  # if you remove it editor will get freeze
        for pattern, format in self.highlighting_rules:
            expression = QRegularExpression(pattern)
            it = expression.globalMatch(text)
            while it.hasNext():
                match = it.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), format)
