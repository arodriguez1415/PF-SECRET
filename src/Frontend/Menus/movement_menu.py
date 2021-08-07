from src.Backend.Image_processing_algorithms.Operations.common_operations import show_coloured_image
from src.Backend.Video_processing_algorithms.movement_image_generator import create_motion_image
from src.Classes.Image_wrapper import Image_wrapper
from src.Classes.Project_mastermind import Project_mastermind
from src.Constants import string_constants
from src.Frontend.Utils.button_controller import disable_button, enable_button
from src.Frontend.Utils.viewer_buttons import enable_view_button


def configure_movement_menu_connections(main_window):
    main_window.generate_heat_map_menu_option.triggered. \
        connect(lambda: load_heat_map_options(main_window))

    main_window.generate_heat_map_button.clicked. \
        connect(lambda: generate_heat_map(main_window))


def load_heat_map_options(main_window):
    page = main_window.heat_map_options
    stacked_feature_windows = main_window.stacked_feature_windows
    stacked_feature_windows.setCurrentWidget(page)
    return


def generate_heat_map(main_window):
    disable_button(main_window.generate_heat_map_button)
    project_mastermind = Project_mastermind.get_instance()
    threshold_value = main_window.generate_heat_map_threshold_input.value()
    uncolored_motion_image_array, coloured_motion_image_array = create_motion_image(threshold_value)
    movement_heat_map_image_wrapper = Image_wrapper(coloured_motion_image_array, "")
    movement_image_wrapper = Image_wrapper(uncolored_motion_image_array, "")
    project_mastermind.set_movement_heat_map_image(movement_heat_map_image_wrapper)
    project_mastermind.set_movement_image(movement_image_wrapper)
    show_coloured_image(coloured_motion_image_array)
    main_window.image_viewer.set_screen_image(movement_heat_map_image_wrapper)
    enable_button(main_window.generate_heat_map_button)
    enable_view_button(string_constants.MOVEMENT_VIEW)