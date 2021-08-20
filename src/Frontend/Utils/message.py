from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox, QApplication

from src.Classes.Project_mastermind import Project_mastermind
from src.Constants import string_constants


def show_information_message(information_description):
    messageBox = QMessageBox()
    messageBox.setWindowTitle(string_constants.INFORMATION_TITLE)
    messageBox.setText(information_description)
    messageBox.exec()


def show_error_message(error_description):
    messageBox = QMessageBox()
    messageBox.setWindowTitle(string_constants.ERROR_TITLE)
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
    project_mastermind = Project_mastermind.get_instance()
    project_mastermind.set_wait_message(messageBox)
    return messageBox


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
