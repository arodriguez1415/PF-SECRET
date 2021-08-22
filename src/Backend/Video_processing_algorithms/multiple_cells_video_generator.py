from PIL import Image
import numpy as np

from src.Backend.Image_processing_algorithms.Archive_manipulation.file_manipulation import \
    create_directory_if_not_exists, remove_directory
from src.Backend.Image_processing_algorithms.Archive_manipulation.image_file_manipulation import \
    get_images_from_directories
from src.Backend.Image_processing_algorithms.Archive_manipulation.video_file_manipulation import \
    get_video_frames_as_array
from src.Backend.Image_processing_algorithms.Border_detection.mgac import map_borders
from src.Backend.Image_processing_algorithms.Operations.common_operations import gray_to_rgb, resize_image
from src.Backend.Image_processing_algorithms.Operations.image_save import save_image
from src.Backend.Video_processing_algorithms import video_generator
from src.Classes.Methods.Adaptive_threshold import Adaptive_threshold
from src.Classes.Methods.Anisotropic_Filter import Anisotropic_Filter
from src.Classes.Project_mastermind import Project_mastermind
from src.Constants.algorithm_constants import CONTOUR_VIDEO, SIMPLE_CELL_VIDEO, COMPARISON_VIDEO
from src.Frontend.Utils import progress_bar
from src.Classes.Methods.Mgac import Mgac
from src.Classes.Region import Region
from src.Constants import configuration_constants
from src.Constants import properties_constants as ps


def generate_mask_video_of_all_cells(source_directory):
    images_list_of_lists = get_images_from_directories(source_directory)
    masked_videos_paths_list = []
    for images_list_paths in images_list_of_lists:
        if progress_bar.is_progress_bar_cancelled():
            return None
        specified_methods_to_apply = set_methods_to_apply(images_list_paths[0])
        video_path = video_generator.generate_video(images_list=images_list_paths,
                                                    feature_type=CONTOUR_VIDEO,
                                                    specified_methods_to_apply=specified_methods_to_apply)
        masked_videos_paths_list.append(video_path)
    return masked_videos_paths_list


def generate_video_of_all_cells(source_directory):
    images_list_of_lists = get_images_from_directories(source_directory)
    cells_videos_paths_list = []
    for images_list_paths in images_list_of_lists:
        if progress_bar.is_progress_bar_cancelled():
            return None
        video_path = video_generator.generate_video(images_list=images_list_paths,
                                                    feature_type=SIMPLE_CELL_VIDEO,
                                                    specified_methods_to_apply=[],
                                                    save_directory=configuration_constants.CELLS_VIDEOS)
        cells_videos_paths_list.append(video_path)
    return cells_videos_paths_list


def generate_video_comparator_of_all_cells(cell_videos, mask_videos):
    comparison_videos_paths_list = []
    for i in range(0, len(mask_videos)):
        if progress_bar.is_progress_bar_cancelled():
            return None
        setup()
        cell_images_array_list = get_video_frames_as_array(cell_videos[i])
        mask_images_array_list = get_video_frames_as_array(mask_videos[i])
        comparison_images_path_list = generate_comparison(cell_images_array_list,
                                                          mask_images_array_list)
        video_path = video_generator.generate_video(images_list=comparison_images_path_list,
                                                    feature_type=COMPARISON_VIDEO,
                                                    specified_methods_to_apply=[],
                                                    save_directory=configuration_constants.COMPARISON_VIDEOS)
        comparison_videos_paths_list.append(video_path)
    remove_directory(configuration_constants.TEMPORARY_VIDEO_DIRECTORY_PATH)
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
    props_dict = Project_mastermind.get_instance().get_properties_dictionary()
    methods_to_apply = set_preprocessed_methods(methods_to_apply, props_dict)
    preprocessed_image = video_generator.apply_methods_specified(cell_image, methods_to_apply)

    return preprocessed_image


def set_methods_to_apply(image_path):
    methods_to_apply = []
    props_dict = Project_mastermind.get_instance().get_properties_dictionary()
    methods_to_apply = set_preprocessed_methods(methods_to_apply, props_dict)
    methods_to_apply = set_mgac_method(methods_to_apply, image_path, props_dict)
    return methods_to_apply


def set_preprocessed_methods(methods_to_apply, props_dict):
    anisotropic_method = Anisotropic_Filter(props_dict[ps.GLOBAL_ROUTINE_ANISOTROPIC_FILTER_TIMES])
    methods_to_apply.append(anisotropic_method)

    adaptive_threshold_window_size = props_dict[ps.GLOBAL_ROUTINE_ADAPTIVE_THRESHOLD_WINDOW_SIZE]
    adaptive_threshold_c_constant = props_dict[ps.GLOBAL_ROUTINE_ADAPTIVE_C_CONSTANT]
    adaptive_threshold_method_type = props_dict[ps.GLOBAL_ROUTINE_ADAPTIVE_METHOD]
    adaptive_threshold_method = Adaptive_threshold(adaptive_threshold_window_size,
                                                   adaptive_threshold_c_constant,
                                                   adaptive_threshold_method_type)
    methods_to_apply.append(adaptive_threshold_method)

    return methods_to_apply


def set_mgac_method(methods_to_apply, image_path, props_dict):
    image = Image.open(image_path)
    image_array = np.uint8(image)
    polygon_region = Region.get_all_image_as_region(image_array)
    mgac_iterations = props_dict[ps.GLOBAL_ROUTINE_MGAC_ITERATIONS]
    mgac_threshold = props_dict[ps.GLOBAL_ROUTINE_MGAC_THRESHOLD]
    mgac_smoothing = props_dict[ps.GLOBAL_ROUTINE_MGAC_SMOOTHING]
    mgac_balloon = props_dict[ps.GLOBAL_ROUTINE_MGAC_BALLOON]
    mgac_alpha = props_dict[ps.GLOBAL_ROUTINE_MGAC_ALPHA]
    mgac_sigma = props_dict[ps.GLOBAL_ROUTINE_MGAC_SIGMA]

    mgac_method = Mgac(polygon_region, mgac_iterations, mgac_threshold, mgac_smoothing,
                       mgac_balloon, mgac_alpha, mgac_sigma, mask_flag=True)
    methods_to_apply.append(mgac_method)

    return methods_to_apply


def get_images(images_list_of_lists):
    total_length = 0
    for images_list_paths in images_list_of_lists:
        total_length += len(images_list_paths)
    return total_length


def setup():
    create_directory_if_not_exists(configuration_constants.TEMPORARY_VIDEO_DIRECTORY_PATH)
