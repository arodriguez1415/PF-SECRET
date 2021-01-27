from medpy.filter.smoothing import anisotropic_diffusion
from PIL import Image
import numpy as np

# https://loli.github.io/medpy/generated/medpy.filter.smoothing.anisotropic_diffusion.html
def anisotropic_diffusion_filter_medpy(image):
    pixels = np.uint8(image)
    anisotropic = anisotropic_diffusion(pixels)
    return anisotropic


def save_anisotropic_image(image_array, save_path):
    image = Image.fromarray(image_array)
    image = image.convert("L")
    image.save(save_path)
    return
