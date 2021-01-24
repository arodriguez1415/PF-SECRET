from PyQt5 import QtCore
from src.Classes.Project_image import Project_image
import src.Backend.Menus.archive_menu as archive_menu
from src.Classes.QDrawable_label import QDrawable_label


def set_style(main_window):
    stylesheets_paths_list = []
    # stylesheets_paths_list.append("./StyleSheets/main_window_stylesheet.css")
    # main_window.centralwidget.setStyleSheet(unified_stylesheet)


def configure_windows(main_window, app):
    set_initial_configuration(main_window)
    configure_main_window_connections(main_window)


def set_initial_configuration(main_window):
    main_window.image_viewer = replace_image_viewer(main_window.image_viewer)
    return


def configure_main_window_connections(main_window):
    image_viewer = main_window.image_viewer
    main_window.load_image_menu_option.triggered.connect(lambda: load_image(image_viewer))


def replace_image_viewer(image_viewer):
    drawable_image_viewer = QDrawable_label(image_viewer.parent())
    drawable_image_viewer.setGeometry(image_viewer.geometry())
    drawable_image_viewer.setAlignment(QtCore.Qt.AlignCenter)
    drawable_image_viewer.setObjectName("image_viewer")
    return drawable_image_viewer


def load_image(main_window):
    image_path = archive_menu.get_image_path()
    if image_path:
        image_wrapper = Project_image(image_path)
        # archive_menu.load_image_on_memory(image_wrapper)
        load_image_on_screen(image_wrapper, main_window)


def load_image_on_screen(image_wrapper, image_viewer):
    image_viewer.set_label_image(image_wrapper)
