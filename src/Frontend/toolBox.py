from PyQt5.QtCore import Qt

from src.Classes.Image_loader import Image_loader
from src.Classes.Image_wrapper import Image_wrapper
from src.Classes.Methods.Original import Original
from src.Classes.Project_mastermind import Project_mastermind
import src.Backend.Image_processing_algorithms.Operations.image_save as image_saver
from src.Constants.algorithm_constants import DIAGONAL_LINE_TYPE, HORIZONTAL_LINE_TYPE, VERTICAL_LINE_TYPE
from src.Constants.string_constants import PROCESS_LIST_WIDGET_TITLE
from src.Frontend.Utils.button_controller import enable_button, disable_button, select_button, deselect_all
from src.Frontend.process_list import populate_process_list


def configure_toolBox_connections(main_window):
    main_window.polygon_region_button.clicked.connect(lambda: start_polygon(main_window))
    main_window.square_region_button.clicked.connect(lambda: start_square(main_window))
    main_window.fixed_square_region_button.clicked.connect(lambda: start_fixed_square(main_window))
    main_window.diagonal_line_button.clicked.connect(lambda: start_line(main_window, line_type=DIAGONAL_LINE_TYPE))
    main_window.horizontal_line_button.clicked.connect(lambda: start_line(main_window, line_type=HORIZONTAL_LINE_TYPE))
    main_window.vertical_line_button.clicked.connect(lambda: start_line(main_window, line_type=VERTICAL_LINE_TYPE))
    main_window.clear_region_button.clicked.connect(lambda: clear_region(main_window))
    main_window.process_information_button.clicked.connect(lambda: show_process_list(main_window))
    main_window.undo_button.clicked.connect(lambda: undo(main_window))
    main_window.save_image_button.clicked.connect(lambda: save_image(main_window))
    main_window.next_image_button.clicked.connect(lambda: get_next_image(main_window))
    main_window.previous_image_button.clicked.connect(lambda: get_previous_image(main_window))


def enable_toolbox(main_window):
    enable_button(main_window.polygon_region_button)
    enable_button(main_window.square_region_button)
    enable_button(main_window.fixed_square_region_button)
    enable_button(main_window.diagonal_line_button)
    enable_button(main_window.horizontal_line_button)
    enable_button(main_window.vertical_line_button)
    enable_button(main_window.clear_region_button)
    enable_button(main_window.process_information_button)
    enable_button(main_window.undo_button)
    enable_button(main_window.save_image_button)
    enable_button(main_window.next_image_button)
    enable_button(main_window.previous_image_button)


def disable_toolbox(main_window):
    disable_button(main_window.polygon_region_button)
    disable_button(main_window.square_region_button)
    disable_button(main_window.fixed_square_region_button)
    disable_button(main_window.diagonal_line_button)
    disable_button(main_window.horizontal_line_button)
    disable_button(main_window.vertical_line_button)
    disable_button(main_window.clear_region_button)
    disable_button(main_window.process_information_button)
    disable_button(main_window.undo_button)
    disable_button(main_window.save_image_button)
    disable_button(main_window.next_image_button)
    disable_button(main_window.previous_image_button)


def deselect_all_and_clear_viewer(main_window):
    deselect_all(main_window)
    main_window.image_viewer.clear_region()
    main_window.image_viewer.reset_line_flag()


def start_polygon(main_window):
    deselect_all_and_clear_viewer(main_window)
    main_window.image_viewer.set_paint_flag()
    select_button(main_window.polygon_region_button)


def start_square(main_window):
    deselect_all_and_clear_viewer(main_window)
    main_window.image_viewer.set_paint_flag()
    main_window.image_viewer.set_square_flag()
    select_button(main_window.square_region_button)


def start_fixed_square(main_window):
    deselect_all_and_clear_viewer(main_window)
    main_window.image_viewer.set_paint_flag()
    main_window.image_viewer.set_fixed_square_flag()
    select_button(main_window.fixed_square_region_button)


def start_line(main_window, line_type=DIAGONAL_LINE_TYPE):
    deselect_all_and_clear_viewer(main_window)
    main_window.image_viewer.set_paint_flag()
    if line_type == HORIZONTAL_LINE_TYPE:
        main_window.image_viewer.set_fixed_line_type(line_type)
        select_button(main_window.horizontal_line_button)
    elif line_type == VERTICAL_LINE_TYPE:
        main_window.image_viewer.set_fixed_line_type(line_type)
        select_button(main_window.vertical_line_button)
    else:
        main_window.image_viewer.set_diagonal_line_flag()
        select_button(main_window.diagonal_line_button)


def clear_region(main_window):
    deselect_all(main_window)
    main_window.image_viewer.clear_region()


def show_process_list(main_window):
    deselect_all_and_clear_viewer(main_window)
    project_mastermind = Project_mastermind.get_instance()
    process_list_widget = project_mastermind.process_list_widget
    process_list_widget.setWindowTitle(PROCESS_LIST_WIDGET_TITLE)
    process_list_widget.setWindowModality(Qt.WindowModal)
    process_list_widget.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowTitleHint)
    populate_process_list()
    process_list_widget.exec()


def undo(main_window):
    deselect_all_and_clear_viewer(main_window)
    project_mastermind = Project_mastermind.get_instance()
    project_mastermind.remove_last_processing()
    last_processing = project_mastermind.get_last_image()
    image_wrapper = Image_wrapper(last_processing)
    main_window.image_viewer.set_screen_image(image_wrapper)


def save_image(main_window):
    deselect_all_and_clear_viewer(main_window)
    project_mastermind = Project_mastermind.get_instance()
    current_image_array = project_mastermind.get_last_image()
    image_save_path = image_saver.get_save_image_path()

    if image_save_path == "" or image_save_path is None:
        return

    image_saver.save_image(current_image_array, image_save_path)


def get_next_image(main_window):
    project_mastermind = Project_mastermind.get_instance()
    image_path = project_mastermind.get_next_original_image()
    project_mastermind = Project_mastermind.get_instance()
    deselect_all_and_clear_viewer(main_window)

    if image_path is None:
        disable_button(main_window.next_image_button)
        return

    current_index = project_mastermind.get_current_original_image_index()
    original_list_length = len(project_mastermind.get_original_images_from_dir_path())

    if current_index == original_list_length:
        disable_button(main_window.next_image_button)

    label_text = str(current_index + 1) + "/" + str(original_list_length)
    main_window.images_index_label.setText(label_text)
    enable_button(main_window.previous_image_button)
    image_loader = Image_loader(image_path, method=Original())
    image_wrapper = Image_wrapper(image_loader.image_array, method=Original())
    project_mastermind.add_image_process(image_wrapper)
    disable_button(main_window.texture_image)
    disable_button(main_window.movement_compare_to_texture_image)
    disable_button(main_window.texture_image_compare_to_texture_video)
    main_window.image_viewer.set_screen_image(image_loader)


def get_previous_image(main_window):
    project_mastermind = Project_mastermind.get_instance()
    image_path = project_mastermind.get_previous_original_image()
    project_mastermind = Project_mastermind.get_instance()
    deselect_all_and_clear_viewer(main_window)

    if image_path is None:
        disable_button(main_window.previous_image_button)
        return

    original_list_length = len(project_mastermind.get_original_images_from_dir_path())
    current_index = project_mastermind.get_current_original_image_index()

    if current_index == 0:
        disable_button(main_window.previous_image_button)

    label_text = str(current_index + 1) + "/" + str(original_list_length)
    main_window.images_index_label.setText(label_text)
    enable_button(main_window.next_image_button)
    image_loader = Image_loader(image_path, method=Original())
    image_wrapper = Image_wrapper(image_loader.image_array, method=Original())
    project_mastermind.add_image_process(image_wrapper)
    disable_button(main_window.texture_image)
    disable_button(main_window.movement_compare_to_texture_image)
    disable_button(main_window.texture_image_compare_to_texture_video)
    main_window.image_viewer.set_screen_image(image_loader)
