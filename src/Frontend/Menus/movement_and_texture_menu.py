from src.Backend.Image_processing_algorithms.Archive_manipulation.properties_manipulation import \
    save_video_texture_params, save_image_texture_params, save_movement_params
from src.Backend.Image_processing_algorithms.Operations.common_operations import show_coloured_image, resize_image
from src.Backend.Image_processing_algorithms.Texture import fractal_dimention
from src.Backend.Image_processing_algorithms.Texture import profile_texture
from src.Backend.Image_processing_algorithms.Texture import texture_heatmap
from src.Backend.Video_processing_algorithms.movement_image_generator import create_motion_image
from src.Backend.Video_processing_algorithms.texture_image_generator import create_texture_image_from_video, \
    classify_single_image
from src.Classes.Image_wrapper import Image_wrapper
from src.Classes.Project_mastermind import Project_mastermind
from src.Classes.Region import Region
from src.Constants import string_constants, configuration_constants
from src.Frontend.Utils import progress_bar
from src.Frontend.Utils.button_controller import disable_button, enable_button
from src.Frontend.Utils.message import show_wait_message, show_error
from src.Frontend.Utils.viewer_buttons import enable_view_button


def configure_texture_menu_connections(main_window):
    main_window.texture_and_movement_generate_movement_heat_map_menu_option.triggered.connect(
        lambda: load_heat_map_options(main_window))
    main_window.texture_and_movement_generate_profile_menu_option.triggered.connect(
        lambda: texture_profile_options(main_window))
    main_window.texture_and_movement_generate_texture_heat_map_menu_option.triggered.connect(
        lambda: texture_classification_options(main_window))

    main_window.generate_heat_map_button.clicked.connect(lambda: generate_heat_map(main_window))
    main_window.texture_profile_apply_button.clicked.connect(lambda: generate_profile_texture(main_window))
    main_window.texture_classification_image_button.clicked.connect(lambda: classify_image_texture(main_window))
    main_window.texture_classification_video_button.clicked.connect(lambda: classify_video_texture(main_window))


def load_heat_map_options(main_window):
    page = main_window.heat_map_options
    stacked_feature_windows = main_window.stacked_feature_windows
    stacked_feature_windows.setCurrentWidget(page)
    return


def fractal_dimension_options(main_window):
    page = main_window.fractal_dimension_options
    stacked_feature_windows = main_window.stacked_feature_windows
    stacked_feature_windows.setCurrentWidget(page)
    return


def texture_profile_options(main_window):
    page = main_window.texture_profile_options
    stacked_feature_windows = main_window.stacked_feature_windows
    stacked_feature_windows.setCurrentWidget(page)
    return


def texture_classification_options(main_window):
    page = main_window.texture_classification_options
    stacked_feature_windows = main_window.stacked_feature_windows
    stacked_feature_windows.setCurrentWidget(page)
    return


def generate_heat_map(main_window):
    disable_button(main_window.generate_heat_map_button)
    project_mastermind = Project_mastermind.get_instance()
    threshold_value = main_window.generate_heat_map_threshold_input.value()
    uncolored_motion_image_array, uncolored_motion_image_array_normalized, coloured_motion_image_array = create_motion_image(threshold_value)
    movement_normalized_image_wrapper = Image_wrapper(uncolored_motion_image_array_normalized, "")
    movement_image_wrapper = Image_wrapper(uncolored_motion_image_array, "")
    movement_heat_map_image_wrapper = Image_wrapper(coloured_motion_image_array, "")
    project_mastermind.set_normalized_movement_image(movement_normalized_image_wrapper)
    project_mastermind.set_movement_image(movement_image_wrapper)
    project_mastermind.set_movement_heat_map_image(movement_heat_map_image_wrapper)
    show_coloured_image(coloured_motion_image_array)
    main_window.image_viewer.set_screen_image(movement_heat_map_image_wrapper)
    progress_bar.force_to_close()
    save_movement_params(main_window)
    enable_button(main_window.generate_heat_map_button)
    enable_view_button(string_constants.MOVEMENT_VIEW)


def generate_fractal_dimension(main_window):
    disable_button(main_window.fractal_dimension_apply_button)
    project_mastermind = Project_mastermind.get_instance()
    current_image_array = project_mastermind.get_last_image()
    method = main_window.fractal_dimension_function_combobox.currentText()

    fractal_dimension_image = fractal_dimention.fractal_dimension_texture(current_image_array, method)
    image_wrapper = Image_wrapper(fractal_dimension_image)
    main_window.image_viewer.set_screen_image(image_wrapper)
    enable_button(main_window.fractal_dimension_apply_button)


def generate_profile_texture(main_window):
    disable_button(main_window.texture_profile_apply_button)
    project_mastermind = Project_mastermind.get_instance()
    width, height = configuration_constants.IMAGE_VIEWER_WIDTH, configuration_constants.IMAGE_VIEWER_HEIGHT
    current_image_array = project_mastermind.get_last_image()
    current_image_array = resize_image(current_image_array, width, height)
    line_region = Region()
    if not line_region.has_region():
        show_error(string_constants.NO_PROFILE_SELECTED_ERROR)
    else:
        try:
            line = line_region.get_line()
            profile_texture.fractal_dimension_line(current_image_array, line)
        except ValueError:
            show_error(string_constants.NO_LINE_SELECTED_ERROR)
    enable_button(main_window.texture_profile_apply_button)


def classify_image_texture(main_window):
    disable_button(main_window.texture_classification_image_button)
    project_mastermind = Project_mastermind.get_instance()
    current_image_array = project_mastermind.get_last_image()
    clusters_quantity = main_window.texture_classification_image_clusters_input.value()
    message_box = show_wait_message(string_constants.WAIT_TEXTURE_IMAGE_MESSAGE_TITLE,
                                    string_constants.WAIT_TEXTURE_IMAGE_MESSAGE_DESC)
    uncoloured_classified_image, coloured_classified_image = classify_single_image(current_image_array,
                                                                                   clusters_quantity=clusters_quantity)
    message_box.done(0)
    show_coloured_image(coloured_classified_image)
    texture_image_wrapper = Image_wrapper(uncoloured_classified_image)
    texture_heat_map_image_wrapper = Image_wrapper(coloured_classified_image)
    project_mastermind.set_texture_image(texture_image_wrapper)
    project_mastermind.set_texture_heat_map_image(texture_heat_map_image_wrapper)
    main_window.image_viewer.set_screen_image(texture_heat_map_image_wrapper)
    progress_bar.force_to_close()
    save_image_texture_params(main_window)
    enable_button(main_window.texture_classification_image_button)
    enable_view_button(string_constants.TEXTURE_IMAGE_VIEW)


def classify_video_texture(main_window):
    disable_button(main_window.texture_classification_video_button)
    project_mastermind = Project_mastermind.get_instance()
    clusters_quantity = main_window.texture_classification_video_clusters_input.value()
    threshold = main_window.texture_classification_video_threshold_input.value()
    uncoloured_classified_image, coloured_classified_image = create_texture_image_from_video(
        clusters_quantity=clusters_quantity,
        threshold=threshold)
    show_coloured_image(coloured_classified_image)
    texture_image_wrapper = Image_wrapper(uncoloured_classified_image)
    texture_heat_map_image_wrapper = Image_wrapper(coloured_classified_image)
    project_mastermind.set_texture_image_video(texture_image_wrapper)
    project_mastermind.set_texture_heat_map_image_video(texture_heat_map_image_wrapper)
    main_window.image_viewer.set_screen_image(texture_heat_map_image_wrapper)
    progress_bar.force_to_close()
    save_video_texture_params(main_window)
    enable_button(main_window.texture_classification_video_button)
    enable_view_button(string_constants.TEXTURE_VIDEO_VIEW)
