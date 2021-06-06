import cv2 as cv
import numpy as np
from PIL import Image
from src.Backend.Image_processing_algorithms.Operations import common_operations
from src.Backend.Image_processing_algorithms.Texture.profile_texture import fractal_dimension_static_wrapper


def texture_heatmap(image):
    width = image.shape[0]
    height = image.shape[1]
    combinated_results = np.zeros((image.shape[1], image.shape[0]), dtype=np.float64)

    for y in range(0, height):
        for x in range(0, width):
            entropy, fractal_dimension = \
                fractal_dimension_static_wrapper(image, x - 7, y - 7, x + 7, y + 7, width, height)
            combinated_results[y, x] = entropy * 0.5 + 0.5 * fractal_dimension

    show_and_generate_heat_map(combinated_results)

def show_and_generate_heat_map(img):
    img = Image.fromarray(img)
    img = common_operations.normalize_from_pil_image(img)
    color_np = cv.applyColorMap(img, cv.COLORMAP_HOT)
    color_image = Image.fromarray(color_np)
    color_image.show()
