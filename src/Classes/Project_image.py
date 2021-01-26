import numpy as np
import cv2 as cv
from PIL import Image

from src.Classes.Project_mastermind import Project_mastermind
from src.Classes.Methods.Original import Original

partial_save_path = "./generated/"


class Project_image:
    image_array = None
    showable_image_path = None
    method = None
    width = 0
    height = 0

    def __init__(self, image_path, method=Original()):
        image = Project_image.read_image(image_path)
        image_width = Project_image.get_image_width(image)
        image_height = Project_image.get_image_height(image)
        normalized_image_array = Project_image.normalized_image_data(image)
        showable_image_path = image_path
        if method.name == "Original":  # Cambiar por cte
            showable_image_path = Project_mastermind.get_instance().create_stage_path_name(method.name)
            Project_image.save_showable_image(normalized_image_array, showable_image_path)
        self.set_image_array(normalized_image_array)
        self.set_showable_image_path(showable_image_path)
        self.set_size(image_width, image_height)
        self.set_method(method)

    def set_image_array(self, image_array):
        self.image_array = image_array

    def set_showable_image_path(self, showable_image_path):
        self.showable_image_path = showable_image_path

    def set_size(self, width, height):
        self.width = width
        self.height = height

    def set_method(self, method):
        self.method = method

    def print_information(self):
        print("Path: " + self.showable_image_path)
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
