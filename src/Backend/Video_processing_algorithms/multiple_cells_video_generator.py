import os
import shutil

from PIL import Image
import numpy as np
from matplotlib import pyplot as plt

from src.Backend.Image_processing_algorithms.Archive_manipulation import image_file_manipulation
from src.Backend.Image_processing_algorithms.Archive_manipulation.video_file_manipulation import \
    get_video_frames_as_array
from src.Backend.Image_processing_algorithms.Border_detection.mgac import map_borders
from src.Backend.Image_processing_algorithms.Operations.common_operations import gray_to_rgb, resize_image
from src.Backend.Image_processing_algorithms.Operations.image_save import save_image
from src.Backend.Video_processing_algorithms import video_generator
from src.Classes.Methods.Adaptive_threshold import Adaptive_threshold
from src.Classes.Methods.Anisotropic_Filter import Anisotropic_Filter
from src.Frontend.Utils import progress_bar
from src.Classes.Methods.Mgac import Mgac
from src.Classes.Region import Region
from src.Constants import algorithm_constants, configuration_constants


def generate_mask_video_of_all_cells(source_directory):
    images_list_of_lists = get_images_from_directories(source_directory)
    masked_videos_paths_list = []
    for images_list_paths in images_list_of_lists:
        if progress_bar.is_progress_bar_cancelled():
            return None
        specified_methods_to_apply = set_methods_to_apply(images_list_paths[0])
        video_path = video_generator.generate_video(images_list=images_list_paths,
                                                    specified_methods_to_apply=specified_methods_to_apply)
        masked_videos_paths_list.append(video_path)
    return masked_videos_paths_list


def generate_video_of_all_cells(source_directory):
    images_list_of_lists = get_images_from_directories(source_directory)
    cells_videos_paths_list = []
    for images_list_paths in images_list_of_lists:
        video_path = video_generator.generate_video(images_list=images_list_paths,
                                                    save_directory=configuration_constants.CELLS_VIDEOS)
        cells_videos_paths_list.append(video_path)
    return cells_videos_paths_list


def generate_video_comparator_of_all_cells(cell_videos, mask_videos):
    comparison_videos_paths_list = []
    for i in range(0, len(mask_videos)):
        setup()
        cell_images_array_list = get_video_frames_as_array(cell_videos[i])
        mask_images_array_list = get_video_frames_as_array(mask_videos[i])
        comparison_images_path_list = generate_comparison(cell_images_array_list,
                                                          mask_images_array_list)
        video_path = video_generator.generate_video(images_list=comparison_images_path_list,
                                                    save_directory=configuration_constants.COMPARISON_VIDEOS)
        comparison_videos_paths_list.append(video_path)
    shutil.rmtree(configuration_constants.TEMPORARY_VIDEO_DIRECTORY_PATH, ignore_errors=True)
    return comparison_videos_paths_list


def generate_comparison(cell_images_array_list, mask_images_array_list):
    width = configuration_constants.IMAGE_VIEWER_WIDTH
    height = configuration_constants.IMAGE_VIEWER_HEIGHT
    comparison_path_list = []
    for i in range(0, len(cell_images_array_list)):
        cell_image = resize_image(cell_images_array_list[i], width, height)
        mask_image = resize_image(mask_images_array_list[i], width, height)
        mask_image = gray_to_rgb(mask_image)
        preprocessed_image = generate_preprocessed_image(cell_image)
        preprocessed_image = gray_to_rgb(preprocessed_image)
        cell_with_borders_images_array, preprocessed_image_with_borders_array = map_borders(cell_image,
                                                                                            preprocessed_image,
                                                                                            mask_image)
        save_path = configuration_constants.TEMPORARY_VIDEO_DIRECTORY_PATH + "frame - " + str(i) + ".tif"
        generate_comparison_figure(cell_with_borders_images_array, preprocessed_image_with_borders_array,
                                   mask_image, save_path)
        comparison_path_list.append(save_path)
    return comparison_path_list


def generate_comparison_figure(cell_image, preprocessed_image, mask_image, save_path):
    width = configuration_constants.IMAGE_VIEWER_WIDTH
    black_space = np.zeros((width, 100, 3))
    comparison_image_array = np.concatenate((cell_image, black_space, preprocessed_image,
                                             black_space, mask_image), axis=1)
    save_image(comparison_image_array, save_path)


def generate_preprocessed_image(cell_image):
    methods_to_apply = []
    methods_to_apply = set_preprocessed_methods(methods_to_apply)
    preprocessed_image = video_generator.apply_methods_specified(cell_image, methods_to_apply)

    return preprocessed_image


def get_images_from_directories(source_directory):
    directories_list = os.walk(get_source_directory(source_directory))
    images_list_of_lists = []
    filtered_list_of_lists = []
    for directory_wrapper in directories_list:
        directory_path = directory_wrapper[0]
        images_list_of_lists.append(video_generator.get_files_from_directory(directory_path))
    for images_list in images_list_of_lists:
        if images_list:
            filtered_list_of_lists.append(images_list)
    return filtered_list_of_lists


def get_source_directory(source_directory=None):
    if source_directory is None:
        source_directory = image_file_manipulation.get_directory_path()
    return source_directory


def set_methods_to_apply(image_path):
    methods_to_apply = []
    methods_to_apply = set_preprocessed_methods(methods_to_apply)
    methods_to_apply = set_mgac_method(methods_to_apply, image_path)
    return methods_to_apply


def set_preprocessed_methods(methods_to_apply):
    anisotropic_method = Anisotropic_Filter()
    adaptive_threshold_method = Adaptive_threshold(21, 5, algorithm_constants.ADAPTIVE_THRESHOLD_GAUSSIAN)
    methods_to_apply.append(anisotropic_method)
    methods_to_apply.append(anisotropic_method)
    methods_to_apply.append(anisotropic_method)
    methods_to_apply.append(adaptive_threshold_method)

    return methods_to_apply


def set_mgac_method(methods_to_apply, image_path):
    image = Image.open(image_path)
    image_array = np.uint8(image)
    polygon_region = Region.get_all_image_as_region(image_array)
    mgac_method = Mgac(polygon_region, 250, 0.35, 0, -1, 200, 2, mask_flag=True)
    methods_to_apply.append(mgac_method)

    return methods_to_apply


def get_images(images_list_of_lists):
    total_length = 0
    for images_list_paths in images_list_of_lists:
        total_length += len(images_list_paths)
    return total_length


def setup():
    create_directory_if_not_exists(configuration_constants.TEMPORARY_VIDEO_DIRECTORY_PATH)


def create_directory_if_not_exists(directory_path):
    if not os.path.isdir(directory_path):
        os.mkdir(directory_path)
