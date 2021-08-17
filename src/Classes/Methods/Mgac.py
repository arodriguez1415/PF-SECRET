from src.Backend.Image_processing_algorithms.Border_detection import mgac as mgac_functions
from src.Constants.algorithm_constants import MGAC_ITERATIONS, MGAC_THRESHOLD, MGAC_SMOOTHING, \
    MGAC_BALLOON, MGAC_ALPHA, MGAC_SIGMA, MGAC_NAME


class Mgac:

    def __init__(self, region_point, iterations, threshold, smoothing, balloon, alpha, sigma, mask_flag=False):
        self.name = MGAC_NAME
        self.iterations = iterations
        self.threshold = threshold
        self.smoothing = smoothing
        self.balloon = balloon
        self.alpha = alpha
        self.sigma = sigma
        self.region_point = region_point
        self.mask_flag = mask_flag

    def apply_method(self, image_array):
        borders_image, mask_image = mgac_functions.mgac(self.region_point, image_array, self.iterations,
                                                        self.threshold, self.smoothing, self.balloon, self.alpha,
                                                        self.sigma)
        if self.mask_flag:
            return mask_image
        return borders_image

    def set_mask_flag(self, mask_flag):
        self.mask_flag = mask_flag

    def get_method_name(self):
        return self.name

    def get_attributes_dict(self):
        mgac_attributes_dict = {MGAC_ITERATIONS: self.iterations, MGAC_THRESHOLD: self.threshold,
                                MGAC_SMOOTHING: self.smoothing, MGAC_BALLOON: self.balloon, MGAC_ALPHA: self.alpha,
                                MGAC_SIGMA: self.sigma}
        return mgac_attributes_dict
