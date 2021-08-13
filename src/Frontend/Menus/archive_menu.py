import src.Frontend.Utils.message as messages
from src.Backend.Image_processing_algorithms.Archive_manipulation import image_file_manipulation
from src.Backend.Image_processing_algorithms.Archive_manipulation.properties_manipulation import save_properties
from src.Classes.Image_wrapper import Image_wrapper
from src.Classes.Methods.Original import Original
from src.Classes.Project_mastermind import Project_mastermind
from src.Classes.Image_loader import Image_loader
from src.Constants import string_constants
from src.Constants.properties_constants import IMAGES_SOURCE_FOLDER
from src.Frontend.Utils.viewer_buttons import disable_extra_views, enable_view_button
from src.Frontend.toolBox import enable_toolbox


def configure_archive_menu_connections(main_window):
    image_viewer = main_window.image_viewer
    main_window.load_main_image_menu_option.triggered.connect(lambda: load_image(image_viewer, method=Original()))
    main_window.set_images_source_directory_menu_option.triggered.connect(lambda: set_images_source_directory())


def load_image(image_viewer, method):
    project_mastermind = Project_mastermind.get_instance()
    image_path = image_file_manipulation.get_image_path()
    image_dir = image_file_manipulation.get_image_dir(image_path)
    if image_path:
        image_loader = Image_loader(image_path, method=method)
        image_wrapper = Image_wrapper(image_loader.image_array, method=method)
    else:
        return
    project_mastermind.clear_all()
    disable_extra_views(project_mastermind.main_window)
    enable_toolbox(project_mastermind.main_window)
    project_mastermind.set_original_image_path(image_path)
    project_mastermind.set_original_images_from_dir_path(image_dir)
    project_mastermind.set_original_image_dir(image_dir)
    project_mastermind.add_image_process(image_wrapper)
    set_image_on_screen(image_loader, image_viewer)
    enable_view_button(string_constants.MAIN_VIEW)


def set_image_on_screen(image_wrapper, image_viewer):
    image_viewer.set_screen_image(image_wrapper)


def set_images_source_directory():
    project_mastermind = Project_mastermind.get_instance()
    source_directory_path = image_file_manipulation.get_directory_path()
    properties_directory = project_mastermind.get_properties_dictionary()
    properties_directory[IMAGES_SOURCE_FOLDER] = source_directory_path
    save_properties(properties_directory)
    project_mastermind.reload_properties(properties_directory)