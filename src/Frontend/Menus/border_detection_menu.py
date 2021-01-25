from src.Classes.Region import Region
from src.Classes.Project_mastermind import Project_mastermind
from src.Backend.Image_processing_algorithms.Border_detection.mgac import mgac_process
from PIL import Image


def configure_border_detection_menu_connections(main_window):
    stacked_feature_windows = main_window.stacked_feature_windows
    main_window.mgac_menu_option.triggered.connect(lambda: load_mgac_options(stacked_feature_windows))
    main_window.apply_mgac_button.clicked.connect(lambda: mgac(main_window))


def load_mgac_options(stacked_feature_windows):
    stacked_feature_windows.setCurrentIndex(1)


def mgac(main_window):
    polygon_region = Region().get_square_region()
    image_array = Project_mastermind.get_instance().get_last_image()
    pil_image = Image.fromarray(image_array)
    iterations = int(main_window.iterations_mgac_input.text())
    threshold = float(main_window.threshold_mgac_input.text())
    smoothing = int(main_window.smoothing_mgac_input.text())
    balloon = int(main_window.balloon_mgac_input.text())
    alpha = int(main_window.alpha_mgac_input.text())
    sigma = int(main_window.sigma_mgac_input.text())
    print(sigma + alpha)
    mgac_process(polygon_region, pil_image, iterations, threshold, smoothing, balloon, alpha, sigma)

