from medpy.filter.smoothing import anisotropic_diffusion
from PIL import Image
import numpy as np
from src.Constants import configuration_constants
from src.Constants import string_constants


# https://loli.github.io/medpy/generated/medpy.filter.smoothing.anisotropic_diffusion.html
def anisotropic_diffusion_filter_medpy(image):
    pixels = np.uint8(image)
    anisotropic_array = anisotropic_diffusion(pixels)
    filtered_image_array = anisotropic_array_correction(anisotropic_array)
    return filtered_image_array


def anisotropic_array_correction(image_array):
    image = Image.fromarray(image_array)
    image = image.convert("I")
    image_corrected_array = np.asarray(image)
    return image_corrected_array
