from src.Backend.Image_processing_algorithms.Preprocessing import adaptive_threshold


class Adaptive_threshold:

    def __init__(self, window_size, c_constant, method_type):
        self.name = "Adaptive threshold"
        self.window_size = window_size
        self.c_constant = c_constant
        self.method_type = method_type

    def apply_method(self, image_array):
        result_array_image = adaptive_threshold.adaptive_threshold(image_array, self.window_size,
                                                                   self.c_constant, self.method_type)
        return result_array_image
