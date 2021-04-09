from src.Constants import string_constants
from src.Backend.Image_processing_algorithms.Border_detection import mgac as mgac_functions


class Mgac:

    def __init__(self, region_point, iterations, threshold, smoothing, balloon, alpha, sigma, mask_flag=False):
        self.name = string_constants.MGAC_METHOD_NAME
        self.iterations = iterations
        self.threshold = threshold
        self.smoothing = smoothing
        self.balloon = balloon
        self.alpha = alpha
        self.sigma = sigma
        self.region_point = region_point
        self.mask_flag = mask_flag

    def apply_method(self, image_array):
        if self.mask_flag:
            result_array_image = mgac_functions.mgac_mask(self.region_point, image_array, self.iterations,
                                                          self.threshold, self.smoothing, self.balloon, self.alpha,
                                                          self.sigma)
        else:
            result_array_image = mgac_functions.mgac_borders(self.region_point, image_array, self.iterations,
                                                             self.threshold, self.smoothing, self.balloon, self.alpha,
                                                             self.sigma)
        return result_array_image

    def set_mask_flag(self, mask_flag):
        self.mask_flag = mask_flag
