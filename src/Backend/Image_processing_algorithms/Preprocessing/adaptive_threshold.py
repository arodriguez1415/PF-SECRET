import numpy as np
import cv2 as cv

from src.Constants import algorithm_constants


def adaptive_threshold(image, window_size, constant, method):
    pixels = np.uint8(image)

    if window_size % 2 == 0:
        window_size = window_size + 1

    threshold_image = cv.adaptiveThreshold(pixels, 255, adaptiveMethod=method,
                                           thresholdType=cv.THRESH_BINARY, blockSize=window_size, C=constant)
    threshold_image = cv.bitwise_not(threshold_image)
    return threshold_image


def get_method(method_value):
    switcher = {
        "Umbralización de la media": algorithm_constants.ADAPTIVE_THRESHOLD_MEAN,
        "Umbralización gaussiana": algorithm_constants.ADAPTIVE_THRESHOLD_GAUSSIAN,
    }
    return switcher.get(method_value, "nothing")

def get_text_method(method_value):
    switcher = {
        algorithm_constants.ADAPTIVE_THRESHOLD_MEAN: "Umbralización de la media",
        algorithm_constants.ADAPTIVE_THRESHOLD_GAUSSIAN: "Umbralización gaussiana",
    }
    return switcher.get(method_value, "nothing")