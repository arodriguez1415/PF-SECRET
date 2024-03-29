import os

from PyQt5.QtWidgets import QProgressDialog

from src.Constants import string_constants


class Project_mastermind:
    __instance = None

    # Image processing attributes
    image_processing_list = []
    original_images_in_dir_path = []
    current_original_image_index = 0
    original_image_path = None
    original_image_dir = None

    # Progress Bar and messages attributes
    wait_message = None
    normal_progress_bar = None
    global_progress_bar = None
    is_global_progress_bar_active_flag = None
    cancel_progress_bar_flag = False

    # Current view
    current_view = None

    # Application attributes
    properties_dictionary = None
    main_window = None
    process_list_widget = None
    process_list = None
    global_routine_params = None
    global_routine_params_widget = None
    app = None

    # Movement and Texture processing attributes
    movement_image_wrapper = None
    normalized_movement_wrapper = None
    movement_heat_map_image_wrapper = None
    texture_image_wrapper = None
    texture_heat_map_image_wrapper = None
    texture_image_video_wrapper = None
    texture_heat_map_image_video_wrapper = None

    def __init__(self, app, main_window,
                 process_list, process_list_widget,
                 global_routine_params, global_routine_params_widget):
        if Project_mastermind.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            Project_mastermind.__instance = self
            self.app = app
            self.main_window = main_window
            self.process_list = process_list
            self.process_list_widget = process_list_widget
            self.global_routine_params = global_routine_params
            self.global_routine_params_widget = global_routine_params_widget
            self.is_global_progress_bar_active_flag = False

    @staticmethod
    def get_instance():
        return Project_mastermind.__instance

    def get_wait_message(self):
        return self.wait_message

    def get_normal_progress_bar(self):
        return self.normal_progress_bar

    def get_global_progress_bar(self):
        return self.global_progress_bar

    def is_global_progress_bar_active(self):
        return self.is_global_progress_bar_active_flag

    def is_cancel_progress_bar_flag_active(self):
        return self.cancel_progress_bar_flag

    def reset_normal_progress_bar(self):
        self.normal_progress_bar = QProgressDialog("", string_constants.CANCEL_BUTTON_TEXT, 0, 0)

    def reset_global_progress_bar(self):
        self.global_progress_bar = QProgressDialog("", string_constants.CANCEL_BUTTON_TEXT, 0, 0)

    def add_image_process(self, image_wrapper):
        self.image_processing_list.append(image_wrapper)

    def get_last_image_process(self):
        if len(self.image_processing_list) == 0:
            return
        return self.image_processing_list[-1]

    def get_last_image(self):
        if len(self.image_processing_list) == 0:
            return
        return self.image_processing_list[-1].image_array

    def get_original_image(self):
        if len(self.image_processing_list) == 0:
            return
        return self.image_processing_list[0].image_array

    def get_last_image_wrapper(self):
        if len(self.image_processing_list) == 0:
            return
        return self.image_processing_list[-1]

    def get_original_image_wrapper(self):
        if len(self.image_processing_list) == 0:
            return
        return self.image_processing_list[0]

    def get_movement_heat_map_image(self):
        return self.movement_heat_map_image_wrapper

    def get_movement_image(self):
        return self.movement_image_wrapper

    def get_normalized_movement_wrapper(self):
        return self.normalized_movement_wrapper

    def get_texture_heat_map_image(self):
        return self.texture_heat_map_image_wrapper

    def get_texture_image(self):
        return self.texture_image_wrapper

    def get_texture_heat_map_image_video(self):
        return self.texture_heat_map_image_video_wrapper

    def get_texture_image_video(self):
        return self.texture_image_video_wrapper

    def remove_last_processing(self):
        if len(self.image_processing_list) > 1:
            del (self.image_processing_list[-1])

    def get_original_image_path(self):
        return self.original_image_path

    def get_original_image_dir(self):
        return self.original_image_dir

    def get_image_processing_list(self):
        return self.image_processing_list

    def get_original_images_from_dir_path(self):
        return self.original_images_in_dir_path

    def get_current_original_image_index(self):
        return self.current_original_image_index

    def get_next_original_image(self):
        index = self.current_original_image_index + 1
        list_of_images = self.get_original_images_from_dir_path()
        if len(list_of_images) <= index:
            return None
        self.clear_on_original_image_change()
        self.current_original_image_index += 1
        return list_of_images[index]

    def get_previous_original_image(self):
        index = self.current_original_image_index - 1
        list_of_images = self.get_original_images_from_dir_path()
        if len(list_of_images) == index or index < 0:
            return None
        self.clear_on_original_image_change()
        self.current_original_image_index -= 1
        return list_of_images[index]

    def get_properties_dictionary(self):
        return self.properties_dictionary

    def get_current_view(self):
        return self.current_view

    def set_wait_message(self, wait_message):
        self.wait_message = wait_message

    def set_normal_progress_bar(self, progress_bar):
        self.normal_progress_bar = progress_bar

    def set_global_progress_bar(self, progress_bar):
        self.global_progress_bar = progress_bar

    def set_global_progress_bar_active(self, flag):
        self.is_global_progress_bar_active_flag = flag

    def set_cancel_progress_bar_flag(self, flag):
        self.cancel_progress_bar_flag = flag

    def set_original_image_path(self, original_image_path):
        self.original_image_path = original_image_path

    def set_original_image_dir(self, original_image_dir):
        self.original_image_dir = original_image_dir

    def set_original_images_from_dir_path(self, image_dir):
        self.original_images_in_dir_path = self.get_files_from_directory(image_dir)
        self.find_current_original_image_index()

    def find_current_original_image_index(self):
        original_path = os.path.realpath(self.original_image_path)
        for i in range(0, len(self.original_images_in_dir_path)):
            current_path = os.path.realpath(self.original_images_in_dir_path[i])
            if current_path == original_path:
                self.current_original_image_index = i
                label_text = str(i + 1) + "/" + str(len(self.original_images_in_dir_path))
                self.main_window.images_index_label.setText(label_text)
                return
        raise Exception("Not found")

    def set_image_processing_list(self, image_processing_list):
        self.image_processing_list = image_processing_list

    def set_movement_heat_map_image(self, movement_heat_map_image):
        self.movement_heat_map_image_wrapper = movement_heat_map_image

    def set_movement_image(self, movement_image):
        self.movement_image_wrapper = movement_image

    def set_normalized_movement_image(self, normalized_movement_image):
        self.normalized_movement_wrapper = normalized_movement_image

    def set_texture_heat_map_image(self, texture_heat_map_image):
        self.texture_heat_map_image_wrapper = texture_heat_map_image

    def set_texture_image(self, texture_image):
        self.texture_image_wrapper = texture_image

    def set_texture_heat_map_image_video(self, texture_heat_map_image_video):
        self.texture_heat_map_image_video_wrapper = texture_heat_map_image_video

    def set_texture_image_video(self, texture_image_video):
        self.texture_image_video_wrapper = texture_image_video

    def set_current_view(self, view_name):
        self.current_view = view_name

    def reload_properties(self, new_properties_dictionary):
        self.properties_dictionary = new_properties_dictionary

    def get_files_from_directory(self, directory):
        directory_files_paths_list = os.listdir(directory)
        directory_files_paths_list.sort()
        correct_directory_files_paths_list = []
        for file in directory_files_paths_list:
            if file.endswith(string_constants.TIF_EXTENSION):
                file_path = os.path.join(directory, file)
                correct_directory_files_paths_list.append(file_path)
        if correct_directory_files_paths_list and len(correct_directory_files_paths_list) > 1:
            correct_directory_files_paths_list.pop()
        return correct_directory_files_paths_list

    def clear_all(self):
        self.image_processing_list = []
        self.original_images_in_dir_path = []
        self.current_original_image_index = 0
        self.original_image_path = None
        self.original_image_dir = None
        self.wait_message = None
        self.normal_progress_bar = None
        self.global_progress_bar = None
        self.is_global_progress_bar_active_flag = False
        self.cancel_progress_bar_flag = False
        self.movement_image_wrapper = None
        self.normalized_movement_wrapper = None
        self.movement_heat_map_image_wrapper = None
        self.texture_image_wrapper = None
        self.texture_heat_map_image_wrapper = None
        self.texture_image_video_wrapper = None
        self.texture_heat_map_image_video_wrapper = None

    def clear_on_original_image_change(self):
        self.image_processing_list = []
        self.wait_message = None
        self.normal_progress_bar = None
        self.global_progress_bar = None
        self.is_global_progress_bar_active_flag = False
        self.cancel_progress_bar_flag = False
        self.texture_image_wrapper = None
        self.texture_heat_map_image_wrapper = None
