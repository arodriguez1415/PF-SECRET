from src.Constants import string_constants
from src.Frontend.Utils.message import show_information_message


def configure_information_buttons(main_window):
    main_window.adaptive_threshold_window_size_help.clicked.connect(lambda: show_information(string_constants.ADAPTIVE_THRESHOLD_SIZE_HELP))
    main_window.adaptive_threshold_c_constant_help.clicked.connect(lambda: show_information(string_constants.ADAPTIVE_THRESHOLD_SIZE_CONSTANT))
    main_window.adaptive_threshold_method_help.clicked.connect(lambda: show_information(string_constants.ADAPTIVE_THRESHOLD_SIZE_METHOD))

def show_information(message_id):
    show_information_message(message_id)
    return
