import os

from src.Backend.Image_processing_algorithms.Archive_manipulation import image_file_manipulation
from src.Backend.Video_processing_algorithms import video_generator
from src.Classes.Project_mastermind import Project_mastermind
from src.Constants import string_constants
from src.Frontend.Utils import message


def generate_border_detection_video():
    project_mastermind = Project_mastermind.get_instance()
    image_processing_list = project_mastermind.get_image_processing_list()
    if len(image_processing_list) <= 1 or image_processing_list[-1].method.name != string_constants.MGAC_METHOD_NAME:
        message.show_error(string_constants.NO_MGAC_METHOD_ERROR)
        return
    set_mask_flag(False)
    video_generator.generate_video()


def generate_mask_video():
    project_mastermind = Project_mastermind.get_instance()
    image_processing_list = project_mastermind.get_image_processing_list()
    if len(image_processing_list) <= 1 or image_processing_list[-1].method.name != string_constants.MGAC_METHOD_NAME:
        message.show_error(string_constants.NO_MGAC_METHOD_ERROR)
        return
    set_mask_flag(True)
    video_generator.generate_video()


def set_mask_flag(mask_flag):
    project_mastermind = Project_mastermind.get_instance()
    image_processing_list = project_mastermind.get_image_processing_list()
    mgac_borders_method = image_processing_list[-1]
    mgac_borders_method.method.set_mask_flag(mask_flag)
    image_processing_list[-1] = mgac_borders_method
    project_mastermind.set_image_processing_list(image_processing_list)



