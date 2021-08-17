from src.Backend.Image_processing_algorithms.filters import anisotropic_filter as anisotropic_filter_functions
from src.Constants.algorithm_constants import ANISOTROPIC_FILTER_NAME


class Anisotropic_Filter:

    def __init__(self):
        self.name = ANISOTROPIC_FILTER_NAME

    def apply_method(self, image_array):
        result_array_image = anisotropic_filter_functions.anisotropic_diffusion_filter_medpy(image_array)
        return result_array_image

    def get_method_name(self):
        return self.name

    def get_attributes_dict(self):
        return {}

