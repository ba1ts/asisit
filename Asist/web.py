from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QLineEdit, QListWidget, QTextEdit, QWidget, QHBoxLayout, QVBoxLayout, QGroupBox, QButtonGroup, QRadioButton, QPushButton, QLabel, QFormLayout)


app = QApplication([])
btn = QPushButton('Нажми!')
main = QWidget()
row1 = QHBoxLayout()
row1.addWidget(btn)
main.resize(100,100)
btn.setText('хз что ставить')
main.setLayout(row1)
main.show()
app.exec_()
