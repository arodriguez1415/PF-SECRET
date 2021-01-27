from src.Backend.Image_processing_algorithms.filters import anisotropic_filter as anisotropic_filter_functions
from src.Backend.Image_processing_algorithms.filters import bilateral_filter as bilateral_filter_functions
from src.Classes.Methods.Anisotropic_Filter import Anisotropic_Filter
from src.Classes.Methods.Bilateral_Filter import Bilateral_Filter
from src.Classes.Project_mastermind import Project_mastermind
from src.Classes.Project_image import Project_image
from PIL import Image

def configure_filter_menu_connections(main_window):
    stacked_feature_windows = main_window.stacked_feature_windows
    main_window.anisotropic_filter_menu_option.triggered.connect(
        lambda: load_anisotropic_options(stacked_feature_windows))
    main_window.bilateral_filter_menu_option.triggered.connect(
        lambda: load_bilateral_options(stacked_feature_windows))
    main_window.apply_anisotropic_filter_button.clicked.connect(lambda: anisotropic_filter(main_window))
    main_window.apply_bilateral_filter_button.clicked.connect(lambda: bilateral_filter(main_window))


def load_anisotropic_options(stacked_feature_windows):
    stacked_feature_windows.setCurrentIndex(1)
    return


def load_bilateral_options(stacked_feature_windows):
    stacked_feature_windows.setCurrentIndex(2)
    return


def anisotropic_filter(main_window):
    project_mastermind = Project_mastermind.get_instance()
    image_array = project_mastermind.get_last_image()
    image = Image.fromarray(image_array)
    image_filtered_array = anisotropic_filter_functions.anisotropic_diffusion_filter_medpy(image)
    anisotropic_filter_method = Anisotropic_Filter()
    save_image_path = project_mastermind.create_stage_path_name(anisotropic_filter_method.name)
    anisotropic_filter_functions.save_anisotropic_image(image_filtered_array, save_image_path)
    image_wrapper = Project_image(save_image_path, anisotropic_filter_method)
    project_mastermind.add_image_process(image_wrapper)
    main_window.image_viewer.set_screen_image(image_wrapper)


def bilateral_filter(main_window):
    project_mastermind = Project_mastermind.get_instance()
    image_array = project_mastermind.get_last_image()
    image = Image.fromarray(image_array)
    sigma_r = int(main_window.sigma_r_bilateral_filter_input.text())
    sigma_s = int(main_window.sigma_s_bilateral_filter_input.text())
    window_size = int(main_window.window_size_bilateral_filter_input.text())
    image_filtered_array = bilateral_filter_functions.bilateral_filter(image, sigma_r, sigma_s, window_size)
    bilateral_filter_method = Bilateral_Filter(sigma_r, sigma_s, window_size)
    save_image_path = project_mastermind.create_stage_path_name(bilateral_filter_method.name)
    bilateral_filter_functions.save_bilateral_image(image_filtered_array, save_image_path)
    image_wrapper = Project_image(save_image_path, bilateral_filter_method)
    project_mastermind.add_image_process(image_wrapper)
    main_window.image_viewer.set_screen_image(image_wrapper)