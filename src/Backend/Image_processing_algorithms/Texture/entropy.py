from skimage.measure import shannon_entropy
from skimage.util import img_as_ubyte
from skimage.filters.rank import entropy
from skimage.morphology import disk
import numpy as np


def calculate_entropy_piece(image, start_x, start_y, end_x, end_y, width, height):
    float_image = np.float32(image)
    start_x = start_x if start_x >= 0 else 0
    start_y = start_y if start_y >= 0 else 0
    end_x = end_x if end_x < width else width - 1
    end_y = end_y if end_y < height else height - 1
    float_piece = np.zeros((end_y - start_y, end_x - start_x), dtype=float)

    for y in range(start_y, end_y):
        for x in range(start_x, end_x):
            float_piece[y - start_y, x - start_x] = float_image[y, x]

    entropy = shannon_entropy(float_piece)
    return entropy


def calculate_shannon_entropy(image):
    width = image.shape[0]
    height = image.shape[1]
    diff = 7
    entropy_result = np.zeros((image.shape[1], image.shape[0]), dtype=np.float64)

    for y in range(0, height):
        for x in range(0, width):
            entropy_result[y, x] = calculate_entropy_piece(image, x - diff, y - diff, x + diff, y + diff, width, height)

    return entropy_result


def calculate_local_entropy(image):
    image = img_as_ubyte(image)
    entropy_result = entropy(image, disk(5))
    return entropy_result
