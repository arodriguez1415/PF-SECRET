from src.Backend.Image_processing_algorithms.Archive_manipulation import video_file_manipulation
from src.Backend.Image_processing_algorithms.Metrics import metrics_file
from src.Backend.Image_processing_algorithms.Metrics import perimeter_metric
from src.Backend.Image_processing_algorithms.Metrics import area_metric
from src.Backend.Image_processing_algorithms.Metrics import axis_metric
from src.Constants import algorithm_constants
from src.Constants import string_constants
from src.Frontend.Utils import progress_bar


def generate_metrics(mask_video_path, metrics_dictionary):
    array_images_list = video_file_manipulation.get_video_as_array(mask_video_path)
    checked_metrics_count = get_checked_metrics_count(metrics_dictionary)
    metric_keys_list = filter_keys(metrics_dictionary)

    progress_bar.start_progress_bar(string_constants.CALCULATE_METRICS_TITLE,
                                    string_constants.CALCULATE_METRICS_DESCRIPTION,
                                    len(array_images_list) * checked_metrics_count)

    for i in range(0, len(metric_keys_list)):
        metric_key = metric_keys_list[i]
        metric_values_list = generate_metric(metric_key, array_images_list)
        metrics_excel_path = metrics_file.save_mask_metric(mask_video_path, metric_values_list, metric_key)

    return metrics_excel_path


def generate_metric(metric_type, array_images_list):
    metric_values_list = []

    if metric_type == algorithm_constants.PERIMETER_METRIC:
        metric_values_list = perimeter_metric.get_perimeter_over_time(array_images_list)
    elif metric_type == algorithm_constants.AREA_METRIC:
        metric_values_list = area_metric.get_area_over_time(array_images_list)
    elif metric_type == algorithm_constants.AXIS_RATE_METRIC:
        metric_values_list = axis_metric.get_axis_ratio_over_time(array_images_list)

    return metric_values_list


def get_checked_metrics_count(metrics_dictionary):
    checked_values = 0

    for check_state_value in metrics_dictionary.values():
        if check_state_value:
            checked_values = checked_values + 1

    return checked_values


def filter_keys(metrics_keys_dictionary):
    metric_keys_list = []

    for key in metrics_keys_dictionary.keys():
        if metrics_keys_dictionary[key]:
            metric_keys_list.append(key)

    return metric_keys_list
