from PyQt5.QtCore import QCoreApplication


def disable_button(button):
    button.setEnabled(False)
    QCoreApplication.processEvents()


def enable_button(button):
    button.setEnabled(True)
    QCoreApplication.processEvents()


def is_enabled(button):
    return button.isEnabled()
