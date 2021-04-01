import numpy as np


def normalize(array):
    array2 = array - array.min()
    result = array2 * (255.0 / array2.max())
    return result.astype(np.uint8)


def is_RGB(image_array):
    dimensions = len(image_array.shape)
    if dimensions == 2:
        return False
    else:
        return True
