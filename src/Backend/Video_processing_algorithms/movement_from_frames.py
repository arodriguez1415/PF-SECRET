import os

import numpy as np
import cv2

from src.Backend.Video_processing_algorithms import video_generator
from src.Constants import configuration_constants


def create_motion_image(threshold):
    frames_path_list = generate_frames()
    uncolored_motion_image_array = get_motion(frames_path_list, threshold)
    coloured_motion_image_array = cv2.applyColorMap(uncolored_motion_image_array, cv2.COLORMAP_HOT)

    # save_path = partial_save_path + "motion-heatmap.jpg"
    # cv2.imwrite(save_path, color_image)

    video_generator.delete_frames(frames_path_list)
    os.rmdir(configuration_constants.TEMPORARY_VIDEO_DIRECTORY_PATH)
    return uncolored_motion_image_array, coloured_motion_image_array


def generate_frames():
    if not os.path.isdir(configuration_constants.TEMPORARY_VIDEO_DIRECTORY_PATH):
        os.mkdir(configuration_constants.TEMPORARY_VIDEO_DIRECTORY_PATH)

    images_paths_list = video_generator.get_original_images()
    frames_paths_list = video_generator.generate_frames(images_paths_list, specified_methods_to_apply=None)
    return frames_paths_list


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
    # cv2.imshow('frame', previous_grayscale_frame)
    # cv2.waitKey(0)
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
