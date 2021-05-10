import numpy as np
from cv2 import cv2


def normalize(array):
    array2 = array - array.min()
    result = array2 * (255.0 / array2.max())
    return result.astype(np.uint8)


def normalize_from_pil_image(pil_image):
    image_data = np.array(pil_image)
    image_width = pil_image.width
    image_height = pil_image.height
    dst = np.zeros((image_height, image_width))
    dst = cv2.normalize(image_data, dst, 0, 255, cv2.NORM_MINMAX, cv2.CV_8UC1)
    return dst



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
