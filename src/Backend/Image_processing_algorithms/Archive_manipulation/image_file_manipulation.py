import os
from pathlib import Path
from tkinter import filedialog, Tk

from src.Classes.Project_mastermind import Project_mastermind
from src.Constants import string_constants
from src.Constants.properties_constants import IMAGES_SOURCE_FOLDER


def get_image_path():
    root = Tk()
    root.withdraw()
    project_mastermind = Project_mastermind.get_instance()
    properties_dictionary = project_mastermind.get_properties_dictionary()
    initial_absolute_directory_path = os.path.abspath(properties_dictionary[IMAGES_SOURCE_FOLDER])
    file_path = filedialog.askopenfilename(initialdir=initial_absolute_directory_path,
                                           title=string_constants.CHOOSE_IMAGE_WINDOW,
                                           filetypes=[("Image files", "*.tif"),
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
                                                 title=string_constants.CHOOSE_MULTIPLE_IMAGES_WINDOW,
                                                 filetypes=[("Image files", "*.tif"),
                                                            ("tif", "*.TIF"),
                                                            ("All files", "*")])
    root.destroy()
    return file_path_list


def get_initial_directory():
    root = Tk()
    root.withdraw()
    directory_path = filedialog.askdirectory(title=string_constants.CHOOSE_DIRECTORY_WINDOW)
    root.destroy()
    return directory_path


def get_directory_path(path=None):
    root = Tk()
    root.withdraw()
    project_mastermind = Project_mastermind.get_instance()
    properties_dictionary = project_mastermind.get_properties_dictionary()
    if path is None:
        initial_absolute_directory_path = os.path.abspath(properties_dictionary[IMAGES_SOURCE_FOLDER])
    else:
        initial_absolute_directory_path = os.path.abspath(path)
    directory_path = filedialog.askdirectory(initialdir=initial_absolute_directory_path,
                                             title=string_constants.CHOOSE_DIRECTORY_WINDOW)
    root.destroy()
    return directory_path


def get_image_dir(file_path):
    path = Path(file_path)
    dir_path = path.parent.absolute()
    return dir_path


def get_source_directory(source_directory=None):
    if source_directory is None:
        source_directory = get_directory_path()
    return source_directory


def get_images_from_directories(source_directory):
    directories_list = os.walk(get_source_directory(source_directory))
    images_list_of_lists = []
    filtered_list_of_lists = []
    for directory_wrapper in directories_list:
        directory_path = directory_wrapper[0]
        images_list_of_lists.append(get_files_from_directory(directory_path))
    for images_list in images_list_of_lists:
        if images_list:
            filtered_list_of_lists.append(images_list)
    return filtered_list_of_lists


def get_files_from_directory(directory):
    directory_files_paths_list = os.listdir(directory)
    correct_directory_files_paths_list = []
    for file in directory_files_paths_list:
        if file.endswith(string_constants.TIF_EXTENSION):
            file_path = os.path.join(directory, file)
            correct_directory_files_paths_list.append(file_path)
    if correct_directory_files_paths_list and len(correct_directory_files_paths_list) > 1:
        correct_directory_files_paths_list.pop()
    return correct_directory_files_paths_list


def is_image(image_path):
    extension = os.path.splitext(image_path)[1]
    admitted_extensions = [".tif"]

    if extension not in admitted_extensions:
        return False

    return True
