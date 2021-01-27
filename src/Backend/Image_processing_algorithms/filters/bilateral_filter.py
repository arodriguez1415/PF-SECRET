import cv2 as cv
from PIL import Image
import numpy as np


def bilateral_filter(image, sigma_space, sigma_color, window_size):
    pixels = np.uint8(image)
    bilateral = cv.bilateralFilter(pixels, window_size, sigma_color, sigma_space)
    return bilateral


def save_bilateral_image(image_array, save_path):
    image = Image.fromarray(image_array)
    image = image.convert("L")
    image.save(save_path)
    return
