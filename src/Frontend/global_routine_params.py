from PyQt5.QtGui import QStandardItemModel, QStandardItem

from src.Classes.Project_mastermind import Project_mastermind

def configure_window(global_routine_params):
    global_routine_params.global_routine_params_default_button.clicked.connect(lambda: set_defaults())
    global_routine_params.global_routine_params_cancel_button.clicked.connect(lambda: cancel())
    global_routine_params.global_routine_params_accept_button.clicked.connect(lambda: accept())


def set_defaults():
    print("Set defaults")


def cancel():
    project_mastermind = Project_mastermind.get_instance()
    project_mastermind.global_routine_params_widget.done(0)


def accept():
    project_mastermind = Project_mastermind.get_instance()
    project_mastermind.global_routine_params_widget.done(0)