# pip install markdown2 pycryptodome PySide2
import os
import io
from PySide6.QtWidgets import QPushButton, QWidget, QHBoxLayout, QLabel #, QApplication, QMainWindow, QVBoxLayout, QTextEdit, QToolBar, QFileDialog
from PySide6.QtGui import QTextCursor

from PySide6.QtWidgets import (QWidget) #, QApplication, QMainWindow, QTextEdit, QVBoxLayout, QFileDialog, QLineEdit,QCalendarWidget)
from PySide6.QtWidgets import (QLabel, QPushButton) # , QFontComboBox, QToolBar, QMessageBox, QSizePolicy, QComboBox, QMenu, QListWidget)

import noisereduce as nr
from dependencies.VarDataEncryptor import start_var_data_encryptor
import pyaudio
from pydub import AudioSegment
import threading
import base64
import numpy as np



'''
from PySide6.QtWidgets import QApplication, QMainWindow, QMenu, QMenuBar # QAction,
from PySide6 import QtWidgets, QtGui
from PySide6.QtGui import QFont, QSyntaxHighlighter, QIcon, QKeyEvent, QKeySequence, QColor, QPalette, QTextCursor, QTextCharFormat
from PySide6.QtCore import Qt, QRegularExpression, QPoint , QTimer, QDate
from PySide6 import QtWidgets, QtGui, QtCore
from PySide6.QtWidgets import QInputDialog
#  local file import
#from dependencies.emoji_data import categories

from dependencies.EmojiPicker import EmojiPicker
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
#from PySide6.QtCore import QObject, Signal, QTimer, QBuffer
#from PySide6.QtMultimedia import QMediaPlayer
#from dependencies.record import RecorderGUI

'''
import platform


class AudioWidget(QWidget):
    def __init__(self, audio_path, passwd):
        super().__init__()
        self.passwd = passwd
        self.audio_path = audio_path



        #if platform.system() == "Windows":
            #self.audio_path = audio_path.replace("/","\\")
            
        self.playing = False
        self.noise_reduction=False
        self.pause_event = threading.Event()

        layout = QHBoxLayout(self)
        self.label = QLabel(os.path.basename(audio_path), self)
        layout.addWidget(self.label)

        self.play_button = QPushButton("Play", self)
        self.play_button.clicked.connect(self.toggle_playback)
        self.play_button.setStyleSheet("background-color: #90EE90; color: black;")
        layout.addWidget(self.play_button)

        self.play_with_nr_button = QPushButton("NR", self)
        self.play_with_nr_button.clicked.connect(self.toggle_play_with_nr)
        self.play_with_nr_button.setStyleSheet("background-color: #FFD700; color: black;")
        layout.addWidget(self.play_with_nr_button)
        
        self.pause_button = QPushButton("Pause", self)
        self.pause_button.clicked.connect(self.toggle_pause)
        self.pause_button.setEnabled(False)
        self.pause_button.setStyleSheet("background-color: #FFFFE0; color: black;")
        layout.addWidget(self.pause_button)
        self.pause_button.hide()


        self.stop_button = QPushButton("Stop", self)
        self.stop_button.clicked.connect(self.safe_stop_audio)
        self.stop_button.setEnabled(False)
        
        layout.addWidget(self.stop_button)

        self.toggle_playback()
        self.safe_stop_audio()
    def toggle_play_with_nr(self):
        if self.play_with_nr_button.text() == "NR":
            self.play_with_nr_button.setText("Stop NR")
            self.play_with_nr_button.setStyleSheet("background-color: #ADD8E6; color: black;")
            self.noise_reduction=True
            self.toggle_playback()
            self.safe_stop_audio()

        else:
            self.play_with_nr_button.setText("NR")
            self.play_with_nr_button.setStyleSheet("background-color: #FFD700; color: black;")
            self.noise_reduction=False
            self.toggle_playback()
            self.safe_stop_audio()

    def toggle_playback(self):
        self.stop_button.setStyleSheet("background-color: #FFB6C1; color: black;")
        if not self.playing:
            self.play_audio(self.noise_reduction)
            self.play_button.setText("Pause")
            self.play_button.setStyleSheet("background-color: #ffa600; color: black;")

            self.pause_button.setEnabled(True)
            self.stop_button.setEnabled(True)
        else:
            self.toggle_pause()
            self.play_button.setText("Resume" if not self.pause_event.is_set() else "Pause")
            # Set the color based on the playback state
            color = "#90EE90" if not self.pause_event.is_set() else "#ffa600"
            self.play_button.setStyleSheet(f"background-color: {color}; color: black")

    def play_audio(self, apply_noise_reduction=False):
        print("Let's play the audio:", self.audio_path)

        def play_in_thread():
            with open(self.audio_path, 'r') as file:
                encrypted_data = file.read()

            decrypted_data = start_var_data_encryptor("Dec_Fernet_PBKDF2_HMAC_SHA512", encrypted_data, self.passwd)
            flac_data = base64.b64decode(decrypted_data)
            audio_segment = AudioSegment.from_file(io.BytesIO(flac_data), format="flac")

            if apply_noise_reduction:
                sr = audio_segment.frame_rate
                raw_audio_data = np.frombuffer(audio_segment.raw_data, dtype=np.int16)
                raw_audio_data = nr.reduce_noise(raw_audio_data, sr=sr)
                raw_audio_data = raw_audio_data.astype(np.int16).tobytes()
            else:
                raw_audio_data = audio_segment.raw_data

            p = pyaudio.PyAudio()
            stream = p.open(format=p.get_format_from_width(audio_segment.sample_width),
                            channels=audio_segment.channels,
                            rate=audio_segment.frame_rate,
                            output=True)

            for chunk in self.chunks(raw_audio_data, 1024):
                if not self.playing:
                    break  
                self.pause_event.wait()
                stream.write(chunk)

            stream.stop_stream()
            stream.close()
            p.terminate()

        self.audio_thread = threading.Thread(target=play_in_thread)
        self.playing = True
        self.audio_thread.start()



    def toggle_pause(self):
        print("Toggling pause")
        self.pause_event.set() if not self.pause_event.is_set() else self.pause_event.clear()

    def safe_stop_audio(self):
        print("Stopping the audio safely")
        self.playing = False
        self.pause_event.set()
        if hasattr(self, 'audio_thread') and self.audio_thread.is_alive():
            self.audio_thread.join()  

        self.play_button.setText("Play")
        self.play_button.setStyleSheet("background-color: #90EE90; color: black;")  
        self.pause_button.setEnabled(False)
        self.stop_button.setStyleSheet("background-color: ; color: black;")

        self.stop_button.setEnabled(False)

        

    def chunks(self, data, size):
        for i in range(0, len(data), size):
            yield data[i:i + size]
