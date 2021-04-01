import numpy as np
from cv2 import cv2


def normalize(array):
    array2 = array - array.min()
    result = array2 * (255.0 / array2.max())
    return result.astype(np.uint8)


def is_RGB(image_array):
    dimensions = len(image_array.shape)
    if dimensions == 2:
        return False
    else:
        return True


def rgb_to_gray(image_array):
    if is_RGB(image_array):
        return cv2.cvtColor(image_array, cv2.COLOR_BGR2GRAY)
    return image_array


def threshold(image_array, threshold_value):
    image_array[image_array < threshold_value] = 0
    image_array[image_array >= threshold_value] = 255
    return image_array
