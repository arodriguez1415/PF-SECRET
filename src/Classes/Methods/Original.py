from src.Constants import string_constants


class Original:

    def __init__(self):
        self.name = string_constants.ORIGINAL_METHOD_NAME

    def apply_method(self, image_array):
        return image_array
