import os
import shutil

from PIL import Image

import numpy as np
import cv2

from src.Backend.Image_processing_algorithms.Operations.common_operations import bgr_to_rgb, resize_image
from src.Backend.Video_processing_algorithms import video_generator
from src.Backend.Video_processing_algorithms.multiple_cells_video_generator import get_images_from_directories
from src.Classes.Methods.Anisotropic_Filter import Anisotropic_Filter
from src.Classes.Project_mastermind import Project_mastermind
from src.Constants import configuration_constants, string_constants
from src.Constants import properties_constants as ps
from src.Frontend.Utils import progress_bar


def create_multiple_motion_images(threshold, source_directory):
    images_list_of_lists = get_images_from_directories(source_directory)
    coloured_motion_images_list = []
    coloured_motion_images_save_path_list = []
    for i in range(0, len(images_list_of_lists)):
        unc_motion_image, unc_motion_image_normalized, c_motion_image = create_motion_image(threshold,
                                                                                            images_list_of_lists[i])
        coloured_motion_images_list.append(c_motion_image)
        save_directory = configuration_constants.MOVEMENT_HEATMAP_IMAGES_DIRECTORY
        save_motion_path = video_generator.set_save_name(images_list_of_lists[i][0], save_directory,
                                                         extension=".png")
        save_motion_image(c_motion_image, save_motion_path)
        coloured_motion_images_save_path_list.append(save_motion_path)
    return coloured_motion_images_list, coloured_motion_images_save_path_list


def create_motion_image(threshold, images_path_for_motion_list=None):
    images_path_for_motion_list = get_images(images_path_for_motion_list)
    setup(images_path_for_motion_list)
    frames_path_list = generate_frames(images_path_for_motion_list)
    uncolored_motion_image_array, uncolored_motion_image_array_normalized = get_motion(frames_path_list, threshold)
    coloured_motion_image_array = bgr_to_rgb(cv2.applyColorMap(uncolored_motion_image_array_normalized,
                                                               cv2.COLORMAP_HOT))
    video_generator.delete_frames(frames_path_list)
    shutil.rmtree(configuration_constants.TEMPORARY_VIDEO_DIRECTORY_PATH, ignore_errors=True)
    return uncolored_motion_image_array, uncolored_motion_image_array, coloured_motion_image_array


def get_images(images_path_for_motion_list):
    if images_path_for_motion_list is None:
        images_path_for_motion_list = video_generator.get_original_images()
    return images_path_for_motion_list


def generate_frames(images_path_for_motion_list):
    specified_methods_to_apply = set_methods_to_apply()
    frames_paths_list = video_generator.generate_frames(images_path_for_motion_list,
                                                        specified_methods_to_apply=specified_methods_to_apply)
    return frames_paths_list


def set_methods_to_apply():
    methods_to_apply = []
    min_iterations = 3
    iterations_to_apply = get_anisotropic_iterations()

    if iterations_to_apply < min_iterations:
        iterations_to_apply = min_iterations

    anisotropic_method = Anisotropic_Filter(iterations_to_apply)
    methods_to_apply.append(anisotropic_method)
    return methods_to_apply


def get_anisotropic_iterations():
    project_mastermind = Project_mastermind.get_instance()
    process_list = project_mastermind.get_image_processing_list()
    props_dict = project_mastermind.get_properties_dictionary()
    iterations = 0

    if project_mastermind.is_global_progress_bar_active():
        return props_dict[ps.GLOBAL_ROUTINE_ANISOTROPIC_FILTER_TIMES]

    for i in range(0, len(process_list)):
        process = process_list[i].get_method()
        if isinstance(process, Anisotropic_Filter):
            iterations += process.iterations

    return iterations


def setup(images_path_for_motion_list):
    progress_bar.start_progress_bar(string_constants.GENERATE_MOTION_HEAT_MAP_TITLE,
                                    string_constants.GENERATE_MOTION_HEAT_MAP_DESCRIPTION,
                                    len(images_path_for_motion_list) * 2 + 1)
    create_directory_if_not_exists(configuration_constants.TEMPORARY_VIDEO_DIRECTORY_PATH)
    create_directory_if_not_exists(configuration_constants.MOVEMENT_HEATMAP_IMAGES_DIRECTORY)


def create_directory_if_not_exists(directory_path):
    if not os.path.isdir(directory_path):
        os.mkdir(directory_path)


def save_motion_image(coloured_motion_image_array, save_motion_path):
    im = Image.fromarray(coloured_motion_image_array)
    im.save(save_motion_path)


def get_grayscale(frame_path):
    frame = cv2.imread(os.path.join(frame_path))
    rows, cols, dimensions = frame.shape
    grayscale_frame = np.zeros((rows, cols), np.uint8)
    for row in range(rows):
        for col in range(cols):
            grayscale_frame[row][col] = frame[row][col][0]
    return grayscale_frame


def get_motion(frames_path_list, threshold):
    previous_grayscale_frame = get_grayscale(frames_path_list[0])
    ret, previous_grayscale_frame = cv2.threshold(previous_grayscale_frame, threshold, 255, cv2.THRESH_BINARY)
    width, height = previous_grayscale_frame.shape
    accumulated_motion = np.zeros((width, height), np.uint8)
    accumulated_motion = resize_image(accumulated_motion, width, height)
    progress_bar.increment_value_progress_bar()
    for i in range(0, len(frames_path_list) - 1):
        current_grayscale_frame = get_grayscale(frames_path_list[i])
        current_grayscale_frame = resize_image(current_grayscale_frame, width, height)
        previous_grayscale_frame = resize_image(previous_grayscale_frame, width, height)
        ret, current_grayscale_frame = cv2.threshold(current_grayscale_frame, threshold, 255, cv2.THRESH_BINARY)
        accumulated_motion = get_frame_motion(current_grayscale_frame, previous_grayscale_frame,
                                              accumulated_motion)
        previous_grayscale_frame = current_grayscale_frame
        progress_bar.increment_value_progress_bar()
    accumulated_motion_normalized = normalize_values(accumulated_motion.copy())
    progress_bar.increment_value_progress_bar()
    return accumulated_motion, accumulated_motion_normalized


def get_frame_motion(current_frame, previous_frame, accumulated_motion):
    MIN_MOVEMENT_VALUE = 1
    rows, cols = accumulated_motion.shape
    for row in range(rows):
        for col in range(cols):
            difference = abs(int(current_frame[row][col]) - int(previous_frame[row][col]))
            if difference >= MIN_MOVEMENT_VALUE:
                accumulated_motion[row][col] = accumulated_motion[row][col] + 1
    return accumulated_motion


def normalize_values(accumulated_motion):
    max_value = np.max(accumulated_motion)
    rows, cols = accumulated_motion.shape
    for row in range(rows):
        for col in range(cols):
            accumulated_motion[row][col] = accumulated_motion[row][col] * 255 / max_value
    return accumulated_motion


def get_avg_motion_in_region(region, motion_array):
    accumulated_motion = 0
    values_quantity = 0

    left_top_point = region[0]
    right_bottom_point = region[-1]

    cols_init = left_top_point[0]
    cols_end = right_bottom_point[0]
    rows_init = left_top_point[1]
    rows_end = right_bottom_point[1]
    for i in range(rows_init, rows_end):
        for j in range(cols_init, cols_end):
            accumulated_motion += motion_array[i][j]
            values_quantity += 1

    return accumulated_motion / values_quantity
