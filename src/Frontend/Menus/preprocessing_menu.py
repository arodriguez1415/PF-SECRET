from PyQt5.QtCore import Qt
from PyQt5.QtGui import QMovie

from src.Backend.Image_processing_algorithms.Archive_manipulation.properties_manipulation import \
    save_adaptive_threshold_params
from src.Classes.Image_wrapper import Image_wrapper
from src.Classes.Methods.Adaptive_threshold import Adaptive_threshold
from src.Classes.Project_mastermind import Project_mastermind
from src.Backend.Image_processing_algorithms.Preprocessing import adaptive_threshold
from src.Constants import string_constants
from src.Frontend.Utils.button_controller import disable_button, enable_button
from src.Frontend.Utils.message import show_error_message


def configure_preprocessing_menu_connections(main_window):
    main_window.adaptive_threshold_preprocessing_menu_option.triggered. \
        connect(lambda: adaptive_threshold_options(main_window))

    set_highlight(main_window)

    main_window.adaptive_threshold_window_size_spinner.valueChanged.connect(lambda: show_adaptive_threshold(main_window))
    main_window.adaptive_threshold_c_constant_spinner.valueChanged.connect(lambda: show_adaptive_threshold(main_window))
    main_window.adaptive_threshold_method_box.currentTextChanged.connect(lambda: show_adaptive_threshold(main_window))

    main_window.adaptive_threshold_add_process_button.clicked. \
        connect(lambda: add_process(main_window))
    return


def adaptive_threshold_options(main_window):
    page = main_window.adaptive_threshold_options
    stacked_feature_windows = main_window.stacked_feature_windows
    stacked_feature_windows.setCurrentWidget(page)
    return


def set_highlight(main_window):
    highlight_labels = [main_window.adaptive_threshold_highlight, main_window.adaptive_threshold_highlight_2,
                        main_window.adaptive_threshold_highlight_3]
    gif_animation = QMovie(r"./Resources/Icons/arrow.gif")
    gif_animation.start()
    for i in range(0, len(highlight_labels)):
        highlight_label = highlight_labels[i]
        highlight_label.setAttribute(Qt.WA_NoSystemBackground)
        highlight_label.setMovie(gif_animation)
        highlight_label.setVisible(False)


def show_adaptive_threshold(main_window):
    project_mastermind = Project_mastermind.get_instance()
    window_size_slider = main_window.adaptive_threshold_window_size_spinner
    c_constant_slider = main_window.adaptive_threshold_c_constant_spinner
    method_box = main_window.adaptive_threshold_method_box

    current_image_array = project_mastermind.get_last_image()

    if current_image_array is None:
        return

    window_size = window_size_slider.value()
    constant = c_constant_slider.value()
    method = int(adaptive_threshold.get_method(method_box.currentText()))

    adaptive_threshold_image = adaptive_threshold.adaptive_threshold(current_image_array, window_size, constant, method)
    adaptive_threshold_method = Adaptive_threshold(window_size, constant, method)
    image_wrapper = Image_wrapper(adaptive_threshold_image, adaptive_threshold_method)
    main_window.image_viewer.set_screen_image(image_wrapper)
    main_window.adaptive_threshold_highlight.setVisible(True)
    main_window.adaptive_threshold_highlight_2.setVisible(True)
    main_window.adaptive_threshold_highlight_3.setVisible(True)


def add_process(main_window):
    disable_button(main_window.adaptive_threshold_add_process_button)
    project_mastermind = Project_mastermind.get_instance()
    actual_image_wrapper = main_window.image_viewer.actual_image_wrapper

    if project_mastermind.get_last_image() is None:
        show_error_message(string_constants.NO_IMAGE_LOADED)
        enable_button(main_window.adaptive_threshold_add_process_button)
        return

    if actual_image_wrapper is None or not isinstance(actual_image_wrapper.get_method(), Adaptive_threshold):
        return

    project_mastermind = Project_mastermind.get_instance()
    project_mastermind.add_image_process(actual_image_wrapper)
    save_adaptive_threshold_params(main_window)
    main_window.adaptive_threshold_highlight.setVisible(False)
    main_window.adaptive_threshold_highlight_2.setVisible(False)
    main_window.adaptive_threshold_highlight_3.setVisible(False)
    enable_button(main_window.adaptive_threshold_add_process_button)
