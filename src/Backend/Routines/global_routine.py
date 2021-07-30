import os
import random
import string

from src.Backend.Image_processing_algorithms.Metrics import metrics_generator, metrics_plotter
from src.Backend.Video_processing_algorithms.multiple_cells_video_generator import generate_mask_video_of_all_cells
from src.Constants import algorithm_constants, configuration_constants


def routine():
    # Setup
    routine_setup()

    # Mask stage
    masked_videos_paths_list = generate_mask_video_of_all_cells()
    videos_filename_list = get_videos_files_names(masked_videos_paths_list)

    # Generate metrics stage
    metrics_excel_paths_list = []
    metrics_dictionary = {algorithm_constants.AXIS_RATE_METRIC: True, algorithm_constants.PERIMETER_METRIC: True,
                          algorithm_constants.AREA_METRIC: True}
    distribution_metrics_dictionary = metrics_dictionary
    for masked_video_path in masked_videos_paths_list:
        metrics_excel_path = metrics_generator.generate_metrics(masked_video_path, metrics_dictionary)
        metrics_excel_paths_list.append(metrics_excel_path)

    # Save simple metrics stage
    for i in range(0, len(metrics_excel_paths_list)):
        metrics_excel_path = metrics_excel_paths_list[i]
        graph_filename = videos_filename_list[i]
        graph_save_path = generate_metric_path(graph_filename)
        metrics_values_lists, frames_values_lists, titles_list, x_label_list, y_label_list = metrics_plotter.load_metrics(metrics_excel_path, metrics_dictionary)
        metrics_plotter.save_metrics(metrics_values_lists, frames_values_lists, titles_list,
                                     x_label_list, y_label_list, graph_save_path)

    # Save distribution metrics stage
    metrics_avg_lists, titles_list, x_label_list, y_label_list = metrics_plotter.load_distribution_metrics(
            metrics_excel_paths_list, distribution_metrics_dictionary)
    distribution_save_path = generate_distribution_path(len(metrics_excel_paths_list))
    metrics_plotter.save_distribution_metrics(metrics_avg_lists, titles_list, x_label_list,
                                              y_label_list, distribution_save_path)


def routine_setup():
    create_directory_if_not_exists(configuration_constants.GRAPHS_FOLDER)
    create_directory_if_not_exists(configuration_constants.METRICS_GRAPH_FOLDER)
    create_directory_if_not_exists(configuration_constants.DISTRIBUTION_METRICS_GRAPH_FOLDER)


def create_directory_if_not_exists(directory_path):
    if not os.path.isdir(directory_path):
        os.mkdir(directory_path)


def generate_metric_path(filename):
    initial_path = configuration_constants.METRICS_GRAPH_FOLDER
    middle_name = filename
    extension = ".png"
    full_path = initial_path + middle_name + extension
    return full_path


def generate_distribution_path(cells_number):
    initial_path = configuration_constants.DISTRIBUTION_METRICS_GRAPH_FOLDER
    middle_name = "Celulas en distribucion - " + str(cells_number) + " hash - "
    hash_name = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
    extension = ".png"
    full_path = initial_path + middle_name + hash_name + extension
    return full_path


def get_videos_files_names(masked_videos_paths_list):
    videos_filename_list = []
    for video_path in masked_videos_paths_list:
        image_path_sample = video_path.replace("\\", "/")
        file_name_with_extension = image_path_sample.split('/')[-1]
        file_name_without_extension = os.path.splitext(file_name_with_extension)[0]
        videos_filename_list.append(file_name_without_extension)

    return videos_filename_list
