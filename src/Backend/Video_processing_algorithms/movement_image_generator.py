import os
from PIL import Image

import numpy as np
import cv2

from src.Backend.Image_processing_algorithms.Operations.common_operations import bgr_to_rgb
from src.Backend.Video_processing_algorithms import video_generator
from src.Backend.Video_processing_algorithms.multiple_cells_video_generator import get_images_from_directories
from src.Constants import configuration_constants


def create_multiple_motion_images(threshold, source_directory):
    images_list_of_lists = get_images_from_directories(source_directory)
    coloured_motion_images_list = []
    coloured_motion_images_save_path_list = []
    for i in range(0, len(images_list_of_lists)):
        unc_motion_image, c_motion_image = create_motion_image(threshold, images_list_of_lists[i])
        coloured_motion_images_list.append(c_motion_image)
        save_directory = configuration_constants.MOVEMENT_HEATMAP_IMAGES_DIRECTORY
        save_motion_path = video_generator.set_save_name(images_list_of_lists[i][0], save_directory,
                                                         extension=".png")
        save_motion_image(c_motion_image, save_motion_path)
        coloured_motion_images_save_path_list.append(save_motion_path)
    return coloured_motion_images_list, coloured_motion_images_save_path_list


def create_motion_image(threshold, images_path_for_motion_list=None):
    setup_directories()
    images_path_for_motion_list = get_images(images_path_for_motion_list)
    frames_path_list = generate_frames(images_path_for_motion_list)
    uncolored_motion_image_array = get_motion(frames_path_list, threshold)
    coloured_motion_image_array = bgr_to_rgb(cv2.applyColorMap(uncolored_motion_image_array, cv2.COLORMAP_HOT))
    video_generator.delete_frames(frames_path_list)
    os.rmdir(configuration_constants.TEMPORARY_VIDEO_DIRECTORY_PATH)
    return uncolored_motion_image_array, coloured_motion_image_array


def get_images(images_path_for_motion_list):
    if images_path_for_motion_list is None:
        images_path_for_motion_list = video_generator.get_original_images()
    return images_path_for_motion_list


def generate_frames(images_path_for_motion_list):
    frames_paths_list = video_generator.generate_frames(images_path_for_motion_list, specified_methods_to_apply=None)
    return frames_paths_list


def setup_directories():
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
    rows, cols = previous_grayscale_frame.shape
    accumulated_motion = np.zeros((rows, cols), np.uint8)

    for i in range(0, len(frames_path_list) - 1):
        current_grayscale_frame = get_grayscale(frames_path_list[i])
        ret, current_grayscale_frame = cv2.threshold(current_grayscale_frame, threshold, 255, cv2.THRESH_BINARY)
        accumulated_motion = get_frame_motion(current_grayscale_frame, previous_grayscale_frame,
                                              accumulated_motion)
        previous_grayscale_frame = current_grayscale_frame
    accumulated_motion = normalize_values(accumulated_motion)
    return accumulated_motion


def get_frame_motion(current_frame, previous_frame, accumulated_motion):
    MIN_MOVEMENT_VALUE = 1
    rows, cols = current_frame.shape
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