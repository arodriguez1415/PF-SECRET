import shutil
import sys

from src.Backend.Image_processing_algorithms.Archive_manipulation.properties_manipulation import load_properties
from src.Classes.Methods.Original import Original
from src.Classes.Project_mastermind import Project_mastermind
from src.Constants import string_constants, configuration_constants
from src.Frontend.Menus.archive_menu import load_image
from src.Frontend.Utils import progress_bar
from src.Frontend.Utils.button_controller import enable_button
from src.Frontend.Utils.message import show_error_message

old_hook = sys.excepthook


def initialize_exception_handler():
    sys.excepthook = catch_any_exception


def catch_any_exception(error_class, error_type, traceback_object):
    if error_class == SystemExit or error_class == KeyboardInterrupt or error_class == GeneratorExit:
        sys.exit()

    if error_class is None or error_type is None or traceback_object is None:
        show_error_message(string_constants.UNKNOWN_ERROR)
        set_consistent_interface_state()
        return

    error_type_str = str(error_type)
    error_message = string_constants.UNKNOWN_ERROR + "\n\n" + string_constants.UNKNOWN_ERROR_TYPE + error_type_str
    show_error_message(error_message)
    set_consistent_interface_state()
    old_hook(error_class, error_type, traceback_object)


def set_consistent_interface_state():
    project_mastermind = Project_mastermind.get_instance()
    main_window = project_mastermind.main_window
    global_routine_params = project_mastermind.global_routine_params
    image_viewer = main_window.image_viewer

    original_image_path = project_mastermind.get_original_image_path()
    load_image(image_viewer, method=Original(), image_path=original_image_path)

    shutil.rmtree(configuration_constants.TEMPORARY_VIDEO_DIRECTORY_PATH, ignore_errors=True)
    project_mastermind.reload_properties(load_properties(main_window, global_routine_params))
    progress_bar.force_to_close()
    enable_process_buttons(main_window)


def enable_process_buttons(main_window):
    # Anisotropic Filter
    enable_button(main_window.apply_anisotropic_filter_button)

    # Adaptive Threshold
    enable_button(main_window.adaptive_threshold_add_process_button)

    # MGAC
    enable_button(main_window.apply_mgac_button)

    # Texture and Movement
    enable_button(main_window.texture_classification_video_button)
    enable_button(main_window.texture_classification_image_button)
    enable_button(main_window.texture_profile_apply_button)
    enable_button(main_window.generate_heat_map_button)

    # Metrics
    enable_button(main_window.analyze_movement_and_texture_button)
    enable_button(main_window.analyze_movement_and_texture_generate_views_button)
    enable_button(main_window.plot_metrics_distribution_button)
    enable_button(main_window.plot_metrics_generate_button)
    enable_button(main_window.generate_multiple_cells_metrics_generate_button)
    enable_button(main_window.generate_metrics_generate_button)
    enable_button(main_window.plot_metrics_load_dataframe_button)
    enable_button(main_window.generate_metrics_load_mask_video_button)

    # Global Routine
    enable_button(main_window.global_routine_initiate_button)
