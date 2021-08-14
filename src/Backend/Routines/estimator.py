import os

from src.Backend.Routines import global_routine
from src.Backend.Video_processing_algorithms.multiple_cells_video_generator import get_images_from_directories
from src.Constants import algorithm_constants, configuration_constants, string_constants
import time


def estimate_steps(sub_routines, source_directory):
    images_amount, directories_of_images_amount = get_amount_of_images(source_directory)
    type_of_videos = 2
    type_of_metrics = 3
    texture_calculation_step = 1

    total_steps = 0

    # Masked videos and simple videos
    if algorithm_constants.CONTOUR_SUBROUTINE in sub_routines:
        total_steps += images_amount * type_of_videos

    # Comparison videos of simple cells, preprocessed cells and mask cells
    if algorithm_constants.COMPARISON_SUBROUTINE in sub_routines:
        total_steps += images_amount

    # Metrics: Area, Perimeter and Axis Rate
    if algorithm_constants.METRICS_SUBROUTINE in sub_routines:
        total_steps += images_amount * type_of_metrics

    # Generates movement heat map with all the images
    if algorithm_constants.MOVEMENT_SUBROUTINE in sub_routines:
        total_steps += images_amount * 2

    # Generates texture video heat map with all the images + calculation step
    if algorithm_constants.TEXTURE_SUBROUTINE in sub_routines:
        total_steps += (images_amount * 2) + (directories_of_images_amount * texture_calculation_step)

    return total_steps


def estimate_time_and_space(sub_routines, source_directory):
    images_amount, directories_of_images_amount = get_amount_of_images(source_directory)
    total_time_in_seconds = estimate_time(images_amount, directories_of_images_amount, sub_routines)
    total_memory_in_kb = estimate_memory(images_amount, directories_of_images_amount, sub_routines)
    return total_time_in_seconds, total_memory_in_kb


def estimate_time(images_amount, directories_of_images_amount, sub_routines):
    sample_directory = configuration_constants.SAMPLE_ESTIMATOR_DIRECTORY
    generated_files_path = []
    contour_comparison_and_metrics_files = []

    first_init_time = time.time()

    if algorithm_constants.CONTOUR_SUBROUTINE in sub_routines:
        contour_comparison_and_metrics_files = global_routine.contour_comparison_and_metrics_subroutine(sub_routines,
                                                                                                        sample_directory)

    generated_files_path.extend(contour_comparison_and_metrics_files)

    contours_and_metrics_time_for_one_image = time.time() - first_init_time
    second_init_time = time.time()

    movement_and_texture_files = global_routine.movement_and_texture_heat_map_sub_routine(sub_routines,
                                                                                          sample_directory)
    generated_files_path.extend(movement_and_texture_files)

    remove_generated_files_for_estimation(generated_files_path)

    texture_and_movement_time_for_one_directory = time.time() - second_init_time

    contours_and_metrics_time_for_all_images = contours_and_metrics_time_for_one_image * images_amount
    texture_and_movement_time_for_all_directories = texture_and_movement_time_for_one_directory * directories_of_images_amount

    total_time = contours_and_metrics_time_for_all_images + texture_and_movement_time_for_all_directories
    max_time_texture_error = (directories_of_images_amount * 15) * 2
    max_time_movement_error = (directories_of_images_amount * 15) * 2

    if algorithm_constants.MOVEMENT_SUBROUTINE in sub_routines:
        total_time += max_time_movement_error

    if algorithm_constants.TEXTURE_SUBROUTINE in sub_routines:
        total_time += max_time_texture_error

    return total_time


# Memory estimation in KB
def estimate_memory(images_amount, directories_of_images, sub_routines):
    total_memory_space = 0

    normal_image_memory_space = 500
    masked_image_memory_space = 50

    return masked_image_memory_space


def get_amount_of_images(source_directory):
    images_list_of_lists = get_images_from_directories(source_directory)

    if not is_list_of_lists(images_list_of_lists):
        return len(images_list_of_lists), 1

    images_amount = 0
    directories_of_images = 0
    for list_of_images_path in images_list_of_lists:
        images_amount += len(list_of_images_path)
        directories_of_images += 1

    return images_amount, directories_of_images


def is_list_of_lists(list_of_lists):
    for element in list_of_lists:
        if not isinstance(element, list):
            return False
    return True


def prepare_estimation_message_and_title(total_time_in_seconds, total_memory_in_kb):
    title_message = string_constants.GLOBAL_ROUTINE_ESTIMATION_TITLE
    time_string = get_time_message(total_time_in_seconds)
    memory_string = get_memory_message(total_memory_in_kb)
    time_description_message = string_constants.GLOBAL_ROUTINE_TIME_ESTIMATION + str(time_string) + "\n"
    memory_description_message = string_constants.GLOBAL_ROUTINE_MEMORY_ESTIMATION + str(memory_string)
    description_message = time_description_message + memory_description_message
    return title_message, description_message


def get_time_message(seconds):
    hours = str(seconds // 3600)
    minutes = str((seconds % 3600) // 60)
    rem_seconds = str((seconds % 3600) % 60)
    message = "{} horas {} minutos {} segundos".format(hours, minutes, rem_seconds)
    return message


def get_memory_message(kilobytes):
    kilobytes_in_gigabytes = 1024 * 1024
    kilobytes_in_megabytes = 1024
    if kilobytes >= kilobytes_in_gigabytes:
        return str(kilobytes / kilobytes_in_gigabytes) + " GB"
    if kilobytes >= kilobytes_in_megabytes:
        return str(kilobytes / kilobytes_in_megabytes) + " MB"
    return str(kilobytes) + " KB"


def remove_generated_files_for_estimation(files_path_list):
    for file_path in files_path_list:
        os.remove(file_path)
