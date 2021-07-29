from src.Backend.Image_processing_algorithms.Metrics import metrics_file
from src.Constants import algorithm_constants
from src.Frontend.Utils import metrics_plot


def plot_metrics(metrics_data_path, metrics_dictionary):
    metrics_data = metrics_file.read_metrics_data(metrics_data_path)
    metric_keys_list = filter_keys(metrics_dictionary)

    for i in range(0, len(metric_keys_list)):
        metric_key = metric_keys_list[i]
        frames_values_list = metrics_file.get_frames(metrics_data)
        metric_values_list = metrics_file.get_metric(metrics_data, metric_key)
        if i == len(metric_keys_list) - 1:
            show_metric(metric_key, metric_values_list, frames_values_list, show_flag=True)
        else:
            show_metric(metric_key, metric_values_list, frames_values_list, show_flag=False)


def show_metric(metric_key, metric_values_list, frames_values_list, show_flag):
    labels_dictionary = get_metric_plot_labels(metric_key)
    metrics_plot.plot_metric_over_time(metric_values_list, frames_values_list,
                                       labels_dictionary["title"],
                                       labels_dictionary["x_label"],
                                       labels_dictionary["y_label"],
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
        labels_dictionary = get_distribution_plot_labels(metric_key)
        if i == len(metric_keys_list) - 1:
            metrics_plot.plot_metric_histogram(metrics_avg_list,
                                               plot_title=labels_dictionary["title"],
                                               x_label=labels_dictionary["x_label"],
                                               y_label=labels_dictionary["y_label"],
                                               show_flag=True)
        else:
            metrics_plot.plot_metric_histogram(metrics_avg_list,
                                               plot_title=labels_dictionary["title"],
                                               x_label=labels_dictionary["x_label"],
                                               y_label=labels_dictionary["y_label"],
                                               show_flag=False)


def filter_keys(metrics_keys_dictionary):
    metric_keys_list = []

    for key in metrics_keys_dictionary.keys():
        if metrics_keys_dictionary[key]:
            metric_keys_list.append(key)

    return metric_keys_list


def get_metric_plot_labels(metric_type):
    labels_dictionary = {
        algorithm_constants.PERIMETER_METRIC: {"title": "Perimetro en el tiempo",
                                               "x_label": "Perimetro en pixeles"},
        algorithm_constants.AREA_METRIC: {"title": "Area en el tiempo",
                                          "x_label": "Area en pixeles"},
        algorithm_constants.AXIS_RATE_METRIC: {"title": "Razon de ejes en el tiempo",
                                               "x_label": "Razón de ejes"},
    }.get(metric_type, {"title": "None", "x_label": "None"})
    labels_dictionary["y_label"] = "Tiempo en frames"
    return labels_dictionary


def get_distribution_plot_labels(metric_type):
    labels_dictionary = {
        algorithm_constants.PERIMETER_METRIC: {"title": "Distribucion de perimetros",
                                               "x_label": "Valores de perimetro en pixeles"},
        algorithm_constants.AREA_METRIC: {"title": "Distribucion de areas",
                                          "x_label": "Valores de areas en pixeles"},
        algorithm_constants.AXIS_RATE_METRIC: {"title": "Distribucion de razon de ejes",
                                               "x_label": "Valores de razon de ejes"},
        # algorithm_constants.BORDER_FRACTAL_DIMENSION_METRIC: "Fractal dimension - borde distribucion",
        # algorithm_constants.PERINUCLEAR_FRACTAL_DIMENSION_METRIC: "Fractal dimension - perinucleo distribucion",
        # algorithm_constants.NUCLEAR_FRACTAL_DIMENSION_METRIC: "Fractal dimension - nucleo distribution",
        # algorithm_constants.BORDER_MOVEMENT_METRIC: "Movimiento - borde distribucion",
        # algorithm_constants.PERINUCLEAR_MOVEMENT_METRIC: "Movimiento - perinucleo distribucion",
        # algorithm_constants.NUCLEAR_MOVEMENT_METRIC: "Movimiento - nucleo distribution",
    }.get(metric_type, {"title": "None", "x_label": "None"})
    labels_dictionary["y_label"] = "Cantidad de celulas"
    return labels_dictionary
