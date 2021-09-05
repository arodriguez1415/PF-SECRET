from PIL import Image

from src.Backend.Image_processing_algorithms.Archive_manipulation.properties_manipulation import \
    save_anisotropic_filter_params
from src.Backend.Image_processing_algorithms.filters import anisotropic_filter as anisotropic_filter_functions
from src.Classes.Image_wrapper import Image_wrapper
from src.Classes.Methods.Anisotropic_Filter import Anisotropic_Filter
from src.Classes.Project_mastermind import Project_mastermind
from src.Constants import string_constants
from src.Frontend.Utils.button_controller import disable_button, enable_button
from src.Frontend.Utils.message import show_error_message


def configure_filter_menu_connections(main_window):
    main_window.anisotropic_filter_menu_option_2.triggered.connect(
        lambda: load_anisotropic_options(main_window))

    main_window.apply_anisotropic_filter_button.clicked.connect(lambda: anisotropic_filter(main_window))


def load_anisotropic_options(main_window):
    page = main_window.anisotropic_filter_options
    stacked_feature_windows = main_window.stacked_feature_windows
    stacked_feature_windows.setCurrentWidget(page)
    return


def anisotropic_filter(main_window):
    disable_button(main_window.apply_anisotropic_filter_button)
    project_mastermind = Project_mastermind.get_instance()
    image_array = project_mastermind.get_last_image()

    if image_array is None:
        show_error_message(string_constants.NO_IMAGE_LOADED)
        enable_button(main_window.apply_anisotropic_filter_button)
        return

    iterations = main_window.apply_anisotropic_filter_times_input.value()
    image = Image.fromarray(image_array)
    image_filtered_array = anisotropic_filter_functions.anisotropic_diffusion_filter_medpy(image, iterations)
    anisotropic_method = Anisotropic_Filter(iterations)
    image_wrapper = Image_wrapper(image_filtered_array, anisotropic_method)
    project_mastermind.add_image_process(image_wrapper)
    main_window.image_viewer.set_screen_image(image_wrapper)
    save_anisotropic_filter_params(main_window)
    enable_button(main_window.apply_anisotropic_filter_button)
