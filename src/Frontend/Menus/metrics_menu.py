from src.Backend.Image_processing_algorithms.Archive_manipulation import dataframe_file_manipulation
from src.Backend.Image_processing_algorithms.Archive_manipulation import video_file_manipulation
from src.Backend.Image_processing_algorithms.Metrics import metrics_generator, metrics_plotter
from src.Backend.Image_processing_algorithms.Operations.common_operations import resize_image, normalize_to_range
from src.Classes.Project_mastermind import Project_mastermind
from src.Classes.QDrawable_label import QDrawable_label
from src.Classes.Region import Region
from src.Constants import algorithm_constants, configuration_constants
from src.Constants.string_constants import ORIGINAL_TITLE, MOVEMENT_TITLE, TEXTURE_VIDEO_TITLE, TEXTURE_IMAGE_TITLE, \
    FOUR_GRID_COMPARISON
from src.Frontend.Utils.button_controller import disable_button, enable_button
from src.Frontend.Utils.plot_comparator import plot_four_comparison


def configure_metrics_menu_connections(main_window):
    main_window.generate_metrics_menu_option.triggered.connect(lambda: load_generate_metrics_options(main_window))
    main_window.plot_metrics_menu_option.triggered.connect(lambda: load_plot_metrics_options(main_window))
    main_window.plot_distribution_metric_menu_option.triggered.connect(lambda:
                                                                       load_plot_distribution_metrics_option
                                                                       (main_window))

    main_window.analize_texture_and_movement_metrics_menu_option.triggered.connect(lambda:
                                                                                   load_analyze_texture_and_movement_options
                                                                                   (main_window))

    main_window.generate_metrics_load_mask_video_button.clicked.connect(lambda: load_mask_video_path(main_window))
    main_window.plot_metrics_load_dataframe_button.clicked.connect(lambda: load_metrics_data_path(main_window))
    main_window.generate_metrics_generate_button.clicked.connect(lambda: generate_metrics(main_window))
    main_window.plot_metrics_generate_button.clicked.connect(lambda: plot_metrics(main_window))
    main_window.plot_metrics_distribution_button.clicked.connect(lambda: plot_distribution_metrics(main_window))
    main_window.analyze_movement_and_texture_button.clicked.connect(lambda:
                                                                    analyze_texture_and_movement_metrics(main_window))


def load_generate_metrics_options(main_window):
    page = main_window.generate_metrics_options
    stacked_feature_windows = main_window.stacked_feature_windows
    stacked_feature_windows.setCurrentWidget(page)
    return


def load_plot_metrics_options(main_window):
    page = main_window.plot_metrics_options
    stacked_feature_windows = main_window.stacked_feature_windows
    stacked_feature_windows.setCurrentWidget(page)
    return


def load_plot_distribution_metrics_option(main_window):
    page = main_window.plot_distribution_metrics_option
    stacked_feature_windows = main_window.stacked_feature_windows
    stacked_feature_windows.setCurrentWidget(page)
    return


def load_analyze_texture_and_movement_options(main_window):
    page = main_window.movement_and_texture_metrics_options
    stacked_feature_windows = main_window.stacked_feature_windows
    stacked_feature_windows.setCurrentWidget(page)
    return


def load_mask_video_path(main_window):
    disable_button(main_window.generate_metrics_load_mask_video_button)
    mask_video_path = video_file_manipulation.get_video_path()
    main_window.generate_metrics_mask_video_input.setText(mask_video_path)
    enable_button(main_window.generate_metrics_load_mask_video_button)


def load_metrics_data_path(main_window):
    disable_button(main_window.plot_metrics_load_dataframe_button)
    dataframe_path = dataframe_file_manipulation.get_dataframe_path()
    main_window.plot_metrics_dataframe_input.setText(dataframe_path)
    enable_button(main_window.plot_metrics_load_dataframe_button)


def generate_metrics(main_window):
    disable_button(main_window.generate_metrics_generate_button)
    mask_video_path = main_window.generate_metrics_mask_video_input.text()
    metrics_dictionary = get_generation_metrics_dictionary(main_window)
    metrics_generator.generate_metrics(mask_video_path, metrics_dictionary)
    enable_button(main_window.generate_metrics_generate_button)


def get_generation_metrics_dictionary(main_window):
    metrics_dictionary = {}

    is_perimeter_checked = main_window.generate_metrics_perimeter_checkbox.isChecked()
    metrics_dictionary[algorithm_constants.PERIMETER_METRIC] = is_perimeter_checked

    is_area_checked = main_window.generate_metrics_area_checkbox.isChecked()
    metrics_dictionary[algorithm_constants.AREA_METRIC] = is_area_checked

    is_axis_rate_checked = main_window.generate_metrics_axis_rate_checkbox.isChecked()
    metrics_dictionary[algorithm_constants.AXIS_RATE_METRIC] = is_axis_rate_checked

    return metrics_dictionary


def plot_metrics(main_window):
    disable_button(main_window.plot_metrics_generate_button)
    metrics_data_path = main_window.plot_metrics_dataframe_input.text()
    metrics_dictionary = get_plotting_metrics_dictionary(main_window)
    metrics_values_lists, frames_values_lists, titles_list, x_label_list, y_label_list = metrics_plotter.load_metrics(
        metrics_data_path, metrics_dictionary)
    metrics_plotter.plot_metrics(metrics_values_lists, frames_values_lists, titles_list, x_label_list, y_label_list)
    enable_button(main_window.plot_metrics_generate_button)


def get_plotting_metrics_dictionary(main_window):
    metrics_dictionary = {}

    is_perimeter_checked = main_window.plot_metrics_perimeter_checkbox.isChecked()
    metrics_dictionary[algorithm_constants.PERIMETER_METRIC] = is_perimeter_checked

    is_area_checked = main_window.plot_metrics_area_checkbox.isChecked()
    metrics_dictionary[algorithm_constants.AREA_METRIC] = is_area_checked

    is_axis_rate_checked = main_window.plot_metrics_axis_rate_checkbox.isChecked()
    metrics_dictionary[algorithm_constants.AXIS_RATE_METRIC] = is_axis_rate_checked

    return metrics_dictionary


def plot_distribution_metrics(main_window):
    disable_button(main_window.plot_metrics_distribution_button)
    metrics_data_paths = dataframe_file_manipulation.get_multiple_dataframes_path()
    distribution_metrics_dictionary = get_plotting_distribution_metrics_dictionary(main_window)
    metrics_avg_lists, titles_list, x_label_list, y_label_list = metrics_plotter.load_distribution_metrics(
        metrics_data_paths, distribution_metrics_dictionary)
    metrics_plotter.plot_distribution_metrics(metrics_avg_lists, titles_list, x_label_list, y_label_list)
    enable_button(main_window.plot_metrics_distribution_button)


def get_plotting_distribution_metrics_dictionary(main_window):
    metrics_dictionary = {}

    is_perimeter_checked = main_window.plot_metrics_distribution_perimeter_checkbox.isChecked()
    metrics_dictionary[algorithm_constants.PERIMETER_METRIC] = is_perimeter_checked

    is_area_checked = main_window.plot_metrics_distribution_area_checkbox.isChecked()
    metrics_dictionary[algorithm_constants.AREA_METRIC] = is_area_checked

    is_axis_rate_checked = main_window.plot_metrics_distribution_axis_rate_checkbox.isChecked()
    metrics_dictionary[algorithm_constants.AXIS_RATE_METRIC] = is_axis_rate_checked

    return metrics_dictionary


def analyze_texture_and_movement_metrics(main_window):
    disable_button(main_window.analyze_movement_and_texture_button)
    project_mastermind = Project_mastermind.get_instance()

    original_array = project_mastermind.get_original_image()
    movement_array = project_mastermind.get_movement_image().image_array

    show_movement_array = project_mastermind.get_movement_heat_map_image().image_array
    show_texture_image_array = project_mastermind.get_texture_heat_map_image().image_array
    show_texture_video_array = project_mastermind.get_texture_heat_map_image_video().image_array

    width, height = configuration_constants.IMAGE_VIEWER_WIDTH, configuration_constants.IMAGE_VIEWER_HEIGHT
    weight_image_array = [original_array, movement_array, show_texture_image_array, show_texture_video_array]
    show_images_array = [original_array, show_movement_array, show_texture_image_array, show_texture_video_array]
    avg_values_array = []

    region = Region()
    square_region = region.get_region()
    for i in range(0, len(weight_image_array)):
        show_image_array = resize_image(show_images_array[i], width, height)
        wight_image_array = resize_image(weight_image_array[i], width, height)
        pixels_in_region = region.get_pixels_in_region(wight_image_array)
        normalized_pixels_in_region = normalize_to_range(pixels_in_region, max_value=255)
        show_images_array[i] = QDrawable_label.draw_region_in_image(show_image_array, square_region)
        avg_values_array.append(normalized_pixels_in_region.mean())

    avg_results = "Promedio de valor de pixel escala grises: " + str(round(avg_values_array[0], 2)) + "\n"
    avg_results += "Promedio de valor de pixel de movimiento: " + str(round(avg_values_array[1], 2)) + "\n"
    avg_results += "Promedio de valor de pixel de textura de imagen: " + str(round(avg_values_array[2], 2)) + "\n"
    avg_results += "Promedio de valor de pixel de textura de video: " + str(round(avg_values_array[3], 2))
    title = FOUR_GRID_COMPARISON
    sub_titles = [ORIGINAL_TITLE, MOVEMENT_TITLE, TEXTURE_IMAGE_TITLE, TEXTURE_VIDEO_TITLE]
    plot_four_comparison(show_images_array, title, sub_titles, avg_results)
    enable_button(main_window.analyze_movement_and_texture_button)
