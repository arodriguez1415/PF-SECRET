from PyQt5 import QtCore
import src.Frontend.Menus.archive_menu as archive_menu
import src.Frontend.Menus.filter_menu as filter_menu
import src.Frontend.Menus.border_detection_menu as border_detection_menu
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
    main_window.stacked_feature_windows.setCurrentIndex(0)
    return


def configure_main_window_connections(main_window):
    archive_menu.configure_archive_menu_connections(main_window)
    filter_menu.configure_filter_menu_connections(main_window)
    border_detection_menu.configure_border_detection_menu_connections(main_window)


def replace_image_viewer(image_viewer):
    drawable_image_viewer = QDrawable_label(image_viewer.parent())
    drawable_image_viewer.setGeometry(image_viewer.geometry())
    drawable_image_viewer.setAlignment(QtCore.Qt.AlignCenter)
    drawable_image_viewer.setObjectName("image_viewer")
    return drawable_image_viewer


