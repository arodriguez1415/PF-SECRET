from src.Backend.Video_processing_algorithms.video_generator import generate_video
from src.Classes.Project_mastermind import Project_mastermind
from src.Constants import string_constants
from src.Frontend.Utils.button_controller import enable_button, disable_button
from src.Frontend.Utils.message import show_error_message


def configure_video_menu_connections(main_window):
    main_window.generate_video_with_process_menu_option.triggered.connect(lambda: load_video_options(main_window))

    main_window.generate_video_algorithm_button.clicked.connect(lambda: generate_video_from_process(main_window))


def load_video_options(main_window):
    page = main_window.generate_video_options
    stacked_feature_windows = main_window.stacked_feature_windows
    stacked_feature_windows.setCurrentWidget(page)
    return


def generate_video_from_process(main_window):
    disable_button(main_window.generate_video_algorithm_button)
    project_mastermind = Project_mastermind.get_instance()
    if project_mastermind.get_last_image() is None:
        show_error_message(string_constants.NO_IMAGE_LOADED)
        enable_button(main_window.generate_video_algorithm_button)
        return

    generate_video()
    enable_button(main_window.generate_video_algorithm_button)
