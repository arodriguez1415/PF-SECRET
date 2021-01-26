from src.Classes.Methods.Mgac import Mgac
from src.Classes.Project_image import Project_image
from src.Classes.Region import Region
from src.Classes.Project_mastermind import Project_mastermind
from src.Backend.Image_processing_algorithms.Border_detection.mgac import *
from PIL import Image


def configure_border_detection_menu_connections(main_window):
    stacked_feature_windows = main_window.stacked_feature_windows
    main_window.mgac_menu_option.triggered.connect(lambda: load_mgac_options(stacked_feature_windows))
    main_window.apply_mgac_button.clicked.connect(lambda: mgac(main_window))


def load_mgac_options(stacked_feature_windows):
    stacked_feature_windows.setCurrentIndex(1)


def mgac(main_window):
    project_mastermind = Project_mastermind.get_instance()
    polygon_region = Region().get_region()
    image_array = project_mastermind.get_last_image()
    image = Image.fromarray(image_array)
    iterations = int(main_window.iterations_mgac_input.text())
    threshold = float(main_window.threshold_mgac_input.text())
    smoothing = int(main_window.smoothing_mgac_input.text())
    balloon = int(main_window.balloon_mgac_input.text())
    alpha = int(main_window.alpha_mgac_input.text())
    sigma = int(main_window.sigma_mgac_input.text())
    final_contour = mgac_border_detection(polygon_region, image, iterations, threshold,
                                          smoothing, balloon, alpha, sigma)
    mgac_method = Mgac(polygon_region, iterations, threshold, smoothing, balloon, alpha, sigma)
    save_image_path = project_mastermind.create_stage_path_name(mgac_method.name)
    save_image_with_contours(image, final_contour, save_image_path)
    # mask_contour_image = save_image_with_contours_mask(image, final_contour, save_image_path)
    image_wrapper = Project_image(save_image_path, mgac_method)
    project_mastermind.add_image_process(image_wrapper)
    main_window.image_viewer.clear_region()
    main_window.image_viewer.set_screen_image(image_wrapper)
