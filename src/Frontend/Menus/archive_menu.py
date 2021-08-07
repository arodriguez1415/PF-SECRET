import src.Frontend.Utils.message as messages
from src.Backend.Image_processing_algorithms.Archive_manipulation import image_file_manipulation
from src.Classes.Methods.Original import Original
from src.Classes.Project_mastermind import Project_mastermind
from src.Classes.Image_loader import Image_loader
from src.Constants import string_constants
from src.Frontend.Utils.viewer_buttons import disable_extra_views, enable_view_button


def configure_archive_menu_connections(main_window):
    image_viewer = main_window.image_viewer
    main_window.load_main_image_menu_option.triggered.connect(lambda: load_image(image_viewer, method=Original()))


def load_image(image_viewer, method):
    project_mastermind = Project_mastermind.get_instance()
    image_path = image_file_manipulation.get_image_path()
    if image_path:
        image_wrapper = Image_loader(image_path, method=method)
    else:
        messages.show_error(string_constants.NO_PATH_SELECTION)
        return
    project_mastermind.clear_all()
    disable_extra_views(project_mastermind.main_window)
    project_mastermind.set_original_image_path(image_path)
    project_mastermind.set_original_image_dir(image_file_manipulation.get_image_dir(image_path))
    project_mastermind.add_image_process(image_wrapper)
    set_image_on_screen(image_wrapper, image_viewer)
    enable_view_button(string_constants.MAIN_VIEW)


def set_image_on_screen(image_wrapper, image_viewer):
    image_viewer.set_screen_image(image_wrapper)
