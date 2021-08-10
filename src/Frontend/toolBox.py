from src.Classes.Image_wrapper import Image_wrapper
from src.Classes.Project_mastermind import Project_mastermind
import src.Backend.Image_processing_algorithms.Operations.image_save as image_saver
from src.Constants.algorithm_constants import DIAGONAL_LINE_TYPE, HORIZONTAL_LINE_TYPE, VERTICAL_LINE_TYPE
from src.Frontend.Utils.button_controller import enable_button, disable_button


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
    main_window.save_image_button.clicked.connect(lambda: save_image())
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


def start_polygon(main_window):
    main_window.image_viewer.set_paint_flag()


def start_square(main_window):
    main_window.image_viewer.set_paint_flag()
    main_window.image_viewer.set_square_flag()


def start_fixed_square(main_window):
    main_window.image_viewer.set_paint_flag()
    main_window.image_viewer.set_fixed_square_flag()


def start_line(main_window, line_type=DIAGONAL_LINE_TYPE):
    main_window.image_viewer.set_paint_flag()
    if line_type == HORIZONTAL_LINE_TYPE or line_type == VERTICAL_LINE_TYPE:
        print("Falta funcionalidad")
    else:
        main_window.image_viewer.set_diagonal_line_flag()


def clear_region(main_window):
    main_window.image_viewer.clear_region()


def show_process_list(main_window):
    print("Show process list functionality")


def undo(main_window):
    project_mastermind = Project_mastermind.get_instance()
    project_mastermind.remove_last_processing()
    last_processing = project_mastermind.get_last_image()
    image_wrapper = Image_wrapper(last_processing)
    main_window.image_viewer.set_screen_image(image_wrapper)


def save_image():
    project_mastermind = Project_mastermind.get_instance()
    current_image_array = project_mastermind.get_last_image()
    image_save_path = image_saver.get_save_path(current_image_array)
    image_saver.save_image(current_image_array, image_save_path)


def get_next_image(main_window):
    print("Next functionality")


def get_previous_image(main_window):
    print("Previous functionality")




