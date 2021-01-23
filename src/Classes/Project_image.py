import numpy as np
import cv2 as cv
from PIL import Image
import src.Constants.configuration_constants as constants


class Project_image:
    raw_image_path = None
    image_array = None
    showable_image_path = None
    method = None
    width = 0
    height = 0

    def __init__(self, raw_image_path):
        image = Project_image.read_image(raw_image_path)
        image_width = Project_image.get_image_width(image)
        image_height = Project_image.get_image_height(image)
        normalized_image_data = Project_image.normalized_image_data(image)
        image_array = Project_image.convert_in_image_array(normalized_image_data)
        showable_image_path = Project_image.save_showable_image(image_array)

        self.set_raw_image_path(raw_image_path)
        self.set_image_array(image_array)
        self.set_showable_image_path(showable_image_path)
        self.set_size(image_width, image_height)

    def set_raw_image_path(self, raw_image_path):
        self.raw_image_path = raw_image_path

    def set_image_array(self, image_array):
        self.image_array = image_array

    def set_showable_image_path(self, showable_image_path):
        self.showable_image_path = showable_image_path

    def set_size(self, width, height):
        self.width = width
        self.height = height

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
    def convert_in_image_array(image_data):
        image_array = Image.fromarray(image_data)
        return image_array

    @staticmethod
    def save_showable_image(image_array):
        image_path = constants.TEMPORARY_DIRECTORY + "original.tif"
        image_array.save(image_path)
        return image_path
