import numpy as np
from PIL import Image
from medpy.filter.smoothing import anisotropic_diffusion

from src.Backend.Image_processing_algorithms.Operations.common_operations import normalize_to_range


# https://loli.github.io/medpy/generated/medpy.filter.smoothing.anisotropic_diffusion.html
def anisotropic_diffusion_filter_medpy(image, times):
    filtered_image = image
    for i in range(0, times):
        filtered_image = anisotropic_filter(filtered_image)

    return filtered_image


def anisotropic_filter(image):
    pixels = np.uint8(image)
    anisotropic_array = anisotropic_diffusion(pixels)
    filtered_image_array = anisotropic_array_correction(anisotropic_array)
    return filtered_image_array


def anisotropic_array_correction(image_array):
    image = normalize_to_range(image_array)
    image = Image.fromarray(image)
    image = image.convert("I")
    image_corrected_array = np.asarray(image)
    return image_corrected_array
