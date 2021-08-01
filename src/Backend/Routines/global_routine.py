import os
import random
import string
import numpy as np

from PIL import Image

from src.Backend.Image_processing_algorithms.Metrics import metrics_generator, metrics_plotter
from src.Backend.Video_processing_algorithms import multiple_cells_video_generator
from src.Backend.Video_processing_algorithms.movement_image_generator import create_multiple_motion_images
from src.Backend.Video_processing_algorithms.texture_image_generator import create_multiple_texture_images
from src.Constants import algorithm_constants, configuration_constants


def routine(sub_routines):
    routine_setup()
    source_directory = multiple_cells_video_generator.get_source_directory()

    if algorithm_constants.CONTOUR_SUBROUTINE in sub_routines:
        contour_and_metrics_sub_routine(sub_routines, source_directory)

    if algorithm_constants.MOVEMENT_SUBROUTINE in sub_routines:
        movement_heat_map_sub_routine(source_directory)

    if algorithm_constants.TEXTURE_SUBROUTINE in sub_routines:
        texture_heat_map_sub_routine(source_directory)


def routine_setup():
    create_directory_if_not_exists(configuration_constants.CELLS_VIDEOS)
    create_directory_if_not_exists(configuration_constants.GRAPHS_FOLDER)
    create_directory_if_not_exists(configuration_constants.METRICS_GRAPH_FOLDER)
    create_directory_if_not_exists(configuration_constants.DISTRIBUTION_METRICS_GRAPH_FOLDER)


def create_directory_if_not_exists(directory_path):
    if not os.path.isdir(directory_path):
        os.mkdir(directory_path)


def contour_and_metrics_sub_routine(sub_routines, source_directory):
    masked_videos_paths_list, videos_filename_list = contour_sub_routine(source_directory)

    if algorithm_constants.METRICS_SUBROUTINE in sub_routines:
        metrics_sub_routine(source_directory, masked_videos_paths_list, videos_filename_list)


def contour_sub_routine(source_directory):
    # Cells videos stage
    cells_videos_paths_list = multiple_cells_video_generator.generate_video_of_all_cells(source_directory)

    # Mask videos stage
    masked_videos_paths_list = multiple_cells_video_generator.generate_mask_video_of_all_cells(source_directory)
    videos_filename_list = get_videos_files_names(masked_videos_paths_list)

    return masked_videos_paths_list, videos_filename_list


def metrics_sub_routine(source_directory, masked_videos_paths_list, videos_filename_list):
    metrics_dictionary = {algorithm_constants.AXIS_RATE_METRIC: True, algorithm_constants.PERIMETER_METRIC: True,
                          algorithm_constants.AREA_METRIC: True}
    distribution_metrics_dictionary = metrics_dictionary
    metrics_excel_paths_list = generate_metrics_sub_routine(masked_videos_paths_list, metrics_dictionary)
    plot_simple_metrics_sub_routine(source_directory, metrics_excel_paths_list, videos_filename_list,
                                    metrics_dictionary)
    plot_distribution_metrics_sub_routine(metrics_excel_paths_list, distribution_metrics_dictionary)


def generate_metrics_sub_routine(masked_videos_paths_list, metrics_dictionary):
    # Generate metrics stage
    metrics_excel_paths_list = []
    for masked_video_path in masked_videos_paths_list:
        metrics_excel_path = metrics_generator.generate_metrics(masked_video_path, metrics_dictionary)
        metrics_excel_paths_list.append(metrics_excel_path)

    return metrics_excel_paths_list


def plot_simple_metrics_sub_routine(source_directory, metrics_excel_paths_list, videos_filename_list,
                                    metrics_dictionary):
    # Save simple metrics stage
    first_cell_image_as_array_list = get_first_cell_image_list(source_directory)
    for i in range(0, len(metrics_excel_paths_list)):
        metrics_excel_path = metrics_excel_paths_list[i]
        cell_image_array = first_cell_image_as_array_list[i]
        graph_filename = videos_filename_list[i]
        graph_save_path = generate_metric_path(graph_filename)
        metrics_values_lists, frames_values_lists, titles_list, x_label_list, y_label_list = metrics_plotter.load_metrics(
            metrics_excel_path, metrics_dictionary)
        metrics_plotter.save_metrics(metrics_values_lists, frames_values_lists, titles_list,
                                     x_label_list, y_label_list, cell_image_array, graph_save_path)


def plot_distribution_metrics_sub_routine(metrics_excel_paths_list, distribution_metrics_dictionary):
    # Save distribution metrics stage
    metrics_avg_lists, titles_list, x_label_list, y_label_list = metrics_plotter.load_distribution_metrics(
        metrics_excel_paths_list, distribution_metrics_dictionary)
    distribution_save_path = generate_distribution_path(len(metrics_excel_paths_list))
    metrics_plotter.save_distribution_metrics(metrics_avg_lists, titles_list, x_label_list,
                                              y_label_list, distribution_save_path)


def movement_heat_map_sub_routine(source_directory):
    # Movement heat map stage
    threshold = 30
    create_multiple_motion_images(threshold, source_directory)


def texture_heat_map_sub_routine(source_directory):
    # Texture heat map stage
    threshold = 30
    clusters_quantity = 10
    create_multiple_texture_images(threshold, clusters_quantity, source_directory)


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


def get_first_cell_image_list(source_directory):
    images_list_of_lists_paths = multiple_cells_video_generator.get_images_from_directories(source_directory)
    first_cell_image_as_array_list = []
    for i in range(0, len(images_list_of_lists_paths)):
        image_path = images_list_of_lists_paths[i][0]
        image = Image.open(image_path).convert("L")
        image_array = np.asarray(image)
        first_cell_image_as_array_list.append(image_array)

    return first_cell_image_as_array_list
