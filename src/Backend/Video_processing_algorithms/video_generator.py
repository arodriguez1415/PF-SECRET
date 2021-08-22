from PIL import Image
import cv2 as cv
import numpy as np
import os

from src.Backend.Image_processing_algorithms.Archive_manipulation.file_manipulation import \
    create_directory_if_not_exists, remove_directory
from src.Backend.Image_processing_algorithms.Archive_manipulation.image_file_manipulation import \
    get_files_from_directory
from src.Backend.Image_processing_algorithms.Archive_manipulation.save_file_manipulation import set_save_name
from src.Backend.Image_processing_algorithms.Operations import common_operations
from src.Backend.Image_processing_algorithms.Operations.common_operations import resize_image
from src.Constants import configuration_constants, string_constants
from src.Classes.Project_mastermind import Project_mastermind
from src.Frontend.Utils import progress_bar
from src.Frontend.Utils.message import show_error_message


def generate_video(images_list=None, specified_methods_to_apply=None,
                   save_directory=configuration_constants.MASK_VIDEOS):
    images_paths_list = images_list
    if images_list is None:
        images_paths_list = get_original_images()

    setup(images_paths_list)
    frames_paths_list = generate_frames(images_paths_list, specified_methods_to_apply)
    save_video_path = set_save_name(images_paths_list[0], save_directory)
    save_video(frames_paths_list, save_video_path)
    delete_frames(frames_paths_list)
    remove_directory(configuration_constants.TEMPORARY_VIDEO_DIRECTORY_PATH)
    return save_video_path


def setup(images_paths_list):
    progress_bar.start_progress_bar(string_constants.GENERATE_VIDEO_TITLE,
                                    string_constants.GENERATE_VIDEO_DESCRIPTION, len(images_paths_list))
    create_directory_if_not_exists(configuration_constants.GENERATED_IMAGES_DIR)
    create_directory_if_not_exists(configuration_constants.TEMPORARY_VIDEO_DIRECTORY_PATH)
    create_directory_if_not_exists(configuration_constants.MASK_VIDEOS)


def get_original_images():
    project_mastermind = Project_mastermind.get_instance()
    original_directory = project_mastermind.get_original_image_dir()
    images_list_paths = get_files_from_directory(original_directory)

    if images_list_paths and len(images_list_paths) > 1:
        images_list_paths.pop()  # Last one is odd

    if images_list_paths and len(images_list_paths) == 0:
        show_error_message(string_constants.NO_IMAGE_LOADED)
        return
    return images_list_paths


def generate_frames(images_path, specified_methods_to_apply, apply_methods_flag=True):
    index = 0
    frames_paths_list = []
    for image_path in images_path:
        if progress_bar.is_progress_bar_cancelled():
            return None
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
        progress_bar.increment_value_progress_bar()
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
        resized_frame_array = resize_image(frame_array, width, height)
        video.write(resized_frame_array)
    video.release()


def delete_frames(frames_paths_list):
    for frame_path in frames_paths_list:
        os.remove(frame_path)
