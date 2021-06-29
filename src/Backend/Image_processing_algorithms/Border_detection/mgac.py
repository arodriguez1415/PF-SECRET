import os

import cv2
import numpy as np
from PIL import Image
from matplotlib import pyplot as plt
from matplotlib.path import Path
from scipy import ndimage as ndi
from src.Backend.Image_processing_algorithms.Border_detection import mgac_library_functions as mgac_library
from src.Backend.Image_processing_algorithms.Operations.common_operations import normalize_to_range
from src.Backend.Image_processing_algorithms.filters import anisotropic_filter as anisotropic_filter_functions
from src.Classes.Region import Region
from src.Constants import configuration_constants
from src.Constants import string_constants


def mgac_borders(polygon_region, image, iterations, threshold, smoothing, ballon, alpha, sigma):
    borders = get_borders(polygon_region, image, iterations, threshold, smoothing, ballon, alpha, sigma)
    borders_image = get_mgac_image(image, borders, mask=False)
    return borders_image


def mgac_mask(polygon_region, image, iterations, threshold, smoothing, ballon, alpha, sigma):
    borders = get_borders(polygon_region, image, iterations, threshold, smoothing, ballon, alpha, sigma)
    mask_borders_image = get_mgac_image(image, borders, mask=True)
    return mask_borders_image


# Esto es una villerada para ver si el metodo pasa, si pasa hay que mejorarlo
def mgac_only_cell(image):
    original_image = image.copy()
    filtered_image = anisotropic_filter_functions.anisotropic_diffusion_filter_medpy(original_image)
    polygon_region = Region()
    polygon_region.get_region()
    iterations = 250
    threshold = 0.35
    smoothing = 0
    ballon = -1
    alpha = 200
    sigma = 2
    mask_image = mgac_mask(polygon_region.points, filtered_image, iterations, threshold, smoothing, ballon, alpha, sigma)
    shape = (mask_image.shape[0], mask_image.shape[1])
    filtered_image = np.array(filtered_image, dtype=np.uint8)
    resized_original_image = cv2.resize(filtered_image, shape, cv2.INTER_NEAREST)
    only_cell_image = map_mask(mask_image, resized_original_image)
    return only_cell_image


def get_borders(polygon_region, image, iterations, threshold, smoothing, ballon, alpha, sigma):
    gimg = inverse_gaussian_gradient(image, alpha=alpha, sigma=sigma)
    # callback = mgac_library.visual_callback_2d(image)
    init_ls = polygon_level_set(polygon_region, gimg.shape[0], gimg.shape[1])
    borders = mgac_library.morphological_geodesic_active_contour(gimg, iterations=iterations,
                                                                 # iter_callback=callback,
                                                                 init_level_set=init_ls,
                                                                 smoothing=smoothing, threshold=threshold,
                                                                 balloon=ballon)
    return borders


def get_mgac_image(image, borders, mask=False):
    save_path = configuration_constants.GENERATED_IMAGES_DIR + string_constants.MGAC_BORDER_IMAGE_SAVE_NAME
    if mask:
        generate_image_mask(image, borders, save_path)
    else:
        generate_image_with_borders(image, borders, save_path)
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


def map_mask(mask_image, resized_original_image):
    rows, cols = mask_image.shape[0], mask_image.shape[1]
    mapped_image = np.zeros((rows, cols))

    for i in range(0, rows):
        for j in range(0, cols):
            if mask_image[i][j][0] == 0:
                mapped_image[i][j] = 0
            else:
                mapped_image[i][j] = resized_original_image[i][j]
    return mapped_image
