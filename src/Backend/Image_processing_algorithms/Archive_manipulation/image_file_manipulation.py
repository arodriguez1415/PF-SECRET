from pathlib import Path
import os
from tkinter import filedialog, Tk

from src.Constants.configuration_constants import TEST_IMAGES_DIR, GENERAL_DIRECTORY


def get_image_path():
    root = Tk()
    root.withdraw()
    initial_absolute_directory_path = os.path.abspath(TEST_IMAGES_DIR)
    file_path = filedialog.askopenfilename(initialdir=initial_absolute_directory_path, title='Elegir imagen',
                                           filetypes=[("Image files", "*.tif;;*.pgm;;*.ppm;;*.jpg;;*.raw"),
                                                      ("ppm", "*.PPM"),
                                                      ("jpg", "*.JPG"),
                                                      ("raw", "*.RAW"),
                                                      ("tif", "*.TIF"),
                                                      ("All files", "*")])
    root.destroy()
    return file_path


def get_directory_path():
    root = Tk()
    root.withdraw()
    initial_absolute_directory_path = os.path.abspath(GENERAL_DIRECTORY)
    directory_path = filedialog.askdirectory(initialdir=initial_absolute_directory_path, title='Elegir carpeta')
    root.destroy()
    return directory_path


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