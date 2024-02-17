
import platform
from PySide6.QtGui import QColor, QPalette #, QFont, QSyntaxHighlighter, QIcon, QKeyEvent, QKeySequence,  QTextCursor, QTextCharFormat
from PySide6 import QtWidgets
from PySide6.QtCore import QObject, Signal, QTimer, Qt, QPoint# , QtCore # , QBuffer
from PySide6 import QtCore

import pyaudio

from pydub import AudioSegment
import noisereduce as nr
import numpy as np
import threading
import base64

from dependencies.AudioPlayer import AudioWidget
from dependencies.VarDataEncryptor import start_var_data_encryptor
import random
import string

'''
#from PySide6.QtCore import Qt, QRegularExpression, QDate

from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QFileDialog
from PySide6.QtMultimedia import QMediaPlayer
from PySide6.QtWidgets import QApplication, QMainWindow, QTextEdit, QVBoxLayout, QWidget, QPushButton
from PySide6.QtGui import QTextCursor, QFont, QIcon
from PySide6.QtWidgets import QApplication, QMainWindow, QMenu, QMenuBar # QAction,
from PySide6 import QtWidgets, QtGui
from PySide6.QtWidgets import (QApplication, QMainWindow, QTextEdit, QVBoxLayout, QWidget,  QFileDialog, QLineEdit,QCalendarWidget)
from PySide6.QtWidgets import (QFontComboBox, QToolBar, QMessageBox, QSizePolicy, QLabel, QComboBox, QMenu, QPushButton, QListWidget)
from PySide6.QtWidgets import QInputDialog

'''

class Communicate(QObject):
    finished = Signal()

class Recorder:
    def __init__(self, gui_instance):
        self.CHUNK = 1024
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 44100
        self.signal = Communicate()
        self.recording = False

        self.p = pyaudio.PyAudio()
        self.stream = None
        self.recorded_frames = []
        self.Noise_Reduction  =  False # It work i will add this feature button in future 
        self.FirstTimeWarning = False
        self.SecondTimeWarning = False
        self.ThirdTimeWarning = False
        self.gui_instance = gui_instance

        self.playback_paused = False

        self.stop_event = threading.Event()
        self.pause_event = threading.Event()

    def start_recording(self):
        self.stream = self.p.open(format=self.FORMAT,
                                  channels=self.CHANNELS,
                                  rate=self.RATE,
                                  input=True,
                                  frames_per_buffer=self.CHUNK)

        self.recording = True
        print("Recording started")

    def generate_buzz(self, buzz_type, duration=3, volume=0.5, sample_rate=44100):
        frequencies = {
            1: 440,
            2: 523,
            3: 659,
            4: 783,
            5: 880
        }

        frequency = frequencies.get(buzz_type, 440)

        t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
        signal = volume * np.sin(2 * np.pi * frequency * t)
        return signal.astype(np.float32)

    def play_sound(self, signal, sample_rate=44100):
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paFloat32, channels=1, rate=sample_rate, output=True)

        stream.write(signal.tobytes())

        stream.stop_stream()
        stream.close()
        p.terminate()

    def pause_recording(self):
        if self.recording:
            self.recording = False
            self.stream.stop_stream()
            self.stream.close()
            if self.Noise_Reduction:
                if self.recorded_frames:
                    audio_data = b''.join(self.recorded_frames)
                    audio_array = np.frombuffer(audio_data, dtype=np.int16)
                    reduced_audio = nr.reduce_noise(audio_array, sr=self.RATE)
                    self.recorded_frames = [reduced_audio.tobytes()]
            else:
                print("Noice reduction is disable")
            buffer_size_mb = sum(len(frame) for frame in self.recorded_frames) / (1024 * 1024)
            print(f"Recording paused. Buffer size: {len(self.recorded_frames)} frames {buffer_size_mb:.2f} MB")

    def stop_recording(self):
        if self.recording:
            self.recording = False
            self.stream.stop_stream()
            self.stream.close()
            print("Recording stopped")
#reduced_noise = nr.reduce_noise(y=data, sr=rate)
    def record_chunk(self):
        if self.recording:
            data = self.stream.read(self.CHUNK)
            self.recorded_frames.append(data)
            buffer_size_mb = sum(len(frame) for frame in self.recorded_frames) / (1024 * 1024)
            if buffer_size_mb > 35 and not self.FirstTimeWarning:
                    self.signal = self.generate_buzz(1,duration=1, volume=0.1)
                    self.play_sound(self.signal)
                    self.FirstTimeWarning = True

            elif buffer_size_mb > 40 and not self.SecondTimeWarning:
                    self.signal = self.generate_buzz(3,duration=2, volume=0.5)
                    self.play_sound(self.signal)
                    self.SecondTimeWarning = True

            elif buffer_size_mb > 45 and not self.ThirdTimeWarning:
                    self.signal = self.generate_buzz(5,duration=5, volume=1)
                    self.play_sound(self.signal)
                    self.ThirdTimeWarning = True

                    #Stop
                    self.pause_recording()
                    self.gui_instance.toggle_btn.setText('Start')
                    self.gui_instance.timer.stop()

    def add_audio(self, audio_path, passwd):
        audio_widget = AudioWidget(audio_path, passwd)
        self.gui_instance.parent.audio_widgets.append(audio_widget)
        self.gui_instance.parent.audio_widgets_layout.addWidget(audio_widget)

    #current_text = self.text_widget.toPlainText()
     #           self.text_widget.setPlainText(current_text + '\n' + image_syntax)


        cursor = self.gui_instance.parent.text_widget.textCursor()

        cursor.insertBlock()
        #cursor.movePosition(QTextCursor.End)
#        ![alt text](http://url/to/img.png)
        insert_text = "![ Voice Name ]( " + audio_path + ")"
        cursor.insertText(insert_text)
        cursor.insertBlock()
        cursor.insertText("\n") 


    def save_encrypted_audio(self, file_path, passwd):
        if self.recorded_frames:
            audio_data = b''.join(self.recorded_frames)
            audio_segment = AudioSegment(
                audio_data,
                sample_width=self.p.get_sample_size(self.FORMAT),
                frame_rate=self.RATE,
                channels=self.CHANNELS
            )

            # Convert AudioSegment to FLAC format
            flac_data = audio_segment.export(format="flac").read()# reduce size
            audio_data_str_decode = base64.b64encode(flac_data).decode() #decode for enc
            encrypted_data = start_var_data_encryptor("Enc_Fernet_PBKDF2_HMAC_SHA512", audio_data_str_decode, passwd)
            with open(file_path, "w") as file:
                file.write(encrypted_data)
                            ############################################################

            self.add_audio(file_path , passwd)


            self.recorded_frames = []

    def play_audio_thread(self):
        if self.recorded_frames:
            audio_data = b''.join(self.recorded_frames)

            player = pyaudio.PyAudio()
            stream = player.open(format=self.FORMAT,
                                channels=self.CHANNELS,
                                rate=self.RATE,
                                output=True)

            try:
                chunk_size = 1024
                idx = 0

                while idx < len(audio_data) and not self.stop_event.is_set():
                    if not self.pause_event.is_set():
                        stream.write(audio_data[idx:idx + chunk_size])
                        idx += chunk_size

            finally:
                stream.stop_stream()
                stream.close()
                player.terminate()

    def pause_audio(self):
        self.pause_event.set()

    def resume_audio(self):
        self.pause_event.clear()

    def stop_audio(self):
        self.stop_event.set()


class  RecorderGUI(QtWidgets.QWidget):

    def set_button_size(self, button, width, height):
        button.setFixedWidth(width)
        button.setFixedHeight(height)
    def __init__(self, passwd, parent=None):
        self.passwd = passwd
        self.parent = parent 
        super().__init__(parent)
        self.recorder = Recorder(self)
        self.setWindowTitle("record")
        self.dragging = False
        self.offset = QPoint()
        
        button_width = 150
        button_height = 50

        layout = QtWidgets.QGridLayout()
        self.setMinimumSize(300, 200)  # Adjust the size as needed


        # Set background color to brown
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(139, 69, 19))  # RGB values for brown
        self.setPalette(palette)



        self.toggle_btn = QtWidgets.QPushButton('New')
        self.toggle_btn.clicked.connect(self.on_toggle_btn_clicked)

        self.play_btn = QtWidgets.QPushButton('Play Buffer')
        self.play_btn.clicked.connect(self.on_play_btn_clicked)

        self.stop_btn = QtWidgets.QPushButton('Stop Buffer')
        self.stop_btn.clicked.connect(self.on_stop_btn_clicked)

        self.pause_btn = QtWidgets.QPushButton('Pause Buffer')
        self.pause_btn.clicked.connect(self.on_pause_btn_clicked)

        self.resume_btn = QtWidgets.QPushButton('Resume Buffer')
        self.resume_btn.clicked.connect(self.on_resume_btn_clicked)

        self.clear_buffer_btn = QtWidgets.QPushButton('Clear Buffer')
        self.clear_buffer_btn.clicked.connect(self.on_clear_btn_clicked)

        self.stop_event = threading.Event()

        save_btn = QtWidgets.QPushButton('Save')
        save_btn.clicked.connect(self.on_save_btn_clicked)
    


        self.set_button_size(self.toggle_btn, button_width, button_height)
        self.set_button_size(self.play_btn, button_width, button_height)
        self.set_button_size(self.stop_btn, button_width, button_height)
        self.set_button_size(self.pause_btn, button_width, button_height)
        self.set_button_size(self.resume_btn, button_width, button_height)
        self.set_button_size(self.clear_buffer_btn, button_width, button_height)
        self.set_button_size(save_btn, button_width, button_height)

        self.toggle_btn.setStyleSheet("background-color: green")
        self.play_btn.setStyleSheet("background-color: green")
        self.stop_btn.setStyleSheet("background-color: red")
        self.pause_btn.setStyleSheet("background-color: yellow")
        self.resume_btn.setStyleSheet("background-color: blue")
        self.clear_buffer_btn.setStyleSheet("background-color: red")
        save_btn.setStyleSheet("background-color: green")

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.toggle_btn)
        layout.addWidget(self.play_btn)
        layout.addWidget(self.pause_btn)
        layout.addWidget(save_btn)
        layout.addWidget(self.clear_buffer_btn)
        layout.setAlignment(QtCore.Qt.AlignCenter)

        self.setLayout(layout)
        self.setWindowTitle('Audio Recorder')

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.recorder.record_chunk)

        #hello_button = QtWidgets.QPushButton("Print Hello")
        #hello_button.clicked.connect(self.print_hello)
        #self.layout().addWidget(hello_button)



    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = True
            print(event.pos())
            self.offset = event.pos()

    def mouseMoveEvent(self, event):
        if self.dragging:
            delta = event.pos() - self.offset
            self.move(self.pos() + delta)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = False

    def on_clear_btn_clicked(self):
        self.recorder.recorded_frames = []

    def on_toggle_btn_clicked(self):
        if not self.recorder.recording:
            self.recorder.start_recording()
            self.timer.start(10)
            self.toggle_btn.setText('Pause')
            self.toggle_btn.setStyleSheet("background-color: red")
        else:
            self.recorder.pause_recording()
            self.timer.stop()
            self.toggle_btn.setText('Continue')
            self.toggle_btn.setStyleSheet("background-color: green")


    def on_play_btn_clicked(self):
        self.recorder.stop_event.clear()
        self.recorder.pause_event.clear()

        play_thread = threading.Thread(target=self.recorder.play_audio_thread)
        play_thread.start()

        self.play_btn.setText('Stop Buffer')
        self.play_btn.clicked.disconnect(self.on_play_btn_clicked)
        self.play_btn.clicked.connect(self.on_stop_btn_clicked)
        self.play_btn.setStyleSheet("background-color: red")

    def on_pause_btn_clicked(self):
        self.recorder.pause_audio()
        self.pause_btn.setText('Resume Buffer')
        self.pause_btn.clicked.disconnect(self.on_pause_btn_clicked)
        self.pause_btn.clicked.connect(self.on_resume_btn_clicked)
        self.pause_btn.setStyleSheet("background-color: blue")
    def on_resume_btn_clicked(self):
        self.recorder.resume_audio()
        self.pause_btn.setText('Pause Buffer')
        self.pause_btn.clicked.disconnect(self.on_resume_btn_clicked)
        self.pause_btn.clicked.connect(self.on_pause_btn_clicked)
        self.pause_btn.setStyleSheet("background-color: red")

    def on_stop_btn_clicked(self):
        self.recorder.stop_event.set()
        self.play_btn.setText('Play Buffer')
        self.play_btn.clicked.disconnect(self.on_stop_btn_clicked)
        self.play_btn.clicked.connect(self.on_play_btn_clicked)
        self.play_btn.setStyleSheet("background-color: green")

    def generate_random_string(self,length):
        characters = string.ascii_letters + string.digits
        characters = ''.join(char for char in characters if char.isalnum())
        random_string = ''.join(random.choice(characters) for _ in range(length))
        return random_string

    def on_save_btn_clicked(self):

        random_string = self.generate_random_string(18)
        random_string_with_path = "./" +random_string  + ".enc.flac.GitDiarySync"
        md_random_string = " ![  " + random_string + "  ](" + random_string_with_path + ") "

        if random_string:
            #self.recorder.save_audio(file_path)
            self.recorder.save_encrypted_audio(random_string_with_path, self.passwd)
            self.toggle_btn.setText('New')

#################################################################


