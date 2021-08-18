from src.Backend.Image_processing_algorithms.filters import anisotropic_filter as anisotropic_filter_functions
from src.Constants.algorithm_constants import ANISOTROPIC_FILTER_NAME, ANISOTROPIC_TIMES


class Anisotropic_Filter:

    def __init__(self, iterations):
        self.name = ANISOTROPIC_FILTER_NAME
        self.iterations = iterations

    def apply_method(self, image_array):
        result_array_image = anisotropic_filter_functions.anisotropic_diffusion_filter_medpy(image_array,
                                                                                             self.iterations)
        return result_array_image

    def get_method_name(self):
        return self.name

    def get_attributes_dict(self):
        return {ANISOTROPIC_TIMES: self.iterations}

