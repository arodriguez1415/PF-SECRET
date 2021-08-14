from src.Backend.Image_processing_algorithms.Preprocessing import adaptive_threshold
from src.Constants.algorithm_constants import ADAPTIVE_THRESHOLD_WINDOW_SIZE, ADAPTIVE_THRESHOLD_C_CONSTANT, \
    ADAPTIVE_THRESHOLD_METHOD, ADAPTIVE_THRESHOLD_NAME, ADAPTIVE_THRESHOLD_MEAN_NAME, ADAPTIVE_THRESHOLD_GAUSSIAN_NAME


class Adaptive_threshold:

    def __init__(self, window_size, c_constant, method_type):
        self.name = ADAPTIVE_THRESHOLD_NAME
        self.window_size = window_size
        self.c_constant = c_constant
        self.method_type = method_type

    def apply_method(self, image_array):
        result_array_image = adaptive_threshold.adaptive_threshold(image_array, self.window_size,
                                                                   self.c_constant, self.method_type)
        return result_array_image

    def get_method_name(self):
        return self.name

    def get_attributes_dict(self):
        adaptive_threshold_attributes_dict = {ADAPTIVE_THRESHOLD_WINDOW_SIZE: self.window_size,
                                              ADAPTIVE_THRESHOLD_C_CONSTANT: self.c_constant,
                                              ADAPTIVE_THRESHOLD_METHOD: self.get_method_type_name()}

        return adaptive_threshold_attributes_dict

    def get_method_type_name(self):
        return {
            0: ADAPTIVE_THRESHOLD_MEAN_NAME,
            1: ADAPTIVE_THRESHOLD_GAUSSIAN_NAME,
        }[self.method_type]
