import os

import cv2
import numpy as np
from PIL import Image
from matplotlib import pyplot as plt
from matplotlib.path import Path
from scipy import ndimage as ndi
from src.Backend.Image_processing_algorithms.Border_detection import mgac_library_functions as mgac_library
from src.Backend.Image_processing_algorithms.Operations.common_operations import rgb_to_gray
from src.Backend.Image_processing_algorithms.Preprocessing.threshold import binary_threshold
from src.Constants import configuration_constants
from src.Constants import string_constants


def mgac(polygon_region, image, iterations, threshold, smoothing, ballon, alpha, sigma, show_process=False):
    borders = get_borders(polygon_region, image, iterations, threshold, smoothing, ballon, alpha, sigma, show_process)
    borders_image, mask_borders_image = get_mgac_image_and_mask(image, borders)
    return borders_image, mask_borders_image


def get_borders(polygon_region, image, iterations, threshold, smoothing, ballon, alpha, sigma, show_process):
    def callback(x): var = lambda y: None
    if show_process:
        callback = mgac_library.visual_callback_2d(image)
    gimg = inverse_gaussian_gradient(image, alpha=alpha, sigma=sigma)
    init_ls = polygon_level_set(polygon_region, gimg.shape[0], gimg.shape[1])
    borders = mgac_library.morphological_geodesic_active_contour(gimg, iterations=iterations,
                                                                 iter_callback=callback,
                                                                 init_level_set=init_ls,
                                                                 smoothing=smoothing, threshold=threshold,
                                                                 balloon=ballon)
    return borders


def get_mgac_image_and_mask(image, borders):
    save_path_borders = configuration_constants.GENERATED_IMAGES_DIR + string_constants.MGAC_BORDER_IMAGE_SAVE_NAME
    save_path_mask = configuration_constants.GENERATED_IMAGES_DIR + string_constants.MGAC_MASK_IMAGE_SAVE_NAME
    generate_image_with_borders(image, borders, save_path_borders)
    generate_image_mask(image, borders, save_path_mask)
    borders_image_array = get_generated_image(save_path_borders)
    mask_image_array = get_generated_image(save_path_mask)
    return borders_image_array, mask_image_array


def get_generated_image(save_path):
    image = Image.open(save_path)
    image_array = np.asarray(image)
    image.close()
    os.remove(save_path)
    return image_array


def generate_image_mask(image, borders, save_path):
    fig = plt.figure(figsize=(7, 7))
    fig.clf()
    ax2 = fig.add_subplot(1, 1, 1)
    ax_u = ax2.imshow(np.zeros_like(image), cmap='binary_r', vmin=0, vmax=1)
    ax_u.set_data(borders)
    fig.canvas.draw()
    plt.axis('off')
    extent = ax2.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
    plt.savefig(save_path, bbox_inches=extent)
    plt.close('all')
    return save_path


def generate_image_with_borders(image, borders, save_path):
    fig = plt.figure(figsize=(7, 7))
    fig.clf()
    ax1 = fig.add_subplot(1, 1, 1)
    ax1.imshow(image, cmap=plt.cm.gray, vmin=0, vmax=255)
    ax1.contour(borders, [0.5], colors='r', linewidths=1)
    fig.canvas.draw()
    plt.axis('off')
    extent = ax1.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
    plt.savefig(save_path, bbox_inches=extent)
    plt.close('all')
    return save_path


def polygon_level_set(polygon_region, width, height):
    x, y = np.meshgrid(np.arange(width), np.arange(height))
    x, y = x.flatten(), y.flatten()
    points = np.vstack((x, y)).T

    p = Path(polygon_region)
    grid = p.contains_points(points)
    mask = grid.reshape(width, height)

    return mask


def inverse_gaussian_gradient(image, alpha=100.0, sigma=5.0):
    gradnorm = ndi.gaussian_gradient_magnitude(image, sigma, mode='nearest')
    return 1.0 / np.sqrt(1.0 + alpha * gradnorm)


def map_borders(cell_image_array, mask_image_array):
    mask_image_array = rgb_to_gray(mask_image_array)
    min_threshold = 5
    mask_image_array = binary_threshold(min_threshold, mask_image_array)

    rows, cols = mask_image_array.shape
    for row in range(rows):
        for col in range(cols):
            if mask_image_array[row][col] == 255 and is_perimeter(mask_image_array, row, col):
                cell_image_array = cv2.circle(cell_image_array, (col, row), radius=2, color=(255, 0, 0), thickness=-1)
    return cell_image_array


def is_perimeter(matrix, current_row, current_col):
    rows, cols = matrix.shape

    for i in range(max(0, current_row - 1), min(current_row + 1, rows)):
        for j in range(max(0, current_col - 1), min(current_col + 1, cols)):
            if matrix[i][j] == 0:
                return True
    return False
