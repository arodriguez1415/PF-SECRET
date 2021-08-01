import os
import pandas as pd

from src.Constants import configuration_constants
from src.Constants import algorithm_constants


def generate_metrics_dir():
    if not os.path.isdir(configuration_constants.METRICS_DIRECTORY_PATH):
        os.mkdir(configuration_constants.METRICS_DIRECTORY_PATH)


def set_metrics_save_name_from_video(video_path_sample):
    image_path_sample = video_path_sample.replace("\\", "/")
    file_name_with_extension = image_path_sample.split('/')[-1]
    file_name_with_xlsx_extension = os.path.splitext(file_name_with_extension)[0] + '.xlsx'
    dir_save_path = configuration_constants.METRICS_DIRECTORY_PATH
    save_path = dir_save_path + file_name_with_xlsx_extension
    return save_path


def set_metrics_save_name_from_image(image_path_sample):
    image_path_sample = image_path_sample.replace("\\", "/")
    file_name = image_path_sample.split('/')[-5] + " - " + image_path_sample.split('/')[-4] + " - " + \
                image_path_sample.split('/')[-3] + " - " + image_path_sample.split('/')[-2]
    file_name_with_xlsx_extension = file_name + '.xlsx'
    dir_save_path = configuration_constants.METRICS_DIRECTORY_PATH
    save_path = dir_save_path + file_name_with_xlsx_extension
    return save_path


def read_metrics_data(file_path):
    metrics_data = pd.read_excel(file_path)
    return metrics_data


def read_multiple_metrics_data(file_paths_list):
    metrics_data_list = []

    for file_path in file_paths_list:
        metrics_data = read_metrics_data(file_path)
        metrics_data_list.append(metrics_data)

    return metrics_data_list


def setup_metrics_data(file_path):
    if os.path.exists(file_path):
        metrics_data = pd.read_excel(file_path)
    else:
        metrics_data = pd.DataFrame()
    return metrics_data


def save_mask_metric(video_file_path, metric_values_list, metric_type):
    generate_metrics_dir()
    metrics_file_path = set_metrics_save_name_from_video(video_file_path)
    metrics_data = setup_metrics_data(metrics_file_path)

    if metric_type == algorithm_constants.PERIMETER_METRIC:
        metrics_data = save_perimeter(metrics_data, metric_values_list)
    elif metric_type == algorithm_constants.AREA_METRIC:
        metrics_data = save_area(metrics_data, metric_values_list)
    elif metric_type == algorithm_constants.AXIS_RATE_METRIC:
        metrics_data = save_axis_rate(metrics_data, metric_values_list)

    set_frames(metrics_data, metric_values_list)

    metrics_data = metrics_data[metrics_data.filter(regex='^(?!Unnamed)').columns]
    metrics_data.to_excel(metrics_file_path)
    return metrics_file_path


def save_fractal_dimension_metric(image_file_path, fractal_dimension_value, metric_type):
    generate_metrics_dir()
    metrics_file_path = set_metrics_save_name_from_image(image_file_path)
    metrics_data = setup_metrics_data(metrics_file_path)

    print(fractal_dimension_value)
    if metric_type == algorithm_constants.BORDER_FRACTAL_DIMENSION_METRIC:
        metrics_data[algorithm_constants.BORDER_FRACTAL_DIMENSION_HEADER] = fractal_dimension_value[0]
    elif metric_type == algorithm_constants.PERINUCLEAR_FRACTAL_DIMENSION_METRIC:
        metrics_data[algorithm_constants.PERINUCLEAR_FRACTAL_DIMENSION_HEADER] = fractal_dimension_value[0]
    elif metric_type == algorithm_constants.NUCLEAR_FRACTAL_DIMENSION_METRIC:
        metrics_data[algorithm_constants.NUCLEAR_FRACTAL_DIMENSION_HEADER] = fractal_dimension_value[0]

    metrics_data = metrics_data[metrics_data.filter(regex='^(?!Unnamed)').columns]
    metrics_data.to_excel(metrics_file_path)


def save_motion_metric(image_file_path, motion_value, metric_type):
    generate_metrics_dir()
    metrics_file_path = set_metrics_save_name_from_image(image_file_path)
    metrics_data = setup_metrics_data(metrics_file_path)

    print(metric_type)

    if metric_type == algorithm_constants.BORDER_MOVEMENT_METRIC:
        metrics_data[algorithm_constants.BORDER_MOVEMENT_HEADER] = motion_value
        print("Era borde")
    elif metric_type == algorithm_constants.PERINUCLEAR_MOVEMENT_METRIC:
        metrics_data[algorithm_constants.PERINUCLEAR_MOVEMENT_HEADER] = motion_value
        print("Era peri")
    elif metric_type == algorithm_constants.NUCLEAR_MOVEMENT_METRIC:
        metrics_data[algorithm_constants.NUCLEAR_MOVEMENT_HEADER] = motion_value
        print("Era nucleo")

    metrics_data = metrics_data[metrics_data.filter(regex='^(?!Unnamed)').columns]
    metrics_data.to_excel(metrics_file_path)


def save_perimeter(metrics_data, perimeter_values_list):
    metrics_data[algorithm_constants.PERIMETER_HEADER] = perimeter_values_list
    return metrics_data


def save_area(metrics_data, area_values_list):
    metrics_data[algorithm_constants.AREA_HEADER] = area_values_list
    return metrics_data


def save_axis_rate(metrics_data, axis_rate_values_list):
    metrics_data[algorithm_constants.AXIS_RATE_HEADER] = axis_rate_values_list
    return metrics_data


def get_frames(metrics_data):
    return metrics_data[algorithm_constants.FRAMES_HEADER].values.tolist()


def set_frames(metrics_data, metric_values_list):
    frames_values_list = []

    for i in range(0, len(metric_values_list)):
        frames_values_list.append(i)

    metrics_data[algorithm_constants.FRAMES_HEADER] = frames_values_list


def get_metric(metrics_data, metric_type):
    return metrics_data[metric_type].values.tolist()


def get_fractal_dimension(metrics_data, metric_type):
    return metrics_data[metric_type].values.tolist()[0]


def get_metric_avg(metrics_data, metric_type):
    if metric_type in metrics_data.columns:
        metric_values_list = metrics_data[metric_type].values.tolist()
        metric_values_list_length = len(metric_values_list)
        metric_values_sum = sum(metric_values_list)
        return metric_values_sum / metric_values_list_length
    return 0
