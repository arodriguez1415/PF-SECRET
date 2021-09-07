import os
from tkinter import filedialog, Tk

import numpy as np
import pandas as pd

from src.Backend.Image_processing_algorithms.Operations.common_operations import normalize_to_range
from src.Constants import configuration_constants, algorithm_constants, string_constants


def get_dataframe_path():
    root = Tk()
    root.withdraw()
    initial_absolute_directory_path = os.path.abspath(configuration_constants.METRICS_DIRECTORY_PATH)
    file_path = filedialog.askopenfilename(initialdir=initial_absolute_directory_path,
                                           title=string_constants.CHOOSE_EXCEL_WINDOW,
                                           filetypes=[("Excel", "*.xlsx"),
                                                      ("xlsx", "*.XLSX"),
                                                      ("All files", "*")],)
    if type(file_path) == tuple:
        file_path = ""

    root.destroy()
    return file_path


def get_multiple_dataframes_path():
    root = Tk()
    root.withdraw()
    initial_absolute_directory_path = os.path.abspath(configuration_constants.METRICS_DIRECTORY_PATH)
    file_path_list = filedialog.askopenfilenames(initialdir=initial_absolute_directory_path,
                                                 title=string_constants.CHOOSE_EXCEL_WINDOW,
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


def normalize_dataframe_values(dataframe, normalize_method=algorithm_constants.FROM_0_TO_255):
    dataframe_column_names = list(dataframe.columns)

    for col_index in range(0, len(dataframe_column_names)):
        col_name = dataframe_column_names[col_index]
        values = dataframe[col_name].to_numpy()
        normalized_values = normalize_to_range(values, max_value=normalize_method)
        dataframe[col_name] = normalized_values

    return dataframe


def is_excel(file_path):
    extension = os.path.splitext(file_path)[1]
    admitted_extensions = [".xlsx"]

    if extension not in admitted_extensions:
        return False

    return True


def are_excels(file_path_list):
    flag = True
    for i in range(0, len(file_path_list)):
        flag = flag and is_excel(file_path_list[i])

    return flag
