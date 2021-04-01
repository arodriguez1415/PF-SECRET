from src.Classes.Image_wrapper import Image_wrapper
from src.Classes.Project_mastermind import Project_mastermind
import src.Backend.Image_processing_algorithms.Operations.image_save as image_saver


def configure_toolBox_connections(main_window):
    main_window.polygon_region_button.clicked.connect(lambda: start_polygon(main_window))
    main_window.square_region_button.clicked.connect(lambda: start_square(main_window))
    main_window.clear_region_button.clicked.connect(lambda: clear_region(main_window))
    main_window.undo_button.clicked.connect(lambda: undo(main_window))
    main_window.save_image_button.clicked.connect(lambda: save_image())


def start_polygon(main_window):
    main_window.image_viewer.set_paint_flag()


def start_square(main_window):
    main_window.image_viewer.set_paint_flag()
    main_window.image_viewer.set_square_flag()


def clear_region(main_window):
    main_window.image_viewer.clear_region()


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






