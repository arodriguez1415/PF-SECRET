from PyQt5.QtCore import Qt

from src.Classes.Project_mastermind import Project_mastermind


def start_progress_bar(process_title, process_description, progress_steps=100):
    project_mastermind = Project_mastermind.get_instance()
    project_mastermind.reset_current_progress_bar()
    progress_bar = project_mastermind.get_current_progress_bar()
    progress_bar.setWindowTitle(process_title)
    progress_bar.setWindowModality(Qt.WindowModal)
    progress_bar.show()
    progress_bar.setMinimum(0)
    progress_bar.setMaximum(progress_steps)
    progress_bar.setValue(0)
    progress_bar.setLabelText(process_description)
    project_mastermind.set_current_progress_bar(progress_bar)


def set_progress_bar_steps(progress_steps):
    project_mastermind = Project_mastermind.get_instance()
    progress_bar = project_mastermind.get_current_progress_bar()
    progress_bar.setMaximum(progress_steps)


def increment_value_progress_bar():
    project_mastermind = Project_mastermind.get_instance()
    progress_bar = project_mastermind.get_current_progress_bar()
    current_value = progress_bar.value()
    progress_bar.setValue(current_value + 1)


def is_progress_bar_cancelled():
    project_mastermind = Project_mastermind.get_instance()
    progress_bar = project_mastermind.get_current_progress_bar()
    if progress_bar.wasCanceled():
        progress_bar.close()
        return True
    return False
