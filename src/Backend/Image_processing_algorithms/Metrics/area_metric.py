from src.Backend.Image_processing_algorithms.Operations import common_operations
from src.Frontend.Utils import progress_bar
import numpy as np


def get_area_over_time(array_images_list):
    area_values_list = []
    threshold_value = 50
    for i in range(0, len(array_images_list)):
        if progress_bar.is_progress_bar_cancelled():
            return None
        grayscale_array_image = common_operations.rgb_to_gray(array_images_list[i])
        threshold_array_image = common_operations.threshold(grayscale_array_image, threshold_value)
        area = np.sum(threshold_array_image == 255)
        area_values_list.append(area)
        progress_bar.increment_value_progress_bar()
    return area_values_list
