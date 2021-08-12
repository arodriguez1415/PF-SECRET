from src.Classes.Project_mastermind import Project_mastermind


def configure_window(process_list):
    process_list.process_widget_close_button.clicked.connect(lambda: dismiss_window())


def dismiss_window():
    project_mastermind = Project_mastermind.get_instance()
    project_mastermind.process_list_widget.done(0)