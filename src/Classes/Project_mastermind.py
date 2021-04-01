import os
import src.Frontend.Utils.message as messages

partial_save_path = "./generated/"


class Project_mastermind:
    __instance = None
    image_processing_list = []
    original_image_path = None
    original_image_dir = None
    main_window = None
    app = None

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

    def create_video_path_name(self, video_name):
        file_extension = ".avi"
        video_save_path = partial_save_path + video_name + file_extension
        return video_save_path
