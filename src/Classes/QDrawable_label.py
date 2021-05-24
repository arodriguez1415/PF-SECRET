import qimage2ndarray as qimage2ndarray
from PyQt5.QtCore import QPoint, QSize, QRect, Qt
from PyQt5.QtGui import QPainter, QPen, QColor, QPixmap
from PyQt5.QtWidgets import QLabel
import math

class QDrawable_label(QLabel):

    points_list = []
    paint_flag = False
    square_flag = False
    fixed_square_flag = False
    polygon_finalized = False
    actual_image_wrapper = None

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

    def set_screen_image(self, image_wrapper):
        if image_wrapper is None:
            return
        self.points_list.clear()
        self.polygon_finalized = False
        self.actual_image_wrapper = image_wrapper
        qimage_size = QSize(image_wrapper.width, image_wrapper.height)
        qimage_starting_point = QPoint(0, 0)
        pixel_map = QPixmap(qimage_size)
        painter = QPainter(pixel_map)
        image = qimage2ndarray.array2qimage(image_wrapper.image_array)
        painter.drawImage(QRect(qimage_starting_point, qimage_size), image)
        self.setFixedWidth(image_wrapper.width)
        self.setFixedHeight(image_wrapper.height)
        self.setPixmap(pixel_map)
        painter.end()

    def mouseReleaseEvent(self, event):
        if self.polygon_finalized or not self.paint_flag:
            return
        if len(self.points_list) == 0 and not self.fixed_square_flag:
            self.draw_point(event)
        elif self.square_flag:
            self.finalize_square(event)
        elif self.fixed_square_flag:
            self.finalize_fixed_square(event)
        else:
            if event.button() == Qt.LeftButton:
                self.draw_line(event)
            else:
                self.finalize_polygon()

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

    def draw_line(self, event):
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
        self.points_list.append(top_right_point)
        self.points_list.append(bottom_left_point)
        self.points_list.append(bottom_right_point)
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
        self.points_list.append(top_left_point)
        self.points_list.append(top_right_point)
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
        self.set_screen_image(self.actual_image_wrapper)

