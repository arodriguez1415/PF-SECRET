import asyncio
import threading
import time

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QMessageBox, QProgressDialog, QApplication, QProgressBar

from src.Constants import string_constants


def show_message(message_description):
    messageBox = QMessageBox()
    font = QFont("Tokyo")
    font.setPointSize(18)
    messageBox.setFont(font)
    messageBox.setText(message_description)
    messageBox.exec()


def show_information_message(information_description):
    messageBox = QMessageBox()
    messageBox.setWindowTitle(string_constants.INFORMATION_TITLE)
    messageBox.setText(information_description)
    messageBox.exec()


def show_error(error_description):
    messageBox = QMessageBox()
    messageBox.setText(error_description)
    messageBox.exec()


def show_wait_message(title, message):
    messageBox = QMessageBox()
    messageBox.setWindowTitle(title)
    messageBox.setWindowModality(Qt.WindowModal)
    messageBox.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowTitleHint)
    messageBox.setStandardButtons(QMessageBox.NoButton)
    messageBox.setText(message)
    messageBox.show()
    QApplication.processEvents()
    return messageBox


def increment_wait_message(progress_bar_window):
    for i in range(0, progress_bar_window.maximum()):
        progress_bar_window.setValue(progress_bar_window.value() + 1)
        time.sleep(0.1)
    return


def show_confirmation_message(title, message):
    msgBox = QMessageBox()
    msgBox.setText(title)
    msgBox.setInformativeText(message)
    msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
    msgBox.setDefaultButton(QMessageBox.Cancel)
    button_continue = msgBox.button(QMessageBox.Ok)
    button_continue.setText(string_constants.CONTINUE_BUTTON_TEXT)
    button_cancel = msgBox.button(QMessageBox.Cancel)
    button_cancel.setText(string_constants.CANCEL_BUTTON_TEXT)
    ret = msgBox.exec_()
    if ret == QMessageBox.Ok:
        return True
    return False
