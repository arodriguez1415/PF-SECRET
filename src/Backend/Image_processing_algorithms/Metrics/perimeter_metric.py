import cv2 as cv
import numpy as np

from src.Backend.Image_processing_algorithms.Operations import common_operations
from src.Frontend.Utils import progress_bar


def get_perimeter_over_time(array_images_list):
    perimeter_values_list = []
    threshold_value = 50
    for i in range(0, len(array_images_list)):
        if progress_bar.is_progress_bar_cancelled():
            return None
        grayscale_array_image = common_operations.rgb_to_gray(array_images_list[i])
        threshold_array_image = common_operations.threshold(grayscale_array_image, threshold_value)
        threshold_array_image = cv.Canny(threshold_array_image, threshold_value - 1, threshold_value - 1)
        perimeter = np.sum(threshold_array_image == 255)
        perimeter_values_list.append(perimeter)
        progress_bar.increment_value_progress_bar()
    return perimeter_values_list
