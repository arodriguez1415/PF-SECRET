from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication

from src.Classes.Project_mastermind import Project_mastermind


def start_progress_bar(process_title, process_description, progress_steps, is_global=False):
    project_mastermind = Project_mastermind.get_instance()
    if project_mastermind.is_global_progress_bar_active():
        return
    elif is_global:
        start_global_progress_bar(process_title, progress_steps)
    else:
        start_normal_progress_bar(process_title, process_description, progress_steps)


def start_global_progress_bar(process_title, progress_steps):
    project_mastermind = Project_mastermind.get_instance()
    project_mastermind.reset_global_progress_bar()
    set_global_progress_bar_active()
    progress_bar = project_mastermind.get_global_progress_bar()
    progress_bar = setup_progress_bar(progress_bar, process_title, "", progress_steps=progress_steps)
    project_mastermind.set_global_progress_bar(progress_bar)


def start_normal_progress_bar(process_title, process_description, progress_steps):
    project_mastermind = Project_mastermind.get_instance()
    project_mastermind.reset_normal_progress_bar()
    progress_bar = project_mastermind.get_normal_progress_bar()
    progress_bar = setup_progress_bar(progress_bar, process_title, process_description, progress_steps=progress_steps)
    project_mastermind.set_normal_progress_bar(progress_bar)


def setup_progress_bar(progress_bar, process_title, process_description, progress_steps=100):
    progress_bar.setWindowTitle(process_title)
    progress_bar.setWindowModality(Qt.WindowModal)
    progress_bar.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowTitleHint)
    progress_bar.setLabelText(process_description)
    progress_bar.setMinimumDuration(0)
    progress_bar.setMaximum(progress_steps)
    progress_bar.setValue(0)
    progress_bar.show()
    QApplication.processEvents()
    return progress_bar


def set_global_description(process_description):
    project_mastermind = Project_mastermind.get_instance()
    global_progress_bar = project_mastermind.get_global_progress_bar()
    global_progress_bar.setLabelText(process_description)


def increment_value_progress_bar():
    project_mastermind = Project_mastermind.get_instance()
    progress_bar = get_progress_bar()

    if progress_bar is None:
        return
    current_value = progress_bar.value()
    progress_bar.setValue(current_value + 1)

    if project_mastermind.is_global_progress_bar_active():
        description = "Rutina global: Pasos " + str(current_value) + " de " + str(progress_bar.maximum())
        set_global_description(description)

    if progress_bar.value() == progress_bar.maximum():
        project_mastermind = Project_mastermind.get_instance()
        project_mastermind.set_global_progress_bar_active(False)


def get_progress_bar():
    project_mastermind = Project_mastermind.get_instance()
    if project_mastermind.is_global_progress_bar_active():
        return project_mastermind.get_global_progress_bar()
    return project_mastermind.get_normal_progress_bar()


def set_global_progress_bar_active(flag=True):
    project_mastermind = Project_mastermind.get_instance()
    project_mastermind.set_global_progress_bar_active(flag)


def force_to_close():
    project_mastermind = Project_mastermind.get_instance()
    progress_bar = get_progress_bar()
    if progress_bar is not None:
        project_mastermind.set_global_progress_bar_active(False)
        progress_bar.done(0)




def is_progress_bar_cancelled():
    progress_bar = get_progress_bar()
    if progress_bar is not None and progress_bar.wasCanceled():
        exit()
        project_mastermind = Project_mastermind.get_instance()
        project_mastermind.set_global_progress_bar_active(False)
        progress_bar.close()
        return True
    return False
