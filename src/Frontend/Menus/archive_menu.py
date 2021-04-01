import os
from tkinter import filedialog, Tk

import src.Frontend.Utils.message as messages
from src.Classes.Methods.Original import Original
from src.Classes.Project_mastermind import Project_mastermind
from src.Classes.Image_loader import Image_loader
from src.Constants.configuration_constants import TEST_IMAGES_DIR
from src.Constants import string_constants
from pathlib import Path


def configure_archive_menu_connections(main_window):
    image_viewer = main_window.image_viewer
    main_window.load_main_image_menu_option.triggered.connect(lambda: load_image(image_viewer, method=Original()))


def load_image(image_viewer, method):
    project_mastermind = Project_mastermind.get_instance()
    image_path = get_image_path()
    if image_path:
        image_wrapper = Image_loader(image_path, method=method)
    else:
        messages.show_error(string_constants.NO_PATH_SELECTION)
        return
    project_mastermind.clear_processing()
    project_mastermind.set_original_image_path(image_path)
    project_mastermind.set_original_image_dir(get_image_dir(image_path))
    project_mastermind.add_image_process(image_wrapper)
    set_image_on_screen(image_wrapper, image_viewer)


def set_image_on_screen(image_wrapper, image_viewer):
    image_viewer.set_screen_image(image_wrapper)


def get_image_path():
    root = Tk()
    root.withdraw()
    initial_absolute_directory_path = os.path.abspath(TEST_IMAGES_DIR)
    file_path = filedialog.askopenfilename(initialdir=initial_absolute_directory_path, title='Choose Image',
                                           filetypes=[("Image files", "*.tif;;*.pgm;;*.ppm;;*.jpg;;*.raw"),
                                                      ("ppm", "*.PPM"),
                                                      ("jpg", "*.JPG"),
                                                      ("raw", "*.RAW"),
                                                      ("tif", "*.TIF"),
                                                      ("All files", "*")])
    root.destroy()
    return file_path


def get_image_dir(file_path):
    path = Path(file_path)
    dir_path = path.parent.absolute()
    return dir_path


def get_information_path():
    root = Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(initialdir=TEST_IMAGES_DIR, title='Choose Information',
                                           filetypes=[("txt", "*.TXT"),
                                                      ("All files", "*")])
    root.destroy()
    return file_path
