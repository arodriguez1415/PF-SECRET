from src.Classes.Image_wrapper import Image_wrapper
from src.Classes.Methods.Mgac import Mgac
from src.Classes.Region import Region
from src.Classes.Project_mastermind import Project_mastermind
from src.Backend.Image_processing_algorithms.Border_detection import mgac as mgac_functions
from PIL import Image


def configure_border_detection_menu_connections(main_window):
    main_window.mgac_border_detection_menu_option.triggered.connect(lambda: load_mgac_options(main_window))
    main_window.apply_mgac_button.clicked.connect(lambda: mgac(main_window))


def load_mgac_options(main_window):
    page = main_window.mgac_options
    stacked_feature_windows = main_window.stacked_feature_windows
    stacked_feature_windows.setCurrentWidget(page)
    return


def mgac(main_window):
    project_mastermind = Project_mastermind.get_instance()
    polygon_region = Region()
    polygon_region.get_region()
    image_array = project_mastermind.get_last_image()
    image = Image.fromarray(image_array)
    iterations = int(main_window.iterations_mgac_input.text())
    threshold = float(main_window.threshold_mgac_input.text())
    smoothing = int(main_window.smoothing_mgac_input.text())
    balloon = int(main_window.balloon_mgac_input.text())
    alpha = int(main_window.alpha_mgac_input.text())
    sigma = int(main_window.sigma_mgac_input.text())
    borders_image = mgac_functions.mgac_borders(polygon_region.points, image, iterations,
                                                threshold, smoothing, balloon, alpha, sigma)
    mgac_method = Mgac(polygon_region.points, iterations, threshold, smoothing, balloon, alpha, sigma)
    image_wrapper = Image_wrapper(borders_image, mgac_method)
    project_mastermind.add_image_process(image_wrapper)
    main_window.image_viewer.set_screen_image(image_wrapper)


def mgac_only_cell(main_window):
    project_mastermind = Project_mastermind.get_instance()
    image_array = project_mastermind.get_last_image()
    cell_image = mgac_functions.mgac_only_cell(image_array)
    image_wrapper = Image_wrapper(cell_image)
    project_mastermind.add_image_process(image_wrapper)
    main_window.image_viewer.set_screen_image(image_wrapper)
