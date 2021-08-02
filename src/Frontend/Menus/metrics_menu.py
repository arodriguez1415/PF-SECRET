from src.Backend.Image_processing_algorithms.Archive_manipulation import dataframe_file_manipulation
from src.Backend.Image_processing_algorithms.Archive_manipulation import video_file_manipulation
from src.Backend.Image_processing_algorithms.Metrics import metrics_generator, metrics_plotter
from src.Constants import algorithm_constants


def configure_metrics_menu_connections(main_window):
    main_window.generate_metrics_menu_option.triggered.connect(lambda: load_generate_metrics_options(main_window))
    main_window.plot_metrics_menu_option.triggered.connect(lambda: load_plot_metrics_options(main_window))
    main_window.plot_distribution_metric_menu_option.triggered.connect(lambda:
                                                                       load_plot_distribution_metrics_option
                                                                       (main_window))

    main_window.generate_metrics_load_mask_video_button.clicked.connect(lambda: load_mask_video_path(main_window))
    main_window.plot_metrics_load_dataframe_button.clicked.connect(lambda: load_metrics_data_path(main_window))

    main_window.generate_metrics_generate_button.clicked.connect(lambda: generate_metrics(main_window))
    main_window.plot_metrics_generate_button.clicked.connect(lambda: plot_metrics(main_window))
    main_window.plot_metrics_distribution_button.clicked.connect(lambda: plot_distribution_metrics(main_window))


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


def load_mask_video_path(main_window):
    mask_video_path = video_file_manipulation.get_video_path()
    main_window.generate_metrics_mask_video_input.setText(mask_video_path)


def load_metrics_data_path(main_window):
    dataframe_path = dataframe_file_manipulation.get_dataframe_path()
    main_window.plot_metrics_dataframe_input.setText(dataframe_path)


def generate_metrics(main_window):
    mask_video_path = main_window.generate_metrics_mask_video_input.text()
    metrics_dictionary = get_generation_metrics_dictionary(main_window)
    metrics_generator.generate_metrics(mask_video_path, metrics_dictionary)


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
    metrics_data_path = main_window.plot_metrics_dataframe_input.text()
    metrics_dictionary = get_plotting_metrics_dictionary(main_window)
    metrics_values_lists, frames_values_lists, titles_list, x_label_list, y_label_list = metrics_plotter.load_metrics(metrics_data_path, metrics_dictionary)
    metrics_plotter.plot_metrics(metrics_values_lists, frames_values_lists, titles_list, x_label_list, y_label_list)


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
    metrics_data_paths = dataframe_file_manipulation.get_multiple_dataframes_path()
    distribution_metrics_dictionary = get_plotting_distribution_metrics_dictionary(main_window)
    metrics_avg_lists, titles_list, x_label_list, y_label_list = metrics_plotter.load_distribution_metrics(metrics_data_paths, distribution_metrics_dictionary)
    metrics_plotter.plot_distribution_metrics(metrics_avg_lists, titles_list, x_label_list, y_label_list)


def get_plotting_distribution_metrics_dictionary(main_window):
    metrics_dictionary = {}

    is_perimeter_checked = main_window.plot_metrics_distribution_perimeter_checkbox.isChecked()
    metrics_dictionary[algorithm_constants.PERIMETER_METRIC] = is_perimeter_checked

    is_area_checked = main_window.plot_metrics_distribution_area_checkbox.isChecked()
    metrics_dictionary[algorithm_constants.AREA_METRIC] = is_area_checked

    is_axis_rate_checked = main_window.plot_metrics_distribution_axis_rate_checkbox.isChecked()
    metrics_dictionary[algorithm_constants.AXIS_RATE_METRIC] = is_axis_rate_checked

    return metrics_dictionary

