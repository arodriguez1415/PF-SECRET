from src.Classes.Methods.Original import Original


class Image_wrapper:
    image_array = None
    method = None
    width = 0
    height = 0

    def __init__(self, image_array, method=Original()):
        self.image_array = image_array
        self.method = method
        self.width = image_array.shape[1]
        self.height = image_array.shape[0]

    def get_method(self):
        return self.method