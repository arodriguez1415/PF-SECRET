from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QMessageBox


def show_message(message_description):
    messageBox = QMessageBox()
    font = QFont("Tokyo")
    font.setPointSize(18)
    messageBox.setFont(font)
    messageBox.setText(message_description)
    messageBox.exec()


def show_error(error_description):
    messageBox = QMessageBox()
    messageBox.setText(error_description)
    messageBox.exec()