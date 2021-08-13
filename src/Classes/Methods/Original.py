from src.Constants.algorithm_constants import ORIGINAL_NAME

class Original:

    def __init__(self):
        self.name = ORIGINAL_NAME

    def apply_method(self, image_array):
        return image_array

    def get_method_name(self):
        return self.name

    def get_attributes_dict(self):
        return {}
