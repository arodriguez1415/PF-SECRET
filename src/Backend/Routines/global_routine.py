import os
import random
import string
import time

import numpy as np

from PIL import Image

from src.Backend.Image_processing_algorithms.Metrics import metrics_generator, metrics_plotter
from src.Backend.Routines.estimator import estimate_time_and_space, prepare_estimation_message_and_title, \
    estimate_steps, get_time_message
from src.Backend.Video_processing_algorithms import multiple_cells_video_generator
from src.Backend.Video_processing_algorithms.movement_image_generator import create_multiple_motion_images
from src.Backend.Video_processing_algorithms.multiple_cells_video_generator import get_images_from_directories, \
    generate_video_comparator_of_all_cells
from src.Backend.Video_processing_algorithms.texture_image_generator import create_multiple_texture_images
from src.Backend.Video_processing_algorithms.video_generator import set_save_name
from src.Constants import algorithm_constants, configuration_constants, string_constants
from src.Frontend.Utils import plot_comparator, progress_bar
from src.Frontend.Utils.message import show_confirmation_message, show_wait_message


def routine(sub_routines):
    routine_setup()
    source_directory = multiple_cells_video_generator.get_source_directory()

    if source_directory is None or source_directory == "":
        return

    continue_flag = estimate_time_and_space_sub_routine(sub_routines, source_directory)
    if not continue_flag:
        return

    total_steps = estimate_steps(sub_routines, source_directory)
    progress_bar.start_progress_bar(string_constants.GLOBAL_ROUTINE_PROGRESS_BAR_TITLE,
                                    string_constants.GLOBAL_ROUTINE_PROGRESS_BAR_TITLE,
                                    total_steps, is_global=True)

    init_time = time.time()

    if algorithm_constants.CONTOUR_SUBROUTINE in sub_routines:
        contour_comparison_and_metrics_subroutine(sub_routines, source_directory)

    movement_and_texture_heat_map_sub_routine(sub_routines, source_directory)

    total_time = time.time() - init_time
    print(get_time_message(total_time))


def estimate_time_and_space_sub_routine(sub_routines, source_directory):
    progress_bar.set_global_progress_bar_active(True)
    message_box = show_wait_message(string_constants.WAIT_ESTIMATION_MESSAGE_TITLE,
                                    string_constants.WAIT_ESTIMATION_MESSAGE_DESC)
    total_time_in_seconds, total_memory_in_kb = estimate_time_and_space(sub_routines, source_directory)
    message_box.done(0)
    title_message, description_message = prepare_estimation_message_and_title(total_time_in_seconds, total_memory_in_kb)
    continue_flag = show_confirmation_message(title_message, description_message)
    progress_bar.set_global_progress_bar_active(False)
    return continue_flag


def routine_setup():
    create_directory_if_not_exists(configuration_constants.CELLS_VIDEOS)
    create_directory_if_not_exists(configuration_constants.COMPARISON_VIDEOS)
    create_directory_if_not_exists(configuration_constants.GRAPHS_FOLDER)
    create_directory_if_not_exists(configuration_constants.METRICS_GRAPH_FOLDER)
    create_directory_if_not_exists(configuration_constants.DISTRIBUTION_METRICS_GRAPH_FOLDER)
    create_directory_if_not_exists(configuration_constants.MOVEMENT_VS_TEXTURE_COMPARISON_DIRECTORY)


def create_directory_if_not_exists(directory_path):
    if not os.path.isdir(directory_path):
        os.mkdir(directory_path)


def contour_comparison_and_metrics_subroutine(sub_routines, source_directory):
    masked_videos_path_list, cells_videos_path_list, videos_filename_list, generated_files = contour_sub_routine(source_directory)
    metrics_generated_files = []
    comparison_generated_files = []

    if algorithm_constants.COMPARISON_SUBROUTINE in sub_routines:
        comparison_generated_files = comparison_sub_routine(cells_videos_path_list, masked_videos_path_list)

    if algorithm_constants.METRICS_SUBROUTINE in sub_routines:
        metrics_generated_files = metrics_sub_routine(source_directory, videos_filename_list, masked_videos_path_list)

    generated_files.extend(metrics_generated_files)
    generated_files.extend(comparison_generated_files)
    return generated_files


def contour_sub_routine(source_directory):
    # Cells videos stage
    cells_videos_paths_list = multiple_cells_video_generator.generate_video_of_all_cells(source_directory)

    # Mask videos stage
    masked_videos_paths_list = multiple_cells_video_generator.generate_mask_video_of_all_cells(source_directory)
    videos_filename_list = get_videos_files_names(masked_videos_paths_list)

    generated_files = []
    generated_files.extend(cells_videos_paths_list)
    generated_files.extend(masked_videos_paths_list)

    return masked_videos_paths_list, cells_videos_paths_list, videos_filename_list, generated_files


def comparison_sub_routine(cells_videos_path_list, masked_videos_path_list):
    return generate_video_comparator_of_all_cells(cells_videos_path_list, masked_videos_path_list)


def metrics_sub_routine(source_directory, videos_filename_list, masked_videos_paths_list):
    metrics_dictionary = {algorithm_constants.AXIS_RATE_METRIC: True, algorithm_constants.PERIMETER_METRIC: True,
                          algorithm_constants.AREA_METRIC: True}
    distribution_metrics_dictionary = metrics_dictionary
    metrics_excel_paths_list = generate_metrics_sub_routine(masked_videos_paths_list, metrics_dictionary)
    simple_metrics_path_list = plot_simple_metrics_sub_routine(source_directory, metrics_excel_paths_list,
                                                               videos_filename_list, metrics_dictionary)
    distribution_metrics_path_list = plot_distribution_metrics_sub_routine(metrics_excel_paths_list,
                                                                           distribution_metrics_dictionary)

    generated_files = []
    generated_files.extend(metrics_excel_paths_list)
    generated_files.extend(simple_metrics_path_list)
    generated_files.extend(distribution_metrics_path_list)
    return generated_files


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
    generated_plot_files_list = []
    for i in range(0, len(metrics_excel_paths_list)):
        metrics_excel_path = metrics_excel_paths_list[i]
        cell_image_array = first_cell_image_as_array_list[i]
        graph_filename = videos_filename_list[i]
        graph_save_path = generate_metric_path(graph_filename)
        metrics_values_lists, frames_values_lists, titles_list, x_label_list, y_label_list = metrics_plotter.load_metrics(
            metrics_excel_path, metrics_dictionary)
        metrics_plotter.save_metrics(metrics_values_lists, frames_values_lists, titles_list,
                                     x_label_list, y_label_list, cell_image_array, graph_save_path)
        generated_plot_files_list.append(graph_save_path)
    return generated_plot_files_list


def plot_distribution_metrics_sub_routine(metrics_excel_paths_list, distribution_metrics_dictionary):
    # Save distribution metrics stage
    metrics_avg_lists, titles_list, x_label_list, y_label_list = metrics_plotter.load_distribution_metrics(
        metrics_excel_paths_list, distribution_metrics_dictionary)
    generated_plot_files_list = []
    distribution_save_path = generate_distribution_path(len(metrics_excel_paths_list))
    metrics_plotter.save_distribution_metrics(metrics_avg_lists, titles_list, x_label_list,
                                              y_label_list, distribution_save_path)
    generated_plot_files_list.append(distribution_save_path)
    return generated_plot_files_list


def movement_and_texture_heat_map_sub_routine(sub_routines, source_directory):
    motion_images_array_list = []
    texture_images_array_list = []
    generated_files = []
    motion_images_path_list = []
    texture_images_path_list = []
    generated_plot_files_list = []

    if algorithm_constants.MOVEMENT_SUBROUTINE in sub_routines:
        motion_images_array_list, motion_images_path_list = movement_heat_map_sub_routine(source_directory)

    if algorithm_constants.TEXTURE_SUBROUTINE in sub_routines:
        texture_images_array_list, texture_images_path_list = texture_heat_map_sub_routine(source_directory)

    if algorithm_constants.MOVEMENT_SUBROUTINE and algorithm_constants.TEXTURE_SUBROUTINE in sub_routines:
        generated_plot_files_list = movement_and_texture_comparison_sub_routine(source_directory,
                                                                                motion_images_array_list,
                                                                                texture_images_array_list)

    generated_files.extend(motion_images_path_list)
    generated_files.extend(texture_images_path_list)
    generated_files.extend(generated_plot_files_list)
    return generated_files


def movement_heat_map_sub_routine(source_directory):
    # Movement heat map stage
    threshold = 20
    motion_images_array_list, motion_images_path_list = create_multiple_motion_images(threshold, source_directory)
    return motion_images_array_list, motion_images_path_list


def texture_heat_map_sub_routine(source_directory):
    # Texture heat map stage
    threshold = 20
    clusters_quantity = 10
    texture_images_array_list, texture_images_path_list = create_multiple_texture_images(threshold, clusters_quantity,
                                                                                         source_directory)
    return texture_images_array_list, texture_images_path_list


def movement_and_texture_comparison_sub_routine(source_directory, motion_images_array_list, texture_images_array_list):
    images_list_of_lists = get_images_from_directories(source_directory)
    save_directory = configuration_constants.MOVEMENT_VS_TEXTURE_COMPARISON_DIRECTORY
    generated_plot_files_list = []

    for i in range(0, len(motion_images_array_list)):
        movement_image_array = motion_images_array_list[i]
        texture_image_array = texture_images_array_list[i]
        save_comparison_path = set_save_name(images_list_of_lists[i][0], save_directory, extension=".png")
        images_array_list = [movement_image_array, texture_image_array]
        title = string_constants.MOVEMENT_VS_TEXTURE_VIDEO_TITLE
        sub_titles_list = [string_constants.MOVEMENT_TITLE, string_constants.TEXTURE_VIDEO_TITLE]
        plot_comparator.plot_comparison(images_array_list, title, sub_titles_list, save_path=save_comparison_path)
        generated_plot_files_list.append(save_comparison_path)
    return generated_plot_files_list


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
