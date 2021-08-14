from PyQt5.QtCore import QCoreApplication


def disable_button(button):
    button.setEnabled(False)
    QCoreApplication.processEvents()


def enable_button(button):
    button.setEnabled(True)
    QCoreApplication.processEvents()


def is_enabled(button):
    return button.isEnabled()


def select_button(button):
    button.setStyleSheet("background-color: #99BBF5;")


def deselect_button(button):
    button.setStyleSheet("QPushButton{background-color: transparent;}" +
                         "QPushButton:hover{background-color: #99BBF5;}"
                         "QPushButton:disabled{background-color: #cccccc;}"
                        )


def deselect_all(main_window):
    deselect_button(main_window.polygon_region_button)
    deselect_button(main_window.square_region_button)
    deselect_button(main_window.fixed_square_region_button)
    deselect_button(main_window.horizontal_line_button)
    deselect_button(main_window.vertical_line_button)
    deselect_button(main_window.diagonal_line_button)
