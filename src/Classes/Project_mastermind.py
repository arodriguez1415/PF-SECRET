from PyQt5.QtWidgets import QProgressDialog

import src.Frontend.Utils.message as messages
from src.Constants import string_constants


class Project_mastermind:
    __instance = None
    image_processing_list = []
    original_image_path = None
    original_image_dir = None
    current_progress_bar = None
    main_window = None
    app = None
    heat_map_image_array = None

    def __init__(self, app, main_window):
        if Project_mastermind.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            self.main_window = main_window
            self.app = app
            Project_mastermind.__instance = self

    @staticmethod
    def get_instance():
        return Project_mastermind.__instance

    def set_current_progress_bar(self, progress_bar):
        self.current_progress_bar = progress_bar

    def get_current_progress_bar(self):
        return self.current_progress_bar

    def reset_current_progress_bar(self):
        self.current_progress_bar = QProgressDialog("", string_constants.CANCEL_BUTTON_TEXT, 0, 0)

    def add_image_process(self, image_wrapper):
        self.image_processing_list.append(image_wrapper)

    def get_last_image_process(self):
        if len(self.image_processing_list) == 0:
            messages.show_message("No se cargo ninguna imagen")
            return
        return self.image_processing_list[-1]

    def get_last_image(self):
        if len(self.image_processing_list) == 0:
            messages.show_message("No se cargo ninguna imagen")
            return
        return self.image_processing_list[-1].image_array

    def get_original_image(self):
        if len(self.image_processing_list) == 0:
            messages.show_message("No se cargo ninguna imagen")
            return
        return self.image_processing_list[0].image_array

    def get_last_image_wrapper(self):
        if len(self.image_processing_list) == 0:
            messages.show_message("No se cargo ninguna imagen")
            return
        return self.image_processing_list[-1]

    def get_original_image_wrapper(self):
        if len(self.image_processing_list) == 0:
            messages.show_message("No se cargo ninguna imagen")
            return
        return self.image_processing_list[0]

    def get_heat_map_image_array(self):
        return self.heat_map_image_array

    def clear_processing(self):
        self.image_processing_list = []

    def remove_last_processing(self):
        if len(self.image_processing_list) > 1:
            del(self.image_processing_list[-1])

    def set_original_image_path(self, original_image_path):
        self.original_image_path = original_image_path

    def set_original_image_dir(self, original_image_dir):
        self.original_image_dir = original_image_dir

    def get_original_image_path(self):
        return self.original_image_path

    def get_original_image_dir(self):
        return self.original_image_dir

    def get_image_processing_list(self):
        return self.image_processing_list

    def set_image_processing_list(self, image_processing_list):
        self.image_processing_list = image_processing_list

    def set_heat_map_image_array(self, heat_map_image_array):
        self.heat_map_image_array = heat_map_image_array
