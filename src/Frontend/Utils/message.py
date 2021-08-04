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


def show_confirmation_message(title, message):
    msgBox = QMessageBox()
    msgBox.setText(title)
    msgBox.setInformativeText(message)
    msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
    msgBox.setDefaultButton(QMessageBox.Cancel)
    button_continue = msgBox.button(QMessageBox.Ok)
    button_continue.setText("Continuar")
    button_cancel = msgBox.button(QMessageBox.Cancel)
    button_cancel.setText("Cancelar")
    ret = msgBox.exec_()
    if ret == QMessageBox.Ok:
        return True
    return False
