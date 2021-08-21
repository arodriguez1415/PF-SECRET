from src.Backend.Image_processing_algorithms.Archive_manipulation.properties_manipulation import \
    save_global_routine_params, generate_global_routine_properties, set_global_routine_properties, save_properties
from src.Classes.Project_mastermind import Project_mastermind


def configure_window(global_routine_params):
    global_routine_params.global_routine_params_default_button.clicked.connect(lambda: set_defaults())
    global_routine_params.global_routine_params_cancel_button.clicked.connect(lambda: cancel())
    global_routine_params.global_routine_params_accept_button.clicked.connect(lambda: accept(global_routine_params))


def set_defaults():
    project_mastermind = Project_mastermind.get_instance()
    props_dictionary = project_mastermind.get_properties_dictionary()
    props_dictionary = generate_global_routine_properties(props_dictionary)
    project_mastermind.reload_properties(props_dictionary)
    set_global_routine_properties(props_dictionary, project_mastermind.global_routine_params)
    save_properties(props_dictionary)


def cancel():
    project_mastermind = Project_mastermind.get_instance()
    project_mastermind.global_routine_params_widget.done(0)


def accept(global_routine_params):
    save_global_routine_params(global_routine_params)
    project_mastermind = Project_mastermind.get_instance()
    project_mastermind.global_routine_params_widget.done(0)