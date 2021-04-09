from src.Backend.Image_processing_algorithms.Archive_manipulation import video_file_manipulation
from src.Backend.Image_processing_algorithms.Metrics import perimeter_metric
from src.Backend.Image_processing_algorithms.Metrics import area_metric
from src.Backend.Image_processing_algorithms.Metrics import axis_metric
from src.Constants import string_constants
from src.Frontend.Utils import plot_comparator
from src.Frontend.Utils import progress_bar


def configure_metrics_menu_connections(main_window):
    main_window.perimeter_over_time_metrics_menu_option.triggered.connect(lambda: show_perimeter_over_time())
    main_window.area_over_time_metrics_menu_option.triggered.connect(lambda: show_area_over_time())
    main_window.axis_ratio_over_time_metrics_menu_option.triggered.connect(lambda: show_axis_ratio_over_time())

    main_window.perimeter_and_area_over_time_metrics_menu_option.triggered.\
        connect(lambda: show_area_and_perimeter_over_time())
    main_window.all_metrics_over_time_metrics_menu_option.triggered.\
        connect(lambda: show_all_metrics_over_time())


def show_perimeter_over_time():
    array_images_list = video_file_manipulation.get_video_as_array()
    progress_bar.start_progress_bar(string_constants.CALCULATE_PERIMETERS_TITLE,
                                    string_constants.CALCULATE_PERIMETERS_DESCRIPTION, len(array_images_list))
    perimeter_values_list = perimeter_metric.get_perimeter_over_time(array_images_list)
    if perimeter_values_list is not None:
        plot_comparator.plot_metric_over_time(perimeter_values_list, string_constants.PERIMETER_PLOT_TITLE,
                                              string_constants.PERIMETER_X_LABEL, string_constants.PERIMETER_Y_LABEL)


def show_area_over_time():
    array_images_list = video_file_manipulation.get_video_as_array()
    progress_bar.start_progress_bar(string_constants.CALCULATE_AREA_TITLE,
                                    string_constants.CALCULATE_AREA_DESCRIPTION, len(array_images_list))
    area_values_list = area_metric.get_area_over_time(array_images_list)
    if area_values_list is not None:
        plot_comparator.plot_metric_over_time(area_values_list, string_constants.AREA_PLOT_TITLE,
                                              string_constants.AREA_X_LABEL, string_constants.AREA_Y_LABEL)


def show_axis_ratio_over_time():
    array_images_list = video_file_manipulation.get_video_as_array()
    progress_bar.start_progress_bar(string_constants.CALCULATE_AXIS_RATIO_TITLE,
                                    string_constants.CALCULATE_AXIS_RATIO_DESCRIPTION, len(array_images_list))
    axis_ratio_values_list = axis_metric.get_axis_ratio_over_time(array_images_list)
    if axis_ratio_values_list is not None:
        plot_comparator.plot_metric_over_time(axis_ratio_values_list, string_constants.AXIS_RATIO_PLOT_TITLE,
                                              string_constants.AXIS_RATIO_X_LABEL, string_constants.AXIS_RATIO_Y_LABEL)


def show_area_and_perimeter_over_time():
    array_images_list = video_file_manipulation.get_video_as_array()
    progress_bar.start_progress_bar(string_constants.CALCULATE_METRICS_TITLE,
                                    string_constants.CALCULATE_METRICS_DESCRIPTION, len(array_images_list) * 2)
    perimeter_values_list = perimeter_metric.get_perimeter_over_time(array_images_list)
    area_values_list = area_metric.get_area_over_time(array_images_list)

    metrics_values = []
    metrics_values.append(perimeter_values_list)
    metrics_values.append(area_values_list)
    plot_titles = [string_constants.PERIMETER_PLOT_TITLE, string_constants.AREA_PLOT_TITLE]
    x_labels = [string_constants.PERIMETER_X_LABEL, string_constants.AREA_X_LABEL]
    y_label = string_constants.AREA_Y_LABEL
    if area_values_list is not None and perimeter_values_list is not None:
        plot_comparator.plot_metrics_over_time(metrics_values, plot_titles, x_labels, y_label)


def show_all_metrics_over_time():
    array_images_list = video_file_manipulation.get_video_as_array()
    progress_bar.start_progress_bar(string_constants.CALCULATE_METRICS_TITLE,
                                    string_constants.CALCULATE_METRICS_DESCRIPTION, len(array_images_list) * 3)
    perimeter_values_list = perimeter_metric.get_perimeter_over_time(array_images_list)
    area_values_list = area_metric.get_area_over_time(array_images_list)
    axis_ratio_values_list = axis_metric.get_axis_ratio_over_time(array_images_list)

    metrics_values = []
    metrics_values.append(perimeter_values_list)
    metrics_values.append(area_values_list)
    metrics_values.append(axis_ratio_values_list)
    plot_titles = [string_constants.PERIMETER_PLOT_TITLE, string_constants.AREA_PLOT_TITLE,
                   string_constants.AXIS_RATIO_PLOT_TITLE]
    x_labels = [string_constants.PERIMETER_X_LABEL, string_constants.AREA_X_LABEL,
                string_constants.AXIS_RATIO_X_LABEL]
    y_label = string_constants.AREA_Y_LABEL
    if area_values_list is not None and perimeter_values_list is not None:
        plot_comparator.plot_metrics_over_time(metrics_values, plot_titles, x_labels, y_label)
