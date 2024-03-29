import os

from src.Backend.Image_processing_algorithms.Archive_manipulation import image_file_manipulation
from src.Backend.Image_processing_algorithms.Archive_manipulation.image_file_manipulation import is_image
from src.Backend.Image_processing_algorithms.Archive_manipulation.properties_manipulation import save_properties, \
    generate_default_manual_routines_properties, set_manual_routines_properties
from src.Classes.Image_loader import Image_loader
from src.Classes.Image_wrapper import Image_wrapper
from src.Classes.Methods.Original import Original
from src.Classes.Project_mastermind import Project_mastermind
from src.Constants import string_constants, configuration_constants
from src.Constants.properties_constants import IMAGES_SOURCE_FOLDER, OUTPUT_FOLDER
from src.Constants.string_constants import DEFAULT_PARAMETERS_MANUAL_ROUTINE_TITLE, \
    DEFAULT_PARAMETERS_MANUAL_ROUTINE_DESCRIPTION
from src.Frontend.Utils.message import show_error_message, show_confirmation_message
from src.Frontend.Utils.viewer_buttons import disable_extra_views, enable_view_button
from src.Frontend.toolBox import enable_toolbox


def configure_archive_menu_connections(main_window):
    image_viewer = main_window.image_viewer
    main_window.load_main_image_menu_option.triggered.connect(lambda: load_image(image_viewer, method=Original()))
    main_window.set_images_source_directory_menu_option.triggered.connect(lambda: set_images_source_directory())
    main_window.set_output_directory_menu_option.triggered.connect(lambda: set_output_directory())
    main_window.restore_defaults_menu_option.triggered.connect(lambda: set_default_manual_routine_properties())


def load_image(image_viewer, method, image_path=""):
    project_mastermind = Project_mastermind.get_instance()

    if image_path == "":
        image_path = image_file_manipulation.get_image_path()

    image_dir = image_file_manipulation.get_image_dir(image_path)

    if not is_image(image_path):
        show_error_message(string_constants.NO_IMAGE_FILE)
        return

    image_loader = Image_loader(image_path, method=method)
    image_wrapper = Image_wrapper(image_loader.image_array, method=method)
    project_mastermind.clear_all()
    disable_extra_views(project_mastermind.main_window)
    enable_toolbox(project_mastermind.main_window)
    project_mastermind.set_original_image_path(image_path)
    project_mastermind.set_original_images_from_dir_path(image_dir)
    project_mastermind.set_original_image_dir(image_dir)
    project_mastermind.add_image_process(image_wrapper)
    project_mastermind.set_current_view(string_constants.MAIN_VIEW)
    set_image_on_screen(image_wrapper, image_viewer)
    enable_view_button(string_constants.MAIN_VIEW)


def set_image_on_screen(image_wrapper, image_viewer):
    image_viewer.set_screen_image(image_wrapper)


def set_images_source_directory():
    project_mastermind = Project_mastermind.get_instance()
    properties_directory = project_mastermind.get_properties_dictionary()
    source_directory_path = image_file_manipulation.get_directory_path(properties_directory[IMAGES_SOURCE_FOLDER])

    if source_directory_path == "" or source_directory_path is None:
        return

    properties_directory[IMAGES_SOURCE_FOLDER] = source_directory_path
    save_properties(properties_directory)
    project_mastermind.reload_properties(properties_directory)


def set_default_manual_routine_properties():
    project_mastermind = Project_mastermind.get_instance()

    title = DEFAULT_PARAMETERS_MANUAL_ROUTINE_TITLE
    description = DEFAULT_PARAMETERS_MANUAL_ROUTINE_DESCRIPTION
    continue_flag = show_confirmation_message(title, description)

    if continue_flag:
        props_dictionary = project_mastermind.get_properties_dictionary()
        props_dictionary = generate_default_manual_routines_properties(props_dictionary)
        project_mastermind.reload_properties(props_dictionary)
        set_manual_routines_properties(props_dictionary, project_mastermind.main_window)
        save_properties(props_dictionary)


def set_output_directory():
    project_mastermind = Project_mastermind.get_instance()
    properties_directory = project_mastermind.get_properties_dictionary()
    output_directory_path = image_file_manipulation.get_directory_path(properties_directory[OUTPUT_FOLDER])
    output_directory_path += "/" + configuration_constants.GENERATED_DIR_NAME

    if output_directory_path == "" or output_directory_path is None:
        return

    properties_directory = project_mastermind.get_properties_dictionary()
    properties_directory[OUTPUT_FOLDER] = output_directory_path
    configuration_constants.GENERATED_IMAGES_DIR = output_directory_path
    save_properties(properties_directory)
    project_mastermind.reload_properties(properties_directory)
