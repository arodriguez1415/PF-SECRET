import os
from tkinter import filedialog, Tk
from cv2 import cv2
import numpy as np

from src.Constants import configuration_constants, string_constants


def get_video_as_array(video_path):
    return get_video_frames_as_array(video_path)


def get_video_path():
    root = Tk()
    root.withdraw()
    initial_absolute_directory_path = os.path.abspath(configuration_constants.MASK_VIDEOS)
    video_path = filedialog.askopenfilename(initialdir=initial_absolute_directory_path,
                                            title=string_constants.CHOOSE_VIDEO_WINDOW,
                                            filetypes=[("Video file", "*.avi"),
                                                       ("avi", "*.AVI"),
                                                       ("All files", "*")])
    root.destroy()
    return video_path


def get_multiple_videos_path():
    root = Tk()
    root.withdraw()
    initial_absolute_directory_path = os.path.abspath(configuration_constants.MASK_VIDEOS)
    file_path_list = filedialog.askopenfilenames(initialdir=initial_absolute_directory_path,
                                                 title=string_constants.CHOOSE_MULTIPLE_VIDEOS_WINDOW,
                                                 filetypes=[("Video file", "*.avi"),
                                                            ("avi", "*.AVI"),
                                                            ("All files", "*")])
    root.destroy()
    return file_path_list


def is_video(video_path):
    extension = os.path.splitext(video_path)[1]
    admitted_extensions = [".avi"]

    if extension not in admitted_extensions:
        return False

    return True


def are_videos(videos_path_list):
    flag = True
    for i in range(0, len(videos_path_list)):
        flag = flag and is_video(videos_path_list[i])

    return flag


def get_video_frames_as_array(video_path):
    cap = cv2.VideoCapture(video_path)
    frameCount = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frameWidth = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frameHeight = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    array_images_list = np.empty((frameCount, frameHeight, frameWidth, 3), np.dtype('uint8'))

    current_frame_index = 0
    ret = True

    while current_frame_index < frameCount and ret:
        ret, array_images_list[current_frame_index] = cap.read()
        current_frame_index += 1

    cap.release()
    return array_images_list
