import numpy as np

from src.Classes.Project_mastermind import Project_mastermind
from src.Constants import configuration_constants


class Region:
    drawable_label = None
    points = []

    def __init__(self):
        self.set_drawable_label()
        self.points.clear()
        self.points = []

    def set_drawable_label(self):
        project_mastermind = Project_mastermind.get_instance()
        drawable_label = project_mastermind.main_window.image_viewer
        self.drawable_label = drawable_label

    def has_region(self):
        region_qpoints = self.drawable_label.get_polygon()
        if len(region_qpoints) < 2:
            return False
        return True

    def get_line(self):
        region_qpoints = self.drawable_label.get_polygon()
        print("ASD")
        if len(region_qpoints) != 2:
            raise ValueError('Need at least two points')
        for qpoint in region_qpoints:
            x_axis = qpoint.x()
            y_axis = qpoint.y()
            point = (x_axis, y_axis)
            self.points.append(point)
        return self.points

    def get_region(self):
        region_qpoints = self.drawable_label.get_polygon()
        if len(region_qpoints) < 3:
            return self.get_all_image_region()
        for qpoint in region_qpoints:
            x_axis = qpoint.x()
            y_axis = qpoint.y()
            point = (x_axis, y_axis)
            self.points.append(point)
        return self.points

    def get_all_image_region(self):
        self.points = []
        width, height = configuration_constants.IMAGE_VIEWER_WIDTH, configuration_constants.IMAGE_VIEWER_HEIGHT
        top_left_point = (0, 0)
        bottom_left_point = (0, height - 1)
        bottom_right_point = (width - 1, height - 1)
        top_right_point = (width - 1, 0)
        self.points.append(top_left_point)
        self.points.append(bottom_left_point)
        self.points.append(bottom_right_point)
        self.points.append(top_right_point)
        self.points.append(top_left_point)
        return self.points


    def get_pixels_in_region(self, image_array):
        min_x = min(self.points)[0]
        max_x = max(self.points)[0]
        min_y = min(self.points, key=lambda t: t[1])[1]
        max_y = max(self.points, key=lambda t: t[1])[1]

        pixels_in_region = image_array[min_y:max_y, min_x:max_x]
        return pixels_in_region


    @staticmethod
    def get_all_image_as_region(image_array):
        width, height = image_array.shape
        points = []
        top_left_point = (0, 0)
        bottom_left_point = (0, height - 1)
        bottom_right_point = (width - 1, height - 1)
        top_right_point = (width - 1, 0)
        points.append(top_left_point)
        points.append(bottom_left_point)
        points.append(bottom_right_point)
        points.append(top_right_point)
        points.append(top_left_point)
        return points


