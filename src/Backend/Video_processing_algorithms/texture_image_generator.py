import os
from PIL import Image
import cv2
import numpy as np

from src.Backend.Image_processing_algorithms.Archive_manipulation.dataframe_file_manipulation import \
    create_dataframe_from_descriptors
from src.Backend.Image_processing_algorithms.Archive_manipulation.file_manipulation import \
    create_directory_if_not_exists, remove_directory
from src.Backend.Image_processing_algorithms.Archive_manipulation.image_file_manipulation import \
    get_images_from_directories
from src.Backend.Image_processing_algorithms.Archive_manipulation.save_file_manipulation import set_save_name
from src.Backend.Image_processing_algorithms.Operations.common_operations import bgr_to_rgb, resize_image
from src.Backend.Image_processing_algorithms.Texture.k_means import get_descriptors, k_means
from src.Backend.Video_processing_algorithms import video_generator
from src.Classes.Methods.Anisotropic_Filter import Anisotropic_Filter
from src.Classes.Project_mastermind import Project_mastermind
from src.Constants import configuration_constants, algorithm_constants, string_constants
from src.Constants import properties_constants as ps
from src.Frontend.Utils import progress_bar


def classify_single_image(image_array, clusters_quantity=20):
    descriptors_labels = [algorithm_constants.GLCM_MEAN, algorithm_constants.GLCM_ENTROPY,
                          algorithm_constants.GLCM_HOMOGENEITY, algorithm_constants.GLCM_DISSIMILARITY]
    list_descriptors_dict = []
    list_descriptors_dict = get_descriptors(list_descriptors_dict, image_array, descriptors_labels)
    dataframe = create_dataframe_from_descriptors(list_descriptors_dict)
    uncoloured_classified_image = k_means(dataframe, clusters_quantity=clusters_quantity)
    coloured_classified_image = bgr_to_rgb(cv2.applyColorMap(uncoloured_classified_image, cv2.COLORMAP_HOT))
    return uncoloured_classified_image, coloured_classified_image


def create_multiple_texture_images(threshold, clusters_quantity, source_directory):
    images_list_of_lists = get_images_from_directories(source_directory)
    texture_images_array_list = []
    texture_images_path = []
    for i in range(0, len(images_list_of_lists)):
        if progress_bar.is_progress_bar_cancelled():
            return None
        uncoloured_classified_image, coloured_classified_image = create_texture_image_from_video(images_list_of_lists[i],
                                                                                                 clusters_quantity,
                                                                                                 threshold)
        texture_images_array_list.append(coloured_classified_image)
        save_directory = configuration_constants.TEXTURE_HEATMAP_IMAGES_DIRECTORY
        save_texture_path = set_save_name(algorithm_constants.TEXTURE_IMAGE, save_directory,
                                                          extension=".png")
        save_texture_image(coloured_classified_image, save_texture_path)
        texture_images_path.append(save_texture_path)
    return texture_images_array_list, texture_images_path


def create_texture_image_from_video(images_path_for_texture_list=None, clusters_quantity=20, threshold=15):
    images_path_for_texture_list = get_images(images_path_for_texture_list)
    setup(images_path_for_texture_list)
    frames_path_list = generate_frames(images_path_for_texture_list)
    uncoloured_classified_image, coloured_classified_image = get_texture_image(frames_path_list,
                                                                               clusters_quantity, threshold)
    video_generator.delete_frames(frames_path_list)
    remove_directory(configuration_constants.TEMPORARY_VIDEO_DIRECTORY_PATH)
    return uncoloured_classified_image, coloured_classified_image


def setup(images_path_for_texture_list):
    progress_bar.start_progress_bar(string_constants.GENERATE_TEXTURE_HEAT_MAP_TITLE,
                                    string_constants.GENERATE_TEXTURE_HEAT_MAP_DESCRIPTION,
                                    len(images_path_for_texture_list) * 2 + 1)
    create_directory_if_not_exists(configuration_constants.GENERATED_IMAGES_DIR)
    create_directory_if_not_exists(configuration_constants.GLOBAL_ROUTINE_DIRECTORY)
    create_directory_if_not_exists(configuration_constants.TEMPORARY_VIDEO_DIRECTORY_PATH)
    create_directory_if_not_exists(configuration_constants.TEXTURE_HEATMAP_IMAGES_DIRECTORY)


def get_images(images_path_for_texture_list):
    if images_path_for_texture_list is None:
        images_path_for_texture_list = video_generator.get_original_images()
    return images_path_for_texture_list


def generate_frames(images_path_for_texture_list):
    specified_methods_to_apply = set_methods_to_apply()
    frames_paths_list = video_generator.generate_frames(images_path_for_texture_list,
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


def get_texture_image(images_path_list, clusters_quantity, threshold):
    height, width = get_grayscale(images_path_list[0]).shape
    accumulated_texture = np.zeros((width, height), np.uint8)
    accumulated_texture = resize_image(accumulated_texture, width, height)
    descriptors_labels = [algorithm_constants.GLCM_MEAN, algorithm_constants.GLCM_ENTROPY,
                          algorithm_constants.GLCM_HOMOGENEITY, algorithm_constants.GLCM_DISSIMILARITY]
    for i in range(0, len(images_path_list)):
        current_image_array = get_grayscale(images_path_list[i])
        current_image_array = resize_image(current_image_array, width, height)
        ret, current_image_array = cv2.threshold(current_image_array, threshold, 255, cv2.THRESH_BINARY)
        accumulated_texture += current_image_array
        progress_bar.increment_value_progress_bar()
    accumulated_motion = normalize_values(accumulated_texture)
    list_descriptors_dict = []
    list_descriptors_dict = get_descriptors(list_descriptors_dict, accumulated_motion, descriptors_labels)
    dataframe = create_dataframe_from_descriptors(list_descriptors_dict)
    uncoloured_classified_image = k_means(dataframe, clusters_quantity=clusters_quantity)
    progress_bar.increment_value_progress_bar()
    coloured_classified_image = bgr_to_rgb(cv2.applyColorMap(uncoloured_classified_image, cv2.COLORMAP_HOT))
    return uncoloured_classified_image, coloured_classified_image


def normalize_values(accumulated_motion):
    max_value = np.max(accumulated_motion)
    rows, cols = accumulated_motion.shape
    for row in range(rows):
        for col in range(cols):
            accumulated_motion[row][col] = accumulated_motion[row][col] * 255 / max_value
    return accumulated_motion


def get_grayscale(image_path):
    frame = cv2.imread(os.path.join(image_path))
    rows, cols, dimensions = frame.shape
    grayscale_frame = np.zeros((rows, cols), np.uint8)
    for row in range(rows):
        for col in range(cols):
            grayscale_frame[row][col] = frame[row][col][0]
    return grayscale_frame


def save_texture_image(texture_image_array, save_texture_path):
    im = Image.fromarray(texture_image_array)
    im.save(save_texture_path)
