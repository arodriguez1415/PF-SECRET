from src.Backend.Image_processing_algorithms.Operations import common_operations
from src.Frontend.Utils import progress_bar
from src.Constants import string_constants


def get_area_over_time(array_images_list):
    perimeter_values_list = []
    threshold_value = 50
    for i in range(0, len(array_images_list)):
        if progress_bar.is_progress_bar_cancelled():
            return None
        grayscale_array_image = common_operations.rgb_to_gray(array_images_list[i])
        threshold_array_image = common_operations.threshold(grayscale_array_image, threshold_value)
        perimeter = get_area(threshold_array_image)
        perimeter_values_list.append(perimeter)
        progress_bar.increment_value_progress_bar()
    return perimeter_values_list


def get_area(matrix):
    rows, cols = matrix.shape
    area = 0
    for row in range(rows):
        for col in range(cols):
            if matrix[row][col] == 255:
                area += 1
    return area
