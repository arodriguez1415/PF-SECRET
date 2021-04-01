import src.Constants.algorithm_constants as algorithm_constants
from skimage import feature
import src.Backend.Image_processing_algorithms.Operations.common_operations as common_operations


def local_binary_pattern(image_array, symmetric_points=1, radius=1,
                         method=algorithm_constants.LBP_DEFAULT):
    lbp = feature.local_binary_pattern(image_array, symmetric_points,
                                       radius, method=method)
    lbp_normalized = common_operations.normalize(lbp)
    return lbp_normalized


def get_method(method_value):
    switcher = {
        "default": algorithm_constants.LBP_DEFAULT,
        "uniforme": algorithm_constants.LBP_UNIFORM,
        "ror": algorithm_constants.LBP_ROR,
        "nri_uniforme": algorithm_constants.LBP_NRI_UNIFORM,
    }
    return switcher.get(method_value.lower(), "nothing")
