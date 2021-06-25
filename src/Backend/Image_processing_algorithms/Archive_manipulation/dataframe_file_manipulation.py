import os
from tkinter import filedialog, Tk
import pandas as pd
import numpy as np

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


def create_dataframe_from_descriptors(list_descriptors_dict):
    if list_descriptors_dict is None or len(list_descriptors_dict) == 0:
        return pd.DataFrame()

    dataframe_dictionary = {}

    for descriptor in range(0, len(list_descriptors_dict)):
        data = np.reshape(list_descriptors_dict[descriptor]["data"], -1)
        col_name = list_descriptors_dict[descriptor]["label"]
        dataframe_dictionary[col_name] = data

    rows, cols = list_descriptors_dict[0]["data"].shape[0], list_descriptors_dict[0]["data"].shape[1]

    position_row_list = []
    position_col_list = []

    for row in range(0, rows):
        for col in range(0, cols):
            position_row_list.append(row)
            position_col_list.append(col)

    dataframe_dictionary["row"] = position_row_list
    dataframe_dictionary["col"] = position_col_list

    dataframe = pd.DataFrame(dataframe_dictionary)

    return dataframe



