import os
from tkinter import filedialog, Tk

from src.Constants import configuration_constants


def get_dataframe_path():
    root = Tk()
    root.withdraw()
    initial_absolute_directory_path = os.path.abspath(configuration_constants.METRICS_DIRECTORY_PATH)
    file_path = filedialog.askopenfilename(initialdir=initial_absolute_directory_path, title='Elegir excel de datos',
                                           filetypes=[("Excel", "*.xlsx"),
                                                      ("xlsx", "*.XLSX"),
                                                      ("All files", "*")])
    root.destroy()
    return file_path


def get_multiple_dataframes_path():
    root = Tk()
    root.withdraw()
    initial_absolute_directory_path = os.path.abspath(configuration_constants.METRICS_DIRECTORY_PATH)
    file_path_list = filedialog.askopenfilenames(initialdir=initial_absolute_directory_path,
                                                 title='Elegir excels de datos',
                                                 filetypes=[("Excel", "*.xlsx"),
                                                            ("xlsx", "*.XLSX"),
                                                            ("All files", "*")])
    root.destroy()
    return file_path_list
