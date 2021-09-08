from src.Backend.Video_processing_algorithms.video_generator import generate_video
from src.Classes.Methods.Mgac import Mgac
from src.Classes.Project_mastermind import Project_mastermind
from src.Constants import string_constants
from src.Frontend.Utils.button_controller import enable_button, disable_button
from src.Frontend.Utils.message import show_error_message, show_confirmation_message


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
    mask_flag = False
    if project_mastermind.get_last_image() is None:
        show_error_message(string_constants.NO_IMAGE_LOADED)
        enable_button(main_window.generate_video_algorithm_button)
        return

    if has_mgac_method_message():
        mask_flag = show_confirmation_message(string_constants.MGAC_GENERATE_VIDEO_TITLE,
                                              string_constants.MGAC_GENERATE_VIDEO_DESCRIPTION,
                                              no_button=True)

    if mask_flag:
        set_mgac_mask_flag(mask_flag)

    generate_video()
    set_mgac_mask_flag(False)
    enable_button(main_window.generate_video_algorithm_button)


def has_mgac_method_message():
    project_mastermind = Project_mastermind.get_instance()
    process_list = project_mastermind.get_image_processing_list()
    for i in range(0, len(process_list)):
        process = process_list[i].get_method()
        if isinstance(process, Mgac):
            return True
    return False


def set_mgac_mask_flag(flag):
    project_mastermind = Project_mastermind.get_instance()
    process_list = project_mastermind.get_image_processing_list()
    for i in range(0, len(process_list)):
        process = process_list[i].get_method()
        if isinstance(process, Mgac):
            process_list[i].get_method().set_mask_flag(flag)
