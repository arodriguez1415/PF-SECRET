from src.Backend.Image_processing_algorithms.Archive_manipulation.properties_manipulation import save_mgac_params
from src.Backend.Image_processing_algorithms.Operations.common_operations import resize_image
from src.Classes.Image_wrapper import Image_wrapper
from src.Classes.Methods.Mgac import Mgac
from src.Classes.Region import Region
from src.Classes.Project_mastermind import Project_mastermind
from src.Backend.Image_processing_algorithms.Border_detection import mgac as mgac_functions
from PIL import Image

from src.Constants import configuration_constants
from src.Frontend.Utils.button_controller import disable_button, enable_button


def configure_border_detection_menu_connections(main_window):
    main_window.mgac_border_detection_menu_option.triggered.connect(lambda: load_mgac_options(main_window))
    main_window.apply_mgac_button.clicked.connect(lambda: detect_borders(main_window))


def load_mgac_options(main_window):
    page = main_window.mgac_options
    stacked_feature_windows = main_window.stacked_feature_windows
    stacked_feature_windows.setCurrentWidget(page)
    return


def detect_borders(main_window):
    disable_button(main_window.apply_mgac_button)
    project_mastermind = Project_mastermind.get_instance()
    polygon_region = Region()
    polygon_region.get_region()
    image_array = project_mastermind.get_last_image()
    width, height = configuration_constants.IMAGE_VIEWER_WIDTH, configuration_constants.IMAGE_VIEWER_HEIGHT
    resized_image_array = resize_image(image_array, width, height)
    image = Image.fromarray(resized_image_array)
    iterations = main_window.iterations_mgac_input.value()
    threshold = main_window.threshold_mgac_input.value()
    smoothing = main_window.smoothing_mgac_input.value()
    balloon = main_window.balloon_mgac_input.value()
    alpha = main_window.alpha_mgac_input.value()
    sigma = main_window.sigma_mgac_input.value()
    borders_image, mask_image = mgac_functions.mgac(polygon_region.points, image, iterations,
                                                    threshold, smoothing, balloon, alpha, sigma, show_process=True)
    mgac_method = Mgac(polygon_region.points, iterations, threshold, smoothing, balloon, alpha, sigma)
    image_wrapper = Image_wrapper(borders_image, mgac_method)
    project_mastermind.add_image_process(image_wrapper)
    main_window.image_viewer.set_screen_image(image_wrapper)
    save_mgac_params(main_window)
    enable_button(main_window.apply_mgac_button)

