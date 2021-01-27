from src.Constants import configuration_constants as configuration_constants
from src.Classes.Project_mastermind import Project_mastermind
from PIL import Image
import cv2 as cv
import numpy as np
import os


def generate_video():
    os.mkdir(configuration_constants.TEMPORARY_VIDEO_DIRECTORY_PATH)
    images_paths_list = get_original_images()
    frames_paths_list = generate_frames(images_paths_list)
    save_video(frames_paths_list)
    delete_frames(frames_paths_list)
    os.rmdir(configuration_constants.TEMPORARY_VIDEO_DIRECTORY_PATH)


def get_original_images():
    project_mastermind = Project_mastermind.get_instance()
    original_directory = project_mastermind.get_original_image_directory()
    images_list_paths = get_files_from_directory(original_directory)
    return images_list_paths
    # generate_frames(images_list_paths)
    # frame_list = [img for img in os.listdir(path_constants.GENERATED_VIDEO_IMAGES) if img.endswith(".tif")]
    # generate_video(path_constants.GENERATED_VIDEO_IMAGES, frame_list)


def generate_frames(images_path, apply_methods_flag=False):
    index = 0
    frames_paths_list = []
    for image_path in images_path:
        image = Image.open(image_path)
        image_array = np.uint8(image)
        frame_path = configuration_constants.TEMPORARY_VIDEO_DIRECTORY_PATH + "frame" + str(index) + ".tif"
        if apply_methods_flag:
            print("JE")
            # image = apply_methods(image)
        cv.imwrite(frame_path, np.uint8(image_array))
        frames_paths_list.append(frame_path)
        index = index + 1
    return frames_paths_list


# Cambiar como se genera el path, preguntando que nombre quiere
def save_video(frames_paths_list):
    height, width, layers = cv.imread(frames_paths_list[0]).shape
    video_path = Project_mastermind.get_instance().create_video_path_name("video_name")
    video = cv.VideoWriter(video_path, 0, 1, (width, height))
    for frame_path in frames_paths_list:
        frame_array = cv.imread(frame_path)
        video.write(frame_array)
    video.release()
    return video_path


def get_files_from_directory(directory):
    directory_files_paths_list = os.listdir(directory)
    correct_directory_files_paths_list = []
    for file in directory_files_paths_list:
        if file.endswith(".tif"):
            file_path = os.path.join(directory, file)
            correct_directory_files_paths_list.append(file_path)
    return correct_directory_files_paths_list


def delete_frames(frames_paths_list):
    for frame_path in frames_paths_list:
        os.remove(frame_path)
