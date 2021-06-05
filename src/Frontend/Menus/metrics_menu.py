from src.Backend.Image_processing_algorithms.Archive_manipulation import dataframe_file_manipulation
from src.Backend.Image_processing_algorithms.Archive_manipulation import video_file_manipulation
from src.Backend.Image_processing_algorithms.Texture import fractal_dimention
from src.Backend.Image_processing_algorithms.Metrics import metrics_file
from src.Backend.Image_processing_algorithms.Metrics import perimeter_metric
from src.Backend.Image_processing_algorithms.Metrics import area_metric
from src.Backend.Image_processing_algorithms.Metrics import axis_metric
from src.Backend.Video_processing_algorithms.movement_from_frames import get_avg_motion_in_region
from src.Classes.Project_mastermind import Project_mastermind
from src.Classes.Region import Region
from src.Constants import algorithm_constants
from src.Constants import string_constants
from src.Frontend.Utils import progress_bar
from src.Frontend.Utils import metrics_plot


def configure_metrics_menu_connections(main_window):
    main_window.generate_metrics_menu_option.triggered.connect(lambda: load_generate_metrics_options(main_window))
    main_window.generate_fractal_dimention_metrics_menu_option.triggered.connect \
        (lambda: load_generate_fractal_dimension_metrics_options(main_window))
    main_window.generate_movement_metrics_menu_option.triggered.connect \
        (lambda: load_generate_movement_metrics_options(main_window))
    main_window.plot_metrics_menu_option.triggered.connect \
        (lambda: load_plot_metrics_options(main_window))
    main_window.plot_distribution_metric_menu_option.triggered.connect \
        (lambda: load_plot_distribution_metrics_option(main_window))

    main_window.generate_metrics_load_mask_video_button.clicked.connect(lambda: load_mask_video_path(main_window))
    main_window.plot_metrics_load_dataframe_button.clicked.connect(lambda: load_metrics_data_path(main_window))

    main_window.generate_metrics_generate_button.clicked.connect(lambda: generate_metrics(main_window))
    main_window.generate_fractal_dimension_metrics_apply_button.clicked.connect \
        (lambda: generate_fractal_dimension_metrics(main_window))
    main_window.generate_movement_metrics_apply_button.clicked.connect(lambda: generate_movement_metrics(main_window))
    main_window.plot_metrics_generate_button.clicked.connect(lambda: plot_metrics(main_window))
    main_window.plot_metrics_distribution_button.clicked.connect(lambda: plot_distribution_metrics(main_window))


def load_generate_metrics_options(main_window):
    page = main_window.generate_metrics_options
    stacked_feature_windows = main_window.stacked_feature_windows
    stacked_feature_windows.setCurrentWidget(page)
    return


def load_generate_fractal_dimension_metrics_options(main_window):
    page = main_window.generate_fractal_dimension_metrics_options
    stacked_feature_windows = main_window.stacked_feature_windows
    stacked_feature_windows.setCurrentWidget(page)
    return


def load_plot_metrics_options(main_window):
    page = main_window.plot_metrics_options
    stacked_feature_windows = main_window.stacked_feature_windows
    stacked_feature_windows.setCurrentWidget(page)
    return


def load_generate_movement_metrics_options(main_window):
    page = main_window.generate_movement_metrics_options
    stacked_feature_windows = main_window.stacked_feature_windows
    stacked_feature_windows.setCurrentWidget(page)
    return


def load_plot_distribution_metrics_option(main_window):
    page = main_window.plot_distribution_metrics_option
    stacked_feature_windows = main_window.stacked_feature_windows
    stacked_feature_windows.setCurrentWidget(page)
    return


def load_mask_video_path(main_window):
    mask_video_path = video_file_manipulation.get_video_path()
    main_window.generate_metrics_mask_video_input.setText(mask_video_path)


def generate_metrics(main_window):
    mask_video_path = main_window.generate_metrics_mask_video_input.text()
    array_images_list = video_file_manipulation.get_video_as_array(mask_video_path)
    metrics_dictionary = get_generation_metrics_dictionary(main_window)
    checked_metrics_count = get_checked_metrics_count(metrics_dictionary)

    progress_bar.start_progress_bar(string_constants.CALCULATE_METRICS_TITLE,
                                    string_constants.CALCULATE_METRICS_DESCRIPTION,
                                    len(array_images_list) * checked_metrics_count)

    for metric_key in metrics_dictionary.keys():
        if metrics_dictionary[metric_key]:
            metric_values_list = generate_metric(metric_key, array_images_list)
            metrics_file.save_mask_metric(mask_video_path, metric_values_list, metric_key)


def generate_metric(metric_type, array_images_list):
    metric_values_list = []

    if metric_type == algorithm_constants.PERIMETER_METRIC:
        metric_values_list = perimeter_metric.get_perimeter_over_time(array_images_list)
    elif metric_type == algorithm_constants.AREA_METRIC:
        metric_values_list = area_metric.get_area_over_time(array_images_list)
    elif metric_type == algorithm_constants.AXIS_RATE_METRIC:
        metric_values_list = axis_metric.get_axis_ratio_over_time(array_images_list)

    return metric_values_list


def get_generation_metrics_dictionary(main_window):
    metrics_dictionary = {}

    is_perimeter_checked = main_window.generate_metrics_perimeter_checkbox.isChecked()
    metrics_dictionary[algorithm_constants.PERIMETER_METRIC] = is_perimeter_checked

    is_area_checked = main_window.generate_metrics_area_checkbox.isChecked()
    metrics_dictionary[algorithm_constants.AREA_METRIC] = is_area_checked

    is_axis_rate_checked = main_window.generate_metrics_axis_rate_checkbox.isChecked()
    metrics_dictionary[algorithm_constants.AXIS_RATE_METRIC] = is_axis_rate_checked

    return metrics_dictionary


def get_checked_metrics_count(metrics_dictionary):
    checked_values = 0

    for check_state_value in metrics_dictionary.values():
        if check_state_value:
            checked_values = checked_values + 1

    return checked_values


def generate_fractal_dimension_metrics(main_window):
    project_mastermind = Project_mastermind.get_instance()
    image_path = project_mastermind.get_original_image_path()
    current_image_array = project_mastermind.get_last_image()
    region_type = main_window.generate_fractal_dimension_metrics_region_combobox.currentText()
    region_points = Region().get_region()
    fractal_value = fractal_dimention.get_fractal_dimension_texture(current_image_array, region_points)
    metrics_file.save_fractal_dimension_metric(image_path, fractal_value, region_type)


def generate_movement_metrics(main_window):
    project_mastermind = Project_mastermind.get_instance()
    image_path = project_mastermind.get_original_image_path()
    heat_map_array = project_mastermind.get_heat_map_image_array()
    region_type = main_window.generate_movement_metrics_region_combobox.currentText()
    region_points = Region().get_region()
    avg_motion_value = get_avg_motion_in_region(region_points, heat_map_array)
    metrics_file.save_motion_metric(image_path, avg_motion_value, region_type)


def load_metrics_data_path(main_window):
    dataframe_path = dataframe_file_manipulation.get_dataframe_path()
    main_window.plot_metrics_dataframe_input.setText(dataframe_path)


def plot_metrics(main_window):
    metrics_data_path = main_window.plot_metrics_dataframe_input.text()
    metrics_data = metrics_file.read_metrics_data(metrics_data_path)
    metrics_dictionary = get_plotting_metrics_dictionary(main_window)

    metric_keys_list = list(metrics_dictionary.keys())

    for i in range(0, len(metric_keys_list)):
        metric_key = metric_keys_list[i]
        if metrics_dictionary[metric_key]:
            frames_values_list = metrics_file.get_frames(metrics_data)
            metric_values_list = metrics_file.get_metric(metrics_data, metric_key)
            if i == len(metric_keys_list) - 1:
                show_metric(metric_key, metric_values_list, frames_values_list, show_flag=True)
            else:
                show_metric(metric_key, metric_values_list, frames_values_list, show_flag=False)


def get_plotting_metrics_dictionary(main_window):
    metrics_dictionary = {}

    is_perimeter_checked = main_window.plot_metrics_perimeter_checkbox.isChecked()
    metrics_dictionary[algorithm_constants.PERIMETER_METRIC] = is_perimeter_checked

    is_area_checked = main_window.plot_metrics_area_checkbox.isChecked()
    metrics_dictionary[algorithm_constants.AREA_METRIC] = is_area_checked

    is_axis_rate_checked = main_window.plot_metrics_axis_rate_checkbox.isChecked()
    metrics_dictionary[algorithm_constants.AXIS_RATE_METRIC] = is_axis_rate_checked

    return metrics_dictionary


def show_metric(metric_type, metric_values_list, frames_values_list, show_flag):
    if metric_type == algorithm_constants.PERIMETER_METRIC:
        metrics_plot.plot_metric_over_time(metric_values_list, frames_values_list,
                                           string_constants.PERIMETER_PLOT_TITLE,
                                           string_constants.PERIMETER_X_LABEL,
                                           string_constants.PERIMETER_Y_LABEL,
                                           show_flag=show_flag)
    elif metric_type == algorithm_constants.AREA_METRIC:
        metrics_plot.plot_metric_over_time(metric_values_list, frames_values_list,
                                           string_constants.AREA_PLOT_TITLE,
                                           string_constants.AREA_X_LABEL,
                                           string_constants.AREA_Y_LABEL,
                                           show_flag=show_flag)
    elif metric_type == algorithm_constants.AXIS_RATE_METRIC:
        metrics_plot.plot_metric_over_time(metric_values_list, frames_values_list,
                                           string_constants.AXIS_RATIO_PLOT_TITLE,
                                           string_constants.AXIS_RATIO_X_LABEL,
                                           string_constants.AXIS_RATIO_Y_LABEL,
                                           show_flag=show_flag)


def plot_distribution_metrics(main_window):
    metrics_data_paths = dataframe_file_manipulation.get_multiple_dataframes_path()
    metrics_data_list = metrics_file.read_multiple_metrics_data(metrics_data_paths)
    distribution_metrics_dictionary = get_plotting_distribution_metrics_dictionary(main_window)

    metric_keys_list = list(distribution_metrics_dictionary.keys())

    for i in range(0, len(metric_keys_list)):
        metric_key = metric_keys_list[i]
        metrics_avg_list = []
        for metrics_data in metrics_data_list:
            metric_avg = metrics_file.get_metric_avg(metrics_data, metric_key)
            metrics_avg_list.append(metric_avg)
        plot_title = get_distribution_title(metric_key)
        plot_x_label = get_distribution_x_label(metric_key)
        plot_y_label = get_distribution_y_label(metric_key)
        if i == len(metric_keys_list) - 1:
            metrics_plot.plot_metric_histogram(metrics_avg_list,
                                               plot_title=plot_title,
                                               x_label=plot_x_label,
                                               y_label=plot_y_label,
                                               show_flag=True)
        else:
            metrics_plot.plot_metric_histogram(metrics_avg_list,
                                               plot_title=plot_title,
                                               x_label=plot_x_label,
                                               y_label=plot_y_label,
                                               show_flag=True)


def get_plotting_distribution_metrics_dictionary(main_window):
    metrics_dictionary = {}

    is_perimeter_checked = main_window.plot_metrics_distribution_perimeter_checkbox.isChecked()
    metrics_dictionary[algorithm_constants.PERIMETER_METRIC] = is_perimeter_checked

    is_area_checked = main_window.plot_metrics_distribution_area_checkbox.isChecked()
    metrics_dictionary[algorithm_constants.AREA_METRIC] = is_area_checked

    is_axis_rate_checked = main_window.plot_metrics_distribution_axis_rate_checkbox.isChecked()
    metrics_dictionary[algorithm_constants.AXIS_RATE_METRIC] = is_axis_rate_checked

    is_border_fractal_checked = main_window.plot_metrics_distribution_fractal_border_checkbox.isChecked()
    metrics_dictionary[algorithm_constants.BORDER_FRACTAL_DIMENSION_METRIC] = is_border_fractal_checked

    is_perinuclear_fractal_checked = main_window.plot_metrics_distribution_fractal_perinuclear_checkbox.isChecked()
    metrics_dictionary[algorithm_constants.PERINUCLEAR_FRACTAL_DIMENSION_METRIC] = is_perinuclear_fractal_checked

    is_nuclear_fractal_checked = main_window.plot_metrics_distribution_fractal_nuclear_checkbox.isChecked()
    metrics_dictionary[algorithm_constants.NUCLEAR_FRACTAL_DIMENSION_METRIC] = is_nuclear_fractal_checked

    is_border_movement_checked = main_window.plot_metrics_distribution_movement_border_checkbox.isChecked()
    metrics_dictionary[algorithm_constants.BORDER_MOVEMENT_METRIC] = is_border_movement_checked

    is_perinuclear_movement_checked = main_window.plot_metrics_distribution_movement_perinuclear_checkbox.isChecked()
    metrics_dictionary[algorithm_constants.PERINUCLEAR_MOVEMENT_METRIC] = is_perinuclear_movement_checked

    is_nuclear_movement_checked = main_window.plot_metrics_distribution_movement_nuclear_checkbox.isChecked()
    metrics_dictionary[algorithm_constants.NUCLEAR_MOVEMENT_METRIC] = is_nuclear_movement_checked

    return metrics_dictionary


def get_distribution_title(metric_type):
    return {
        algorithm_constants.PERIMETER_METRIC: "Distribucion de perimetros",
        algorithm_constants.AREA_METRIC: "Distribucion de areas",
        algorithm_constants.AXIS_RATE_METRIC: "Distribucion de razon de ejes",
        algorithm_constants.BORDER_FRACTAL_DIMENSION_METRIC: "Fractal dimension - borde distribucion",
        algorithm_constants.PERINUCLEAR_FRACTAL_DIMENSION_METRIC: "Fractal dimension - perinucleo distribucion",
        algorithm_constants.NUCLEAR_FRACTAL_DIMENSION_METRIC: "Fractal dimension - nucleo distribution",
        algorithm_constants.BORDER_MOVEMENT_METRIC: "Movimiento - borde distribucion",
        algorithm_constants.PERINUCLEAR_MOVEMENT_METRIC: "Movimiento - perinucleo distribucion",
        algorithm_constants.NUCLEAR_MOVEMENT_METRIC: "Movimiento - nucleo distribution",
    }.get(metric_type, "Titulo no encontrado!")


def get_distribution_x_label(metric_type):
    return {
        algorithm_constants.PERIMETER_METRIC: "Valores de perimetro en pixeles",
        algorithm_constants.AREA_METRIC: "Valores de area en pixeles",
        algorithm_constants.AXIS_RATE_METRIC: "Valores de razones de ejes",
        algorithm_constants.BORDER_FRACTAL_DIMENSION_METRIC: "Valores de dimension fractal en borde",
        algorithm_constants.PERINUCLEAR_FRACTAL_DIMENSION_METRIC: "Valores de dimension fractal en perinucleo",
        algorithm_constants.NUCLEAR_FRACTAL_DIMENSION_METRIC: "Valores de dimension fractal en nucleo",
        algorithm_constants.BORDER_MOVEMENT_METRIC: "Valores de moveimiento en borde",
        algorithm_constants.PERINUCLEAR_MOVEMENT_METRIC: "Valores de moveimiento en perinucleo",
        algorithm_constants.NUCLEAR_MOVEMENT_METRIC: "Valores de moveimiento en nucleo",
    }.get(metric_type, "Label no encontrado!")


def get_distribution_y_label(metric_type):
    return {
        algorithm_constants.PERIMETER_METRIC: "Valores de perimetro en pixeles",
        algorithm_constants.AREA_METRIC: "Valores de area en pixeles",
        algorithm_constants.AXIS_RATE_METRIC: "Valores de razones de ejes",
        algorithm_constants.BORDER_FRACTAL_DIMENSION_METRIC: "Valores de dimension fractal en borde",
        algorithm_constants.PERINUCLEAR_FRACTAL_DIMENSION_METRIC: "Valores de dimension fractal en perinucleo",
        algorithm_constants.NUCLEAR_FRACTAL_DIMENSION_METRIC: "Valores de dimension fractal en nucleo",
        algorithm_constants.BORDER_MOVEMENT_METRIC: "Valores de moveimiento en borde",
        algorithm_constants.PERINUCLEAR_MOVEMENT_METRIC: "Valores de moveimiento en perinucleo",
        algorithm_constants.NUCLEAR_MOVEMENT_METRIC: "Valores de moveimiento en nucleo",
    }.get(metric_type, "Label no encontrado!")