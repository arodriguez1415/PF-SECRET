partial_save_path = "./generated/"


class Project_mastermind:
    __instance = None
    image_processing_list = []
    image_processing_stage = 0
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

    def create_stage_path_name(self, method_name):
        file_extension = ".tif"
        save_path = partial_save_path + "stage-" + str(self.image_processing_stage) + "-" + method_name
        full_save_path = save_path + file_extension
        return full_save_path

    def add_image_process(self, image_wrapper):
        self.image_processing_list.append(image_wrapper)
        self.image_processing_stage += 1

    def get_last_image_process(self):
        return self.image_processing_list[-1]

    def get_last_image(self):
        return self.image_processing_list[-1].image_array

    def clear_processing(self):
        self.image_processing_list = []
        self.image_processing_stage = 0