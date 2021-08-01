from src.Backend.Image_processing_algorithms.Operations import common_operations
from src.Constants import configuration_constants as configuration_constants
from src.Classes.Project_mastermind import Project_mastermind
from PIL import Image
import cv2 as cv
import numpy as np
import os


def generate_video(images_list=None, specified_methods_to_apply=None,
                   save_directory=configuration_constants.MASK_VIDEOS):
    setup_directories()
    images_paths_list = images_list
    if images_list is None:
        images_paths_list = get_original_images()
    frames_paths_list = generate_frames(images_paths_list, specified_methods_to_apply)
    save_video_path = set_save_name(images_paths_list[0], save_directory)
    save_video(frames_paths_list, save_video_path)
    delete_frames(frames_paths_list)
    os.rmdir(configuration_constants.TEMPORARY_VIDEO_DIRECTORY_PATH)
    return save_video_path


def setup_directories():
    create_directory_if_not_exists(configuration_constants.TEMPORARY_VIDEO_DIRECTORY_PATH)
    create_directory_if_not_exists(configuration_constants.MASK_VIDEOS)


def create_directory_if_not_exists(directory_path):
    if not os.path.isdir(directory_path):
        os.mkdir(directory_path)


def get_original_images():
    project_mastermind = Project_mastermind.get_instance()
    original_directory = project_mastermind.get_original_image_dir()
    images_list_paths = get_files_from_directory(original_directory)
    return images_list_paths


def generate_frames(images_path, specified_methods_to_apply, apply_methods_flag=True):
    index = 0
    frames_paths_list = []
    for image_path in images_path:
        image = Image.open(image_path)
        image_array = common_operations.normalize_from_pil_image(image)
        frame_path = configuration_constants.TEMPORARY_VIDEO_DIRECTORY_PATH + "frame - " + str(index) + ".tif"
        if apply_methods_flag:
            if specified_methods_to_apply is None:
                image_array = apply_methods_from_process(image_array)
            else:
                image_array = apply_methods_specified(image_array, specified_methods_to_apply)
        cv.imwrite(frame_path, np.uint8(image_array))
        frames_paths_list.append(frame_path)
        index = index + 1
    return frames_paths_list


def apply_methods_from_process(image_array):
    project_mastermind = Project_mastermind.get_instance()
    image_processing_list = project_mastermind.get_image_processing_list()
    result_image_array = image_array
    for i in range(0, len(image_processing_list)):
        current_image_wrapper = image_processing_list[i]
        result_image_array = current_image_wrapper.method.apply_method(result_image_array)
    return result_image_array


def apply_methods_specified(image_array, specified_methods_to_apply):
    for i in range(0, len(specified_methods_to_apply)):
        image_array = specified_methods_to_apply[i].apply_method(image_array)
    return image_array


def save_video(frames_paths_list, video_path):
    height, width, layers = cv.imread(frames_paths_list[0]).shape
    video = cv.VideoWriter(video_path, 0, 1, (width, height))
    for frame_path in frames_paths_list:
        frame_array = cv.imread(frame_path)
        video.write(frame_array)
    video.release()


def get_files_from_directory(directory):
    directory_files_paths_list = os.listdir(directory)
    correct_directory_files_paths_list = []
    for file in directory_files_paths_list:
        if file.endswith(".tif"):
            file_path = os.path.join(directory, file)
            correct_directory_files_paths_list.append(file_path)
    if correct_directory_files_paths_list:
        correct_directory_files_paths_list.pop()
    return correct_directory_files_paths_list


def delete_frames(frames_paths_list):
    for frame_path in frames_paths_list:
        os.remove(frame_path)


def set_save_name(image_path_sample, save_directory, extension=".avi"):
    image_path_sample = image_path_sample.replace("\\", "/")
    initial_path = save_directory
    filename = image_path_sample.split('/')[-5] + " - " + image_path_sample.split('/')[-4] + " - " + \
                image_path_sample.split('/')[-3] + " - " + image_path_sample.split('/')[-2]
    save_path = initial_path + filename + extension
    return save_path
