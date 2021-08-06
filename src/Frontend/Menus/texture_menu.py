from src.Backend.Image_processing_algorithms.Operations.common_operations import show_coloured_image
from src.Backend.Image_processing_algorithms.Texture import fractal_dimention
from src.Backend.Image_processing_algorithms.Texture import profile_texture
from src.Backend.Image_processing_algorithms.Texture import texture_heatmap
from src.Backend.Video_processing_algorithms.texture_image_generator import create_texture_image_from_video, classify_single_image
from src.Classes.Image_wrapper import Image_wrapper
from src.Classes.Project_mastermind import Project_mastermind
from src.Classes.Region import Region
from src.Constants import string_constants
from src.Frontend.Utils.message import show_wait_message


def configure_texture_menu_connections(main_window):
    main_window.lbp_menu_option.triggered.connect(lambda: lbp_options(main_window))
    main_window.fractal_dimension_menu_option.triggered.connect(lambda: fractal_dimension_options(main_window))
    main_window.texture_profile_menu_option.triggered.connect(lambda: texture_profile_options(main_window))
    main_window.texture_classification_menu_option.triggered.connect(
        lambda: texture_classification_options(main_window))

    main_window.fractal_dimension_apply_button.clicked.connect(lambda: generate_fractal_dimension(main_window))
    main_window.texture_profile_apply_button.clicked.connect(lambda: generate_profile_texture())
    main_window.texture_heatmap_apply_button.clicked.connect(lambda: generate_heatmap())

    main_window.texture_classification_image_button.clicked.connect(lambda: classify_image_texture(main_window))
    main_window.texture_classification_video_button.clicked.connect(lambda: classify_video_texture(main_window))


def lbp_options(main_window):
    page = main_window.lbp_options
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


def texture_heatmap_options(main_window):
    page = main_window.texture_heatmap_options
    stacked_feature_windows = main_window.stacked_feature_windows
    stacked_feature_windows.setCurrentWidget(page)
    return


def texture_classification_options(main_window):
    page = main_window.texture_classification_options
    stacked_feature_windows = main_window.stacked_feature_windows
    stacked_feature_windows.setCurrentWidget(page)
    return


def generate_fractal_dimension(main_window):
    project_mastermind = Project_mastermind.get_instance()
    current_image_array = project_mastermind.get_last_image()
    method = main_window.fractal_dimension_function_combobox.currentText()

    fractal_dimension_image = fractal_dimention.fractal_dimension_texture(current_image_array, method)
    image_wrapper = Image_wrapper(fractal_dimension_image)
    main_window.image_viewer.set_screen_image(image_wrapper)


def generate_profile_texture():
    project_mastermind = Project_mastermind.get_instance()
    current_image_array = project_mastermind.get_last_image()

    line_region = Region()
    profile_texture.fractal_dimension_line(current_image_array, line_region.get_region())


def generate_heatmap():
    project_mastermind = Project_mastermind.get_instance()
    current_image_array = project_mastermind.get_last_image()

    texture_heatmap.texture_heatmap(current_image_array)


def classify_image_texture(main_window):
    main_window.texture_classification_image_button.setDisabled(True)
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
    main_window.texture_classification_image_button.setDisabled(False)


def classify_video_texture(main_window):
    project_mastermind = Project_mastermind.get_instance()
    clusters_quantity = main_window.texture_classification_video_clusters_input.value()
    threshold = main_window.texture_classification_video_threshold_input.value()
    uncoloured_classified_image, coloured_classified_image = create_texture_image_from_video(clusters_quantity=clusters_quantity,
                                                                                             threshold=threshold)
    show_coloured_image(coloured_classified_image)
    texture_image_wrapper = Image_wrapper(uncoloured_classified_image)
    texture_heat_map_image_wrapper = Image_wrapper(coloured_classified_image)
    project_mastermind.set_texture_image_video(texture_image_wrapper)
    project_mastermind.set_texture_heat_map_image_video(texture_heat_map_image_wrapper)
    main_window.image_viewer.set_screen_image(texture_heat_map_image_wrapper)