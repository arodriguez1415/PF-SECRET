from PyQt5.QtCore import QRect, QSize, QPoint
from PyQt5.QtGui import QPixmap, QPainter, QImage
from src.Classes.Project_image import Project_image
import src.Backend.Menus.archive_menu as archive_menu

def set_style(main_window):
    stylesheets_paths_list = []
    # stylesheets_paths_list.append("./StyleSheets/main_window_stylesheet.css")
    # main_window.centralwidget.setStyleSheet(unified_stylesheet)


def configure_windows(main_window, app):
    set_initial_configuration(main_window)
    configure_main_window_connections(main_window)


def set_initial_configuration(main_window):

    return


def configure_main_window_connections(main_window):
    main_window.load_image_menu_option.triggered.connect(lambda: load_image(main_window))
    return


def load_image(main_window):
    image_path = archive_menu.get_image_path()
    if image_path:
        image_wrapper = Project_image(image_path)
        # archive_menu.load_image_on_memory(image_wrapper)
        load_image_on_screen(image_wrapper, main_window)


def load_image_on_screen(image_wrapper, main_window):
    qimage_size = QSize(image_wrapper.width, image_wrapper.height)
    qimage_starting_point = QPoint(0, 0)
    pixel_map = QPixmap(qimage_size)
    image_viewer = main_window.image_viewer
    painter = QPainter(pixel_map)
    painter.drawImage(QRect(qimage_starting_point, qimage_size), QImage(image_wrapper.showable_image_path))
    image_viewer.setPixmap(pixel_map)
    painter.end()
