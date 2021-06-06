import cv2 as cv
import numpy as np
from PIL import Image
from src.Backend.Image_processing_algorithms.Operations import common_operations
import skimage.measure


def texture_calculation(image, start_x, start_y, end_x, end_y, width, height):
    float_image = np.float32(image)
    start_x = start_x if start_x >= 0 else 0
    start_y = start_y if start_y >= 0 else 0
    end_x = end_x if end_x < width else width - 1
    end_y = end_y if end_y < height else height - 1
    float_piece = np.zeros((end_y - start_y, end_x - start_x), dtype=float)

    for y in range(start_y, end_y):
        for x in range(start_x, end_x):
            float_piece[y - start_y, x - start_x] = float_image[y, x]

    entropy = skimage.measure.shannon_entropy(float_piece)
    return entropy


def texture_heatmap(image):
    width = image.shape[0]
    height = image.shape[1]
    combined_results = np.zeros((image.shape[1], image.shape[0]), dtype=np.float64)

    for y in range(0, height):
        for x in range(0, width):
            entropy = texture_calculation(image, x - 7, y - 7, x + 7, y + 7, width, height)
            combined_results[y, x] = entropy

    # for y in range(0, height):
    #     for x in range(0, width):
    #         if combined_results[y, x] < 4.0:
    #             combined_results[y, x] = 0
    #
    # min_value = 10.0
    # for y in range(0, height):
    #     for x in range(0, width):
    #         if combined_results[y, x] != 0 and combined_results[y, x] < min_value:
    #             min_value = combined_results[y, x]

    min_value = 4.0 # TODO SACAR
    show_and_generate_heat_map(combined_results, min_value)


def show_and_generate_heat_map(img, min_value):
    img = common_operations.normalize_with_min(img, min_value)
    color_np = cv.applyColorMap(img, cv.COLORMAP_HOT)
    color_np = common_operations.bgr_to_rgb(color_np)
    color_image = Image.fromarray(color_np)
    color_image.show()
