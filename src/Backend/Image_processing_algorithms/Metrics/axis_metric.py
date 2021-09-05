import cv2 as cv
import numpy as np

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
        # show_image(row_axis, col_axis, threshold_array_image)
        ratio = row_axis_diameter / col_axis_diameter
        axis_ratio_values_list.append(ratio)
        progress_bar.increment_value_progress_bar()
    return axis_ratio_values_list


def get_row_axis(image_array):
    rows, cols = image_array.shape

    rows_sum_list = []
    for i in range(0, rows):
        rows_sum_list.append(np.sum(image_array[i, :]))

    return np.max(rows_sum_list), np.argmax(rows_sum_list, axis=0)


def get_col_axis(image_array):
    rows, cols = image_array.shape

    cols_sum_list = []
    for i in range(0, cols):
        cols_sum_list.append(np.sum(image_array[:, i]))

    return np.max(cols_sum_list), np.argmax(cols_sum_list, axis=0)


def show_image(row_axis, col_axis, threshold_array_image):
    rows, cols = threshold_array_image.shape
    color = (0, 255, 0)
    thickness = 3
    threshold_array_image = common_operations.gray_to_rgb(threshold_array_image)
    cv.line(threshold_array_image, (0, row_axis), (cols, row_axis), color, thickness)
    image = cv.line(threshold_array_image, (col_axis, 0), (col_axis, rows), color, thickness)
    cv.imshow("Image", image)

