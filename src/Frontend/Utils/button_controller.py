from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QPushButton


def disable_button(button):
    button.setEnabled(False)
    QCoreApplication.processEvents()


def enable_button(button):
    button.setEnabled(True)
    QCoreApplication.processEvents()


def is_enabled(button):
    return button.isEnabled()


def set_pushed_button(button):
    button.setStyleSheet("border: 2px solid #3232C0;")
