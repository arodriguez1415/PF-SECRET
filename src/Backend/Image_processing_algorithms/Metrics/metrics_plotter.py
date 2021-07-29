from src.Backend.Image_processing_algorithms.Metrics import metrics_file
from src.Constants import algorithm_constants
from src.Constants import string_constants
from src.Frontend.Utils import metrics_plot


def plot_metrics(metrics_data_path, metrics_dictionary):
    metrics_data = metrics_file.read_metrics_data(metrics_data_path)
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


def plot_distribution_metrics(metrics_data_paths, distribution_metrics_dictionary):
    metrics_data_list = metrics_file.read_multiple_metrics_data(metrics_data_paths)
    metric_keys_list = filter_keys(distribution_metrics_dictionary)

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
                                               show_flag=False)


def filter_keys(metrics_keys_dictionary):
    metric_keys_list = []

    for key in metrics_keys_dictionary.keys():
        if metrics_keys_dictionary[key]:
            metric_keys_list.append(key)

    return metric_keys_list


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
    print(metric_type)
    return {
        algorithm_constants.PERIMETER_METRIC: "Valores de perimetro en pixeles",
        algorithm_constants.AREA_METRIC: "Valores de area en pixeles",
        algorithm_constants.AXIS_RATE_METRIC: "Valores de razones de ejes",
        algorithm_constants.BORDER_FRACTAL_DIMENSION_METRIC: "Valores de dimension fractal en borde",
        algorithm_constants.PERINUCLEAR_FRACTAL_DIMENSION_METRIC: "Valores de dimension fractal en perinucleo",
        algorithm_constants.NUCLEAR_FRACTAL_DIMENSION_METRIC: "Valores de dimension fractal en nucleo",
        algorithm_constants.BORDER_MOVEMENT_METRIC: "Valores de movimiento en borde",
        algorithm_constants.PERINUCLEAR_MOVEMENT_METRIC: "Valores de movimiento en perinucleo",
        algorithm_constants.NUCLEAR_MOVEMENT_METRIC: "Valores de movimiento en nucleo",
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
