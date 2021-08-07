import os

from PIL import Image
import numpy as np

from src.Backend.Image_processing_algorithms.Archive_manipulation import image_file_manipulation
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
    anisotropic_method = Anisotropic_Filter()
    adaptive_threshold_method = Adaptive_threshold(21, 5, algorithm_constants.ADAPTIVE_THRESHOLD_GAUSSIAN)
    image = Image.open(image_path)
    image_array = np.uint8(image)
    polygon_region = Region.get_all_image_as_region(image_array)
    mgac_method = Mgac(polygon_region, 250, 0.35, 0, -1, 200, 2, True)
    methods_to_apply.append(anisotropic_method)
    methods_to_apply.append(anisotropic_method)
    methods_to_apply.append(anisotropic_method)
    methods_to_apply.append(adaptive_threshold_method)
    methods_to_apply.append(mgac_method)
    return methods_to_apply


def get_images(images_list_of_lists):
    total_length = 0
    for images_list_paths in images_list_of_lists:
        total_length += len(images_list_paths)
    return total_length


# Posible para borrar
def set_save_name(image_path_sample):
    image_path_sample = image_path_sample.replace("\\", "/")
    save_path = image_path_sample.split('/')[-5] + " - " + image_path_sample.split('/')[-4] + " - " + \
                image_path_sample.split('/')[-3] + " - " + image_path_sample.split('/')[-2]
    return save_path
