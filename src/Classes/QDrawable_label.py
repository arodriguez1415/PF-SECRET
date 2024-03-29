import math

import cv2
import qimage2ndarray as qimage2ndarray
from PyQt5.QtCore import QPoint, QSize, QRect, Qt
from PyQt5.QtGui import QPainter, QPen, QColor, QPixmap
from PyQt5.QtWidgets import QLabel

from src.Backend.Image_processing_algorithms.Operations.common_operations import resize_image, gray_to_rgb
from src.Classes.Project_mastermind import Project_mastermind
from src.Constants import configuration_constants
from src.Constants.algorithm_constants import HORIZONTAL_LINE_TYPE
from src.Frontend.Utils.button_controller import deselect_all


class QDrawable_label(QLabel):
    points_list = []
    paint_flag = False
    square_flag = False
    fixed_square_flag = False
    diagonal_line_flag = False
    polygon_finalized = False
    actual_image_wrapper = None
    fixed_line_type = None

    def _init__(self, *args):
        QLabel.__init__(self, *args)

    def clear_paint_flag(self):
        self.paint_flag = False

    def set_paint_flag(self):
        self.paint_flag = True

    def set_square_flag(self):
        self.square_flag = True

    def set_fixed_square_flag(self):
        self.fixed_square_flag = True

    def set_diagonal_line_flag(self):
        self.diagonal_line_flag = True

    def set_fixed_line_type(self, line_type):
        self.fixed_line_type = line_type

    def reset_line_flag(self):
        self.diagonal_line_flag = False
        self.fixed_line_type = None

    def set_screen_image(self, image_wrapper):
        if image_wrapper is None:
            return
        self.points_list.clear()
        self.polygon_finalized = False
        self.actual_image_wrapper = image_wrapper
        width = configuration_constants.IMAGE_VIEWER_WIDTH
        height = configuration_constants.IMAGE_VIEWER_HEIGHT
        image_array = image_wrapper.image_array
        image_resized = resize_image(image_array, width, height)
        qimage_size = QSize(width, height)
        qimage_starting_point = QPoint(0, 0)
        pixel_map = QPixmap(qimage_size)
        painter = QPainter(pixel_map)
        image = qimage2ndarray.array2qimage(image_resized)
        painter.drawImage(QRect(qimage_starting_point, qimage_size), image)
        self.setFixedWidth(width)
        self.setFixedHeight(height)
        self.setPixmap(pixel_map)
        painter.end()

    def mouseReleaseEvent(self, event):
        project_mastermind = Project_mastermind.get_instance()
        main_window = project_mastermind.main_window
        if self.polygon_finalized or not self.paint_flag:
            return
        if len(self.points_list) == 0 and not self.fixed_square_flag:
            if self.fixed_line_type is None:
                self.draw_point(event)
            else:
                self.draw_fixed_line(event, self.fixed_line_type)
                deselect_all(main_window)
        elif self.square_flag:
            self.finalize_square(event)
            deselect_all(main_window)
        elif self.fixed_square_flag:
            self.finalize_fixed_square(event)
            deselect_all(main_window)
        elif self.diagonal_line_flag:
            self.draw_diagonal_line(event)
            deselect_all(main_window)
        else:
            if event.button() == Qt.LeftButton:
                self.draw_diagonal_line(event)
            else:
                self.finalize_polygon()
                deselect_all(main_window)

    def draw_point(self, event):
        if not self.paint_flag or self.actual_image_wrapper is None:
            return
        current_image = self.pixmap()
        painter = QPainter(current_image)
        point = QPoint(event.x(), event.y())
        line_pen = QPen(QColor("blue"))
        line_pen.setWidth(3)
        painter.setPen(line_pen)
        painter.drawPoint(point)
        self.points_list.append(point)
        self.setPixmap(current_image)
        painter.end()

    def draw_fixed_line(self, event, line_type):
        current_image = self.pixmap()
        painter = QPainter(current_image)

        if line_type == HORIZONTAL_LINE_TYPE:
            from_point = QPoint(0, event.y())
            to_point = QPoint(current_image.width(), event.y())
        else:
            from_point = QPoint(event.x(), 0)
            to_point = QPoint(event.x(), current_image.height())

        line_pen = QPen(QColor("blue"))
        line_pen.setWidth(3)
        painter.setPen(line_pen)
        painter.drawLine(from_point, to_point)
        self.points_list.append(from_point)
        self.points_list.append(to_point)
        self.setPixmap(current_image)
        if self.fixed_line_type:
            self.paint_flag = False
            self.fixed_line_type = None
        painter.end()

    def draw_diagonal_line(self, event):
        current_image = self.pixmap()
        painter = QPainter(current_image)
        to_point = QPoint(event.x(), event.y())
        from_point = self.points_list[-1]
        line_pen = QPen(QColor("blue"))
        line_pen.setWidth(3)
        painter.setPen(line_pen)
        painter.drawLine(from_point, to_point)
        self.points_list.append(to_point)
        self.setPixmap(current_image)
        if self.diagonal_line_flag:
            self.paint_flag = False
            self.diagonal_line_flag = False
        painter.end()

    def finalize_polygon(self):
        current_image = self.pixmap()
        painter = QPainter(current_image)
        to_point = self.points_list[0]
        from_point = self.points_list[-1]
        line_pen = QPen(QColor("blue"))
        line_pen.setWidth(3)
        painter.setPen(line_pen)
        painter.drawLine(from_point, to_point)
        self.points_list.append(to_point)
        self.polygon_finalized = True
        self.setPixmap(current_image)
        self.paint_flag = False
        painter.end()

    def finalize_square(self, event):
        line_pen = QPen(QColor("blue"))
        line_pen.setWidth(3)
        current_image = self.pixmap()
        painter = QPainter(current_image)
        painter.setPen(line_pen)
        bottom_left_point = QPoint(self.points_list[0].x(), event.y())
        bottom_right_point = QPoint(event.x(), event.y())
        top_right_point = QPoint(event.x(), self.points_list[0].y())
        painter.drawLine(self.points_list[0], bottom_left_point)
        painter.drawLine(self.points_list[0], top_right_point)
        painter.drawLine(bottom_left_point, bottom_right_point)
        painter.drawLine(top_right_point, bottom_right_point)
        self.points_list.append(bottom_left_point)
        self.points_list.append(bottom_right_point)
        self.points_list.append(top_right_point)
        self.setPixmap(current_image)
        self.paint_flag = False
        self.square_flag = False
        painter.end()

    def finalize_fixed_square(self, event):
        line_pen = QPen(QColor("blue"))
        line_pen.setWidth(3)
        current_image = self.pixmap()
        painter = QPainter(current_image)
        painter.setPen(line_pen)
        x_fixed_size = math.ceil(current_image.width() * 0.05)
        y_fixed_size = math.ceil(current_image.height() * 0.05)
        bottom_left_point = QPoint(event.x() - x_fixed_size/2, event.y() - y_fixed_size/2)
        bottom_right_point = QPoint(event.x() + x_fixed_size/2, event.y() - y_fixed_size/2)
        top_right_point = QPoint(event.x() + x_fixed_size/2, event.y() + y_fixed_size/2)
        top_left_point = QPoint(event.x() - x_fixed_size / 2, event.y() + y_fixed_size / 2)
        painter.drawLine(top_left_point, top_right_point)
        painter.drawLine(top_right_point, bottom_right_point)
        painter.drawLine(bottom_right_point, bottom_left_point)
        painter.drawLine(bottom_left_point, top_left_point)
        self.points_list = []
        self.points_list.append(top_right_point)
        self.points_list.append(top_left_point)
        self.points_list.append(bottom_left_point)
        self.points_list.append(bottom_right_point)

        self.setPixmap(current_image)
        self.paint_flag = False
        self.fixed_square_flag = False
        painter.end()

    def get_polygon(self):
        return self.points_list

    def clear_region(self):
        self.points_list = []
        self.polygon_finalized = False
        self.paint_flag = False
        self.square_flag = False
        self.fixed_square_flag = False
        self.diagonal_line_flag = False
        self.fixed_line_type = None
        self.set_screen_image(self.actual_image_wrapper)


    @staticmethod
    def draw_region_in_image(image_array, points):
        line_thickness = 3
        from_points = points.copy()
        to_points = points.copy()

        to_points.append(from_points[0])
        to_points.pop(0)

        image_array = gray_to_rgb(image_array)

        for i in range(0, len(points)):
            image_array = cv2.line(image_array, from_points[i], to_points[i], (0, 0, 255), thickness=line_thickness)

        return image_array

