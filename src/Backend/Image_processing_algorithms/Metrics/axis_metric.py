from src.Backend.Image_processing_algorithms.Operations import common_operations
from src.Frontend.Utils import progress_bar


def get_axis_ratio_over_time(array_images_list):
    axis_ratio_values_list = []
    threshold_value = 50
    for i in range(0, len(array_images_list)):
        if progress_bar.is_progress_bar_cancelled():
            return None
        grayscale_array_image = common_operations.rgb_to_gray(array_images_list[i])
        threshold_array_image = common_operations.threshold(grayscale_array_image, threshold_value)
        row_axis_diameter, row_axis = get_row_axis(threshold_array_image)
        col_axis_diameter, col_axis = get_col_axis(threshold_array_image)
        ratio = row_axis_diameter / col_axis_diameter
        axis_ratio_values_list.append(ratio)
        progress_bar.increment_value_progress_bar()
    return axis_ratio_values_list


def get_row_axis(matrix):
    rows, cols = matrix.shape
    max_row = 0
    max_consecutive_ones = 0
    for row in range(rows):
        consecutive_ones = 0
        for col in range(cols):
            if matrix[row][col] == 255:
                consecutive_ones += 1
            else:
                if consecutive_ones > max_consecutive_ones:
                    max_row = row
                    max_consecutive_ones = consecutive_ones
                consecutive_ones = 0
        if consecutive_ones > max_consecutive_ones:
            max_row = row
            max_consecutive_ones = consecutive_ones
    return max_consecutive_ones, max_row


def get_col_axis(matrix):
    rows, cols = matrix.shape
    max_col = 0
    max_consecutive_ones = 0
    for col in range(cols):
        consecutive_ones = 0
        for row in range(rows):
            if matrix[row][col] == 255:
                consecutive_ones += 1
            else:
                if consecutive_ones > max_consecutive_ones:
                    max_row = row
                    max_consecutive_ones = consecutive_ones
                consecutive_ones = 0
        if consecutive_ones > max_consecutive_ones:
            max_col = col
            max_consecutive_ones = consecutive_ones
    return max_consecutive_ones, max_col