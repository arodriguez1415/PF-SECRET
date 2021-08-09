import os

from PyQt5 import QtCore

from src.Classes.QDrawable_label import QDrawable_label
import src.Frontend.Menus.archive_menu as archive_menu
import src.Frontend.Menus.texture_menu as texture_menu
import src.Frontend.Menus.filter_menu as filter_menu
import src.Frontend.toolBox as toolBox
import src.Frontend.Menus.preprocessing_menu as preprocessing_menu
import src.Frontend.Menus.border_detection_menu as border_detection_menu
import src.Frontend.Menus.movement_menu as movement_menu
import src.Frontend.Menus.metrics_menu as metrics_menu
import src.Frontend.Menus.video_menu as video_menu
import src.Frontend.Menus.routines_menu as routines_menu
from src.Frontend.Utils import viewer_buttons, information_buttons
from src.Frontend.Utils.viewer_buttons import disable_extra_views, disable_main_view


def set_style(main_window):
    stylesheet_rel_path = "./Resources/Stylesheets/main_window_stylesheet.css"
    abs_file = os.path.abspath(stylesheet_rel_path)
    file = open(abs_file, 'r')
    stylesheet_content = file.read()
    file.close()
    main_window.centralwidget.setStyleSheet(stylesheet_content)


def configure_windows(main_window, app):
    set_initial_configuration(main_window)
    set_style(main_window)
    configure_main_window_connections(main_window)


def set_initial_configuration(main_window):
    main_window.image_viewer = replace_image_viewer(main_window.image_viewer)
    main_window.stacked_feature_windows.setCurrentIndex(0)
    disable_main_view(main_window)
    disable_extra_views(main_window)
    toolBox.disable_toolbox(main_window)
    return


def configure_main_window_connections(main_window):
    viewer_buttons.configure_viewer_buttons_connections(main_window)
    information_buttons.configure_information_buttons(main_window)
    archive_menu.configure_archive_menu_connections(main_window)
    texture_menu.configure_texture_menu_connections(main_window)
    filter_menu.configure_filter_menu_connections(main_window)
    border_detection_menu.configure_border_detection_menu_connections(main_window)
    movement_menu.configure_movement_menu_connections(main_window)
    metrics_menu.configure_metrics_menu_connections(main_window)
    video_menu.configure_video_menu_connections(main_window)
    toolBox.configure_toolBox_connections(main_window)
    preprocessing_menu.configure_preprocessing_menu_connections(main_window)
    routines_menu.configure_routines_menu_connections(main_window)


def replace_image_viewer(image_viewer):
    drawable_image_viewer = QDrawable_label(image_viewer.parent())
    drawable_image_viewer.setGeometry(image_viewer.geometry())
    drawable_image_viewer.setAlignment(QtCore.Qt.AlignCenter)
    drawable_image_viewer.setObjectName("image_viewer")
    return drawable_image_viewer
