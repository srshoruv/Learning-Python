from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout
from random import choice
import webbrowser

words = ['Shahidur', 'Rahman', 'Zaman', 'Shoruv', 'Shahid', 'Sourav']

# App Objects
app = QApplication([])
main_window = QWidget()
main_window.setWindowTitle("Random Word Generator")
main_window.resize(300,200)

title = QLabel("Random Words")
text1 = QLabel("?")
text2 = QLabel("?")
text3 = QLabel("?")

button1 = QPushButton("Click to Change")
button2 = QPushButton("Click to Change")
button3 = QPushButton("Click to Change")

# App Designs
master_layout = QVBoxLayout()

row1 = QHBoxLayout()
row2 = QHBoxLayout()
row3 = QHBoxLayout()

row1.addWidget(title, alignment=Qt.AlignCenter)

row2.addWidget(text1, alignment=Qt.AlignCenter)
row2.addWidget(text2, alignment=Qt.AlignCenter)
row2.addWidget(text3, alignment=Qt.AlignCenter)

row3.addWidget(button1)
row3.addWidget(button2)
row3.addWidget(button3)

master_layout.addLayout(row1)
master_layout.addLayout(row2)
master_layout.addLayout(row3)

main_window.setLayout(master_layout)

# Functions

def random_word1():
    word = choice(words)
    text1.setText(word)

def random_word2():
    word = choice(words)
    text2.setText(word)

def random_word3():
    word = choice(words)
    text3.setText(word)

# Events

button1.clicked.connect(random_word1)
button2.clicked.connect(random_word2)
button3.clicked.connect(random_word3)


# Show/Hide App
main_window.show()
app.exec_()