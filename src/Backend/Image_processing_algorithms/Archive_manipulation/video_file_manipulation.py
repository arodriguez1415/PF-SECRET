import os
from tkinter import filedialog, Tk

from cv2 import cv2
import numpy as np

from src.Constants import configuration_constants


def get_video_as_array():
    video_path = get_video_path()
    return get_video_frames_as_array(video_path)


def get_video_path():
    root = Tk()
    root.withdraw()
    initial_absolute_directory_path = os.path.abspath(configuration_constants.GENERATED_IMAGES_DIR)
    video_path = filedialog.askopenfilename(initialdir=initial_absolute_directory_path, title='Choose Video',
                                            filetypes=[("Video file", "*.avi"),
                                                       ("avi", "*.AVI"),
                                                       ("All files", "*")])
    root.destroy()
    return video_path


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
