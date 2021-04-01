from src.Constants import string_constants
from src.Backend.Image_processing_algorithms.filters import anisotropic_filter as anisotropic_filter_functions


class Anisotropic_Filter:

    def __init__(self):
        self.name = string_constants.ANISOTROPIC_METHOD_NAME

    def apply_method(self, image_array):
        result_array_image = anisotropic_filter_functions.anisotropic_diffusion_filter_medpy(image_array)
        return result_array_image
