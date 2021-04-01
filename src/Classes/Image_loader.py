import os

import numpy as np
import cv2 as cv
from PIL import Image
from src.Classes.Methods.Original import Original
from src.Frontend.Menus import archive_menu


class Image_loader:
    image_array = None
    method = None
    width = 0
    height = 0

    def __init__(self, image_path, method=Original()):
        image_name, image_extension = os.path.splitext(image_path)
        if image_extension == ".RAW":
            self.generate_raw_image(image_path, method)
        else:
            self.generate_normal_image(image_path, method)

    def generate_raw_image(self, image_path, method):
        width, height = self.get_shape_of_raw(image_path)
        if width is None or height is None:
            raise Exception("Bad shape")
        file = open(image_path, 'rb')
        rawData = file.read()
        file.close()
        imgSize = (width, height)
        image = Image.frombytes('L', imgSize, rawData, 'raw')
        self.generate_normal_image(image_path=image_path, method=method, image=image)

    def get_shape_of_raw(self, image_path):
        information_path = archive_menu.get_information_path()
        width = None
        height = None
        f = open(information_path, "r")
        lines = f.readlines()
        for line in lines:
            line = ' '.join(line.split())
            line_array = line.split(' ')
            if line_array[0] in image_path and len(line_array) == 3:
                width = int(line_array[1])
                height = int(line_array[2])
                break
        f.close()
        return width, height

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
