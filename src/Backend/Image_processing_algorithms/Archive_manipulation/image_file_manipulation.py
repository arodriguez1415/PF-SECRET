from pathlib import Path
import os
from tkinter import filedialog, Tk

from src.Classes.Project_mastermind import Project_mastermind
from src.Constants.properties_constants import IMAGES_SOURCE_FOLDER


def get_image_path():
    root = Tk()
    root.withdraw()
    project_mastermind = Project_mastermind.get_instance()
    properties_dictionary = project_mastermind.get_properties_dictionary()
    initial_absolute_directory_path = os.path.abspath(properties_dictionary[IMAGES_SOURCE_FOLDER])
    file_path = filedialog.askopenfilename(initialdir=initial_absolute_directory_path, title='Elegir imagen',
                                           filetypes=[("Image files", "*.tif;;*.pgm;;*.ppm;;*.jpg;;*.raw"),
                                                      ("ppm", "*.PPM"),
                                                      ("jpg", "*.JPG"),
                                                      ("raw", "*.RAW"),
                                                      ("tif", "*.TIF"),
                                                      ("All files", "*")])
    root.destroy()
    return file_path


def get_multiple_images_path():
    root = Tk()
    root.withdraw()
    project_mastermind = Project_mastermind.get_instance()
    properties_dictionary = project_mastermind.get_properties_dictionary()
    initial_absolute_directory_path = os.path.abspath(properties_dictionary[IMAGES_SOURCE_FOLDER])
    file_path_list = filedialog.askopenfilenames(initialdir=initial_absolute_directory_path,
                                                 title='Elegir imagenes a testear',
                                                 filetypes=[("Image files", "*.tif;;*.pgm;;*.ppm;;*.jpg;;*.raw"),
                                                      ("ppm", "*.PPM"),
                                                      ("jpg", "*.JPG"),
                                                      ("raw", "*.RAW"),
                                                      ("tif", "*.TIF"),
                                                      ("All files", "*")])
    root.destroy()
    return file_path_list


def get_directory_path():
    root = Tk()
    root.withdraw()
    project_mastermind = Project_mastermind.get_instance()
    properties_dictionary = project_mastermind.get_properties_dictionary()
    initial_absolute_directory_path = os.path.abspath(properties_dictionary[IMAGES_SOURCE_FOLDER])
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
    project_mastermind = Project_mastermind.get_instance()
    properties_dictionary = project_mastermind.get_properties_dictionary()
    initial_absolute_directory_path = os.path.abspath(properties_dictionary[IMAGES_SOURCE_FOLDER])
    file_path = filedialog.askopenfilename(initialdir=initial_absolute_directory_path, title='Choose Information',
                                           filetypes=[("txt", "*.TXT"),
                                                      ("All files", "*")])
    root.destroy()
    return file_path