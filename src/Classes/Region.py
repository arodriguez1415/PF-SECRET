import sys

import numpy
import src.Frontend.Utils.message as messages
from src.Classes.Project_mastermind import Project_mastermind


class Region:
    drawable_label = None
    image_array_in_region = None
    points = []

    def __init__(self):
        self.set_drawable_label()
        self.points.clear()
        self.points = self.get_region()

    def set_drawable_label(self):
        project_mastermind = Project_mastermind.get_instance()
        drawable_label = project_mastermind.main_window.image_viewer
        self.image_array_in_region = project_mastermind.get_last_image()
        self.drawable_label = drawable_label

    def get_region(self):
        region_qpoints = self.drawable_label.get_polygon()
        if len(region_qpoints) == 0:
            return self.get_all_image_region()
        for qpoint in region_qpoints:
            x_axis = qpoint.x()
            y_axis = qpoint.y()
            point = (x_axis, y_axis)
            self.points.append(point)
        return self.points

    def get_pixels_in_region(self, inform=True):
        if len(self.points) != 4:
            raise Exception("Region must be square")
        top_left_point = self.points[0]
        bottom_right_point = self.points[3]
        numpy.set_printoptions(threshold=sys.maxsize)
        pixels_in_region = self.image_array_in_region[top_left_point[1]:bottom_right_point[1],
                                                      top_left_point[0]:bottom_right_point[0]]
        if inform:
            message = "La cantidad de pixeles en la region es: " + str(len(pixels_in_region))
            messages.show_message(message)
        return pixels_in_region

    def get_avg_in_region(self):
        dimensions = len(self.image_array_in_region.shape)
        pixels_in_region = self.get_pixels_in_region(inform=False)
        if dimensions == 2:
            pixels_quantity = pixels_in_region.size
            avg = numpy.sum(pixels_in_region) / pixels_quantity
        else:
            pixels_quantity = pixels_in_region[:, :, 0].size
            red = numpy.sum(pixels_in_region[:, :, 0]) / pixels_quantity
            green = numpy.sum(pixels_in_region[:, :, 1]) / pixels_quantity
            blue = numpy.sum(pixels_in_region[:, :, 2]) / pixels_quantity
            avg = (red, green, blue)
        message = "El promedio vale: " + str(avg)
        messages.show_message(message)
        return avg

    def get_all_image_region(self):
        image_process_wrapper = Project_mastermind.get_instance().get_last_image_process()
        height = image_process_wrapper.height
        width = image_process_wrapper.width
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
