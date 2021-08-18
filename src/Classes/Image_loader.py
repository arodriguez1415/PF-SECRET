import numpy as np
import cv2 as cv
from PIL import Image

from src.Classes.Methods.Original import Original


class Image_loader:
    image_array = None
    method = None
    width = 0
    height = 0

    def __init__(self, image_path, method=Original()):
        self.generate_normal_image(image_path, method)

    def generate_normal_image(self, image_path, method, image=None):
        if image is None:
            image = Image_loader.read_image(image_path)
        image_width = Image_loader.get_image_width(image)
        image_height = Image_loader.get_image_height(image)
        normalized_image_array = Image_loader.normalized_image_data(image)
        self.set_image_array(normalized_image_array)
        self.set_size(image_width, image_height)
        self.set_method(method)

    def set_image_array(self, image_array):
        self.image_array = image_array

    def set_size(self, width, height):
        self.width = width
        self.height = height

    def set_method(self, method):
        self.method = method

    def print_information(self):
        if self.method is not None:
            print("Method: " + self.method.name)
        print("Width: " + str(self.width))
        print("Height: " + str(self.height))

    @staticmethod
    def read_image(image_path):
        image = Image.open(image_path)
        return image

    @staticmethod
    def get_image_width(image):
        image_width = image.width
        return image_width

    @staticmethod
    def get_image_height(image):
        image_height = image.height
        return image_height

    @staticmethod
    def normalized_image_data(image):
        image_data = np.array(image)
        image_width = image.width
        image_height = image.height
        dst = np.zeros((image_height, image_width))
        dst = cv.normalize(image_data, dst, 0, 255, cv.NORM_MINMAX, cv.CV_8UC1)
        return dst

    @staticmethod
    def save_showable_image(image_array, image_path):
        image = Image.fromarray(image_array)
        image.save(image_path)
        return image_path
