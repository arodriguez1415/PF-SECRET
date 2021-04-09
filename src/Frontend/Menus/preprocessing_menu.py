from src.Classes.Image_wrapper import Image_wrapper
from src.Classes.Methods.Adaptive_threshold import Adaptive_threshold
from src.Classes.Project_mastermind import Project_mastermind
from src.Backend.Image_processing_algorithms.Preprocessing import adaptive_threshold


def configure_preprocessing_menu_connections(main_window):
    main_window.adaptive_threshold_preprocessing_menu_option.triggered. \
        connect(lambda: adaptive_threshold_options(main_window))

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


def show_adaptive_threshold(main_window):
    project_mastermind = Project_mastermind.get_instance()
    window_size_slider = main_window.adaptive_threshold_window_size_spinner
    c_constant_slider = main_window.adaptive_threshold_c_constant_spinner
    method_box = main_window.adaptive_threshold_method_box

    current_image_array = project_mastermind.get_last_image()
    window_size = int(window_size_slider.value())
    constant = int(c_constant_slider.value())
    method = int(adaptive_threshold.get_method(method_box.currentText()))

    if window_size % 2 == 0:
        window_size = window_size + 1

    lpb_image = adaptive_threshold.adaptive_threshold(current_image_array, method, window_size, constant)
    adaptive_threshold_method = Adaptive_threshold(window_size, constant, method)
    image_wrapper = Image_wrapper(lpb_image, adaptive_threshold_method)
    main_window.image_viewer.set_screen_image(image_wrapper)


def add_process(main_window):
    actual_image_wrapper = main_window.image_viewer.actual_image_wrapper
    project_mastermind = Project_mastermind.get_instance()
    project_mastermind.add_image_process(actual_image_wrapper)
