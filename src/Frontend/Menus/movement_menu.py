from src.Backend.Video_processing_algorithms.movement_from_frames import create_motion_image
from src.Classes.Image_wrapper import Image_wrapper


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
    threshold_value = main_window.generate_heat_map_threshold_input.value()
    uncolored_motion_image_array, coloured_motion_image_array = create_motion_image(threshold_value)
    image_wrapper = Image_wrapper(coloured_motion_image_array, "")
    main_window.image_viewer.set_screen_image(image_wrapper)