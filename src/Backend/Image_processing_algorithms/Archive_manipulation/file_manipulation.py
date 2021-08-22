import os
import shutil
from pathlib import Path
from tkinter import Tk, filedialog

from src.Constants import configuration_constants
from src.Constants.string_constants import WRITE_FILENAME


def create_directory_if_not_exists(directory_path):
    if not os.path.isdir(directory_path):
        os.mkdir(directory_path)


def remove_directory(directory_path):
    shutil.rmtree(directory_path, ignore_errors=True)


def move_directory(source, destination):
    shutil.move(source, destination)


def move_file(source, destination):
    shutil.move(source, destination)


def rename_file(source, destination):
    shutil.move(source, destination)


def get_parent_directory_path(directory_path):
    path = Path(directory_path)
    parent_directory_path = path.parent.absolute()
    return str(parent_directory_path) + "/"


def get_save_path():
    root = Tk()
    root.withdraw()
    save_extension = ".avi"
    save_file_path = filedialog.asksaveasfilename(initialdir=configuration_constants.GENERATED_VIDEOS_DEFAULT_DIR,
                                                  title=WRITE_FILENAME,
                                                  defaultextension=save_extension,
                                                  filetypes=(("Avi file", "*.avi"),("All Files", "*.*"))
                                                  )
    root.destroy()
    return save_file_path
