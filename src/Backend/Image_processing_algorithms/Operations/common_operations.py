import numpy as np
from cv2 import cv2
import matplotlib.pyplot as plt


def normalize(array):
    array2 = array - 15
    result = array2 * (255.0 / array2.max())
    return result.astype(np.uint8)


def normalize_from_pil_image(pil_image):
    image_data = np.array(pil_image)
    image_width = pil_image.width
    image_height = pil_image.height
    dst = np.zeros((image_height, image_width))
    dst = cv2.normalize(image_data, dst, 0, 255, cv2.NORM_MINMAX, cv2.CV_8UC1)
    return dst


def normalize_to_range(array, max_value=255):
    array2 = array - array.min()
    if array2.min() == array2.max():
        return array.astype(np.uint8)
    result = array2 * (max_value / array2.max())
    return result.astype(np.uint8)


def is_RGB(image_array):
    dimensions = len(image_array.shape)
    two_dimensions = 2
    if dimensions == two_dimensions:
        return False
    else:
        return True


def gray_to_rgb(image_array):
    if not is_RGB(image_array):
        return cv2.cvtColor(image_array, cv2.COLOR_GRAY2RGB)
    return image_array


def rgb_to_gray(image_array):
    if is_RGB(image_array):
        return cv2.cvtColor(image_array, cv2.COLOR_BGR2GRAY)
    return image_array


def bgr_to_rgb(image_array):
    rgb_image_array = cv2.cvtColor(image_array, cv2.COLOR_BGR2RGB)
    return rgb_image_array


def threshold(image_array, threshold_value):
    image_array[image_array < threshold_value] = 0
    image_array[image_array >= threshold_value] = 255
    return image_array


def generate_coloured_heatmap(matrix):
    bgr_coloured_matrix = cv2.applyColorMap(matrix, cv2.COLORMAP_HOT)
    rgb_coloured_matrix = cv2.cvtColor(bgr_coloured_matrix, cv2.COLOR_BGR2RGB)
    return rgb_coloured_matrix


def resize_image(image_array, width, height):
    new_dimension = (width, height)
    resized_image = cv2.resize(image_array.astype("uint8"), new_dimension)
    return resized_image


def show_coloured_image(rgb_coloured_matrix, label):
    plt.axis('off')
    plt.imshow(rgb_coloured_matrix, cmap="hot")
    plt.colorbar(label=label, orientation="vertical")
    mng = plt.get_current_fig_manager()
    mng.window.showMaximized()
    plt.show()
