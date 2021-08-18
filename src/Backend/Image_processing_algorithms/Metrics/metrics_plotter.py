from src.Backend.Image_processing_algorithms.Metrics import metrics_file
from src.Constants import algorithm_constants, string_constants
from src.Frontend.Utils import metrics_plot


def load_metrics(metrics_data_path, metrics_dictionary):
    metrics_data = metrics_file.read_metrics_data(metrics_data_path)
    metric_keys_list = filter_keys(metrics_dictionary)
    metrics_values_lists = []
    frames_values_lists = []
    titles_list = []
    x_label_list = []
    y_label_list = []

    for i in range(0, len(metric_keys_list)):
        metric_key = metric_keys_list[i]
        labels_dictionary = get_metric_plot_labels(metric_key)
        frames_values_list = metrics_file.get_frames(metrics_data)
        metric_values_list = metrics_file.get_metric(metrics_data, metric_key)
        frames_values_lists.append(frames_values_list)
        metrics_values_lists.append(metric_values_list)
        titles_list.append(labels_dictionary["title"])
        x_label_list.append(labels_dictionary["x_label"])
        y_label_list.append(labels_dictionary["y_label"])

    return metrics_values_lists, frames_values_lists, titles_list, x_label_list, y_label_list


def load_distribution_metrics(metrics_data_paths, distribution_metrics_dictionary):
    metrics_data_list = metrics_file.read_multiple_metrics_data(metrics_data_paths)
    metric_keys_list = filter_keys(distribution_metrics_dictionary)
    metrics_avg_lists = []
    titles_list = []
    x_label_list = []
    y_label_list = []

    for i in range(0, len(metric_keys_list)):
        metric_key = metric_keys_list[i]
        labels_dictionary = get_distribution_plot_labels(metric_key)
        metrics_avg_list = []
        for metrics_data in metrics_data_list:
            metric_avg = metrics_file.get_metric_avg(metrics_data, metric_key)
            metrics_avg_list.append(metric_avg)
        metrics_avg_lists.append(metrics_avg_list)
        titles_list.append(labels_dictionary["title"])
        x_label_list.append(labels_dictionary["x_label"])
        y_label_list.append(labels_dictionary["y_label"])

    return metrics_avg_lists, titles_list, x_label_list, y_label_list


def plot_metrics(metrics_values_lists, frames_values_lists, titles_list, x_label_list, y_label_list):
    for i in range(0, len(metrics_values_lists)):
        show_flag = set_show_flag(metrics_values_lists, i)
        plot_metric(metrics_values_lists[i], frames_values_lists[i],
                    titles_list[i], x_label_list[i], y_label_list[i], show_flag=show_flag)


def plot_metric(metric_values_list, frames_values_list, title, x_label, y_label, show_flag):
    metrics_plot.plot_metric_over_time(metric_values_list, frames_values_list,
                                       title, x_label, y_label, show_flag=show_flag)


def save_metrics(metrics_values_lists, frames_values_lists, titles_list,
                 x_label_list, y_label_list, cell_image_array, save_path):
    metrics_plot.save_plot_metrics(metrics_values_lists, frames_values_lists, titles_list,
                                   x_label_list, y_label_list, cell_image_array, save_path)


def plot_distribution_metrics(metrics_avg_lists, titles_list, x_label_list, y_label_list):
    for i in range(0, len(metrics_avg_lists)):
        show_flag = set_show_flag(metrics_avg_lists, i)
        plot_distribution_metric(metrics_avg_lists[i], titles_list[i], x_label_list[i],
                                 y_label_list[i], show_flag=show_flag)


def plot_distribution_metric(metrics_avg_list, title, x_label, y_label, show_flag):
    metrics_plot.plot_metric_histogram(metrics_avg_list,
                                       plot_title=title,
                                       x_label=x_label,
                                       y_label=y_label,
                                       show_flag=show_flag)


def save_distribution_metrics(metrics_avg_lists, titles_list, x_label_list, y_label_list, save_path):
    metrics_plot.save_plot_distribution_metrics(metrics_avg_lists, titles_list, x_label_list, y_label_list, save_path)


def filter_keys(metrics_keys_dictionary):
    metric_keys_list = []

    for key in metrics_keys_dictionary.keys():
        if metrics_keys_dictionary[key]:
            metric_keys_list.append(key)

    return metric_keys_list


def set_show_flag(metrics_values_lists, metric_index):
    if metric_index == len(metrics_values_lists) - 1:
        return True
    return False


def get_metric_plot_labels(metric_type):
    labels_dictionary = {
        algorithm_constants.PERIMETER_METRIC: {"title": string_constants.PERIMETER_PLOT_TITLE,
                                               "x_label": string_constants.PERIMETER_X_LABEL},
        algorithm_constants.AREA_METRIC: {"title": string_constants.AREA_PLOT_TITLE,
                                          "x_label": string_constants.AREA_X_LABEL},
        algorithm_constants.AXIS_RATE_METRIC: {"title": string_constants.AXIS_RATIO_PLOT_TITLE,
                                               "x_label": string_constants.AXIS_RATIO_X_LABEL},
    }.get(metric_type, {"title": "None", "x_label": "None"})
    labels_dictionary["y_label"] = string_constants.SIMPLE_METRICS_Y_LABEL
    return labels_dictionary


def get_distribution_plot_labels(metric_type):
    labels_dictionary = {
        algorithm_constants.PERIMETER_METRIC: {"title": string_constants.PERIMETER_DISTRIBUTION_TITLE,
                                               "x_label": string_constants.PERIMETER_DISTRIBUTION_X_LABEL},
        algorithm_constants.AREA_METRIC: {"title": string_constants.AREA_DISTRIBUTION_TITLE,
                                          "x_label": string_constants.AREA_DISTRIBUTION_X_LABEL},
        algorithm_constants.AXIS_RATE_METRIC: {"title": string_constants.AXIS_RATIO_DISTRIBUTION_TITLE,
                                               "x_label": string_constants.AXIS_RATIO_DISTRIBUTION_X_LABEL}
    }.get(metric_type, {"title": "None", "x_label": "None"})
    labels_dictionary["y_label"] = string_constants.DISTRIBUTION_METRICS_Y_LABEL
    return labels_dictionary
