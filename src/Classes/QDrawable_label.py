from PyQt5.QtCore import QPoint, QSize, QRect, Qt
from PyQt5.QtGui import QPainter, QPen, QColor, QPixmap, QImage
from PyQt5.QtWidgets import QLabel


class QDrawable_label(QLabel):

    points_list = []
    polygon_finalized = False

    def _init__(self, *args):
        QLabel.__init__(self, *args)

    def set_label_image(self, image_wrapper):
        qimage_size = QSize(image_wrapper.width, image_wrapper.height)
        qimage_starting_point = QPoint(0, 0)
        pixel_map = QPixmap(qimage_size)
        painter = QPainter(pixel_map)
        painter.drawImage(QRect(qimage_starting_point, qimage_size), QImage(image_wrapper.showable_image_path))
        self.setFixedWidth(image_wrapper.width)
        self.setFixedHeight(image_wrapper.height)
        self.setPixmap(pixel_map)
        self.points_list.clear()
        self.polygon_finalized = False
        painter.end()

    def mouseReleaseEvent(self, event):
        if self.polygon_finalized:
            return
        if len(self.points_list) == 0:
            self.draw_point(event)
        else:
            if event.button() == Qt.LeftButton:
                self.draw_line(event)
            else:
                self.finalize_polygon()

    def draw_point(self, event):
        current_image = self.pixmap()
        painter = QPainter(current_image)
        point = QPoint(event.x(), event.y())
        line_pen = QPen(QColor("blue"))
        line_pen.setWidth(3)
        painter.setPen(line_pen)
        painter.drawPoint(point)
        self.points_list.append(point)
        self.setPixmap(current_image)

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
