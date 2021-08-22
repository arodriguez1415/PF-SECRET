import os
import shutil
from pathlib import Path


def create_directory_if_not_exists(directory_path):
    if not os.path.isdir(directory_path):
        os.mkdir(directory_path)


def remove_directory(directory_path):
    shutil.rmtree(directory_path, ignore_errors=True)


def move_directory(source, destination):
    shutil.move(source, destination)


def move_file(source, destination):
    shutil.move(source, destination)


def get_parent_directory_path(directory_path):
    path = Path(directory_path)
    parent_directory_path = path.parent.absolute()
    return str(parent_directory_path) + "/"
