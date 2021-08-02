import os

from PIL import Image
import cv2
import numpy as np
import matplotlib.pyplot as plt

from src.Backend.Image_processing_algorithms.Archive_manipulation.dataframe_file_manipulation import \
    create_dataframe_from_descriptors
from src.Backend.Image_processing_algorithms.Operations.common_operations import bgr_to_rgb
from src.Backend.Image_processing_algorithms.Texture.unsupervised_learning_methods import get_descriptors, k_means
from src.Backend.Video_processing_algorithms import video_generator
from src.Backend.Video_processing_algorithms.multiple_cells_video_generator import get_images_from_directories
from src.Classes.Methods.Anisotropic_Filter import Anisotropic_Filter
from src.Constants import configuration_constants, algorithm_constants


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
        uncoloured_classified_image, coloured_classified_image = create_texture_image_from_video(images_list_of_lists[i],
                                                                                                 clusters_quantity,
                                                                                                 threshold)
        texture_images_array_list.append(coloured_classified_image)
        save_directory = configuration_constants.TEXTURE_HEATMAP_IMAGES_DIRECTORY
        save_texture_path = video_generator.set_save_name(images_list_of_lists[i][0], save_directory,
                                                          extension=".png")
        save_texture_image(coloured_classified_image, save_texture_path)
        texture_images_path.append(save_texture_path)
    return texture_images_array_list, texture_images_path


def create_texture_image_from_video(images_path_for_texture_list=None, clusters_quantity=20, threshold=15):
    setup_directories()
    images_path_for_texture_list = get_images(images_path_for_texture_list)
    frames_path_list = generate_frames(images_path_for_texture_list)
    uncoloured_classified_image, coloured_classified_image = get_texture_image(frames_path_list,
                                                                               clusters_quantity, threshold)
    video_generator.delete_frames(frames_path_list)
    os.rmdir(configuration_constants.TEMPORARY_VIDEO_DIRECTORY_PATH)
    return uncoloured_classified_image, coloured_classified_image


def setup_directories():
    create_directory_if_not_exists(configuration_constants.TEMPORARY_VIDEO_DIRECTORY_PATH)
    create_directory_if_not_exists(configuration_constants.TEXTURE_HEATMAP_IMAGES_DIRECTORY)


def create_directory_if_not_exists(directory_path):
    if not os.path.isdir(directory_path):
        os.mkdir(directory_path)


def get_images(images_path_for_texture_list):
    if images_path_for_texture_list is None:
        images_path_for_texture_list = video_generator.get_original_images()
    return images_path_for_texture_list


def generate_frames(images_path_for_texture_list):
    specified_methods_to_apply = set_methods_to_apply()
    frames_paths_list = video_generator.generate_frames(images_path_for_texture_list, specified_methods_to_apply)
    return frames_paths_list


def set_methods_to_apply():
    methods_to_apply = []
    anisotropic_method = Anisotropic_Filter()
    methods_to_apply.append(anisotropic_method)
    methods_to_apply.append(anisotropic_method)
    methods_to_apply.append(anisotropic_method)
    return methods_to_apply


def get_texture_image(images_path_list, clusters_quantity, threshold):
    rows, cols = get_grayscale(images_path_list[0]).shape
    accumulated_texture = np.zeros((rows, cols), np.uint8)
    descriptors_labels = [algorithm_constants.GLCM_MEAN, algorithm_constants.GLCM_ENTROPY,
                          algorithm_constants.GLCM_HOMOGENEITY, algorithm_constants.GLCM_DISSIMILARITY]
    for i in range(0, len(images_path_list)):
        current_image_array = get_grayscale(images_path_list[i])
        ret, current_image_array = cv2.threshold(current_image_array, threshold, 255, cv2.THRESH_BINARY)
        accumulated_texture += current_image_array
    accumulated_motion = normalize_values(accumulated_texture)
    list_descriptors_dict = []
    list_descriptors_dict = get_descriptors(list_descriptors_dict, accumulated_motion, descriptors_labels)
    dataframe = create_dataframe_from_descriptors(list_descriptors_dict)
    uncoloured_classified_image = k_means(dataframe, clusters_quantity=clusters_quantity)
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
