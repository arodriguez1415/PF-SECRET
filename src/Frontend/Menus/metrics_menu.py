from src.Backend.Image_processing_algorithms.Archive_manipulation import dataframe_file_manipulation
from src.Backend.Image_processing_algorithms.Archive_manipulation import video_file_manipulation
from src.Backend.Image_processing_algorithms.Metrics import metrics_generator, metrics_plotter
from src.Backend.Image_processing_algorithms.Metrics.metrics_plotter import filter_keys
from src.Backend.Image_processing_algorithms.Operations.common_operations import resize_image, normalize_to_range
from src.Backend.Video_processing_algorithms.movement_image_generator import create_motion_image
from src.Backend.Video_processing_algorithms.texture_image_generator import classify_single_image, \
    create_texture_image_from_video
from src.Classes.Image_wrapper import Image_wrapper
from src.Classes.Project_mastermind import Project_mastermind
from src.Classes.QDrawable_label import QDrawable_label
from src.Classes.Region import Region
from src.Constants import algorithm_constants, configuration_constants, string_constants
from src.Constants.string_constants import ORIGINAL_TITLE, MOVEMENT_TITLE, TEXTURE_VIDEO_TITLE, TEXTURE_IMAGE_TITLE, \
    FOUR_GRID_COMPARISON
from src.Frontend.Utils import progress_bar
from src.Frontend.Utils.button_controller import disable_button, enable_button
from src.Frontend.Utils.message import show_confirmation_message, show_error, show_wait_message
from src.Frontend.Utils.plot_comparator import plot_four_comparison
from src.Frontend.Utils.viewer_buttons import enable_view_button

def configure_metrics_menu_connections(main_window):
    main_window.generate_metrics_menu_option.triggered.connect(lambda: load_generate_metrics_options(main_window))
    main_window.generate_multiple_cells_metrics_menu_option.triggered.connect(
        lambda: load_generate_multiple_cells_metrics_options(main_window))
    main_window.plot_metrics_menu_option.triggered.connect(lambda: load_plot_metrics_options(main_window))
    main_window.plot_distribution_metric_menu_option.triggered.connect(
        lambda: load_plot_distribution_metrics_option(main_window))

    main_window.analize_texture_and_movement_metrics_menu_option.triggered.connect(
        lambda: load_analyze_texture_and_movement_options(main_window))

    main_window.generate_metrics_load_mask_video_button.clicked.connect(lambda: load_mask_video_path(main_window))
    main_window.generate_multiple_cells_metrics_generate_button.clicked.connect(
        lambda: generate_multiple_cells_metrics(main_window))
    main_window.plot_metrics_load_dataframe_button.clicked.connect(lambda: load_metrics_data_path(main_window))
    main_window.generate_metrics_generate_button.clicked.connect(lambda: generate_metrics(main_window))
    main_window.plot_metrics_generate_button.clicked.connect(lambda: plot_metrics(main_window))
    main_window.plot_metrics_distribution_button.clicked.connect(lambda: plot_distribution_metrics(main_window))
    main_window.analyze_movement_and_texture_button.clicked.connect(
        lambda: analyze_texture_and_movement_metrics(main_window))
    main_window.analyze_movement_and_texture_generate_views_button.clicked.connect(
        lambda: generate_views(main_window))


def load_generate_metrics_options(main_window):
    page = main_window.generate_metrics_options
    stacked_feature_windows = main_window.stacked_feature_windows
    stacked_feature_windows.setCurrentWidget(page)
    return


def load_generate_multiple_cells_metrics_options(main_window):
    page = main_window.generate_multiple_cells_metrics_options
    stacked_feature_windows = main_window.stacked_feature_windows
    stacked_feature_windows.setCurrentWidget(page)
    return


def load_plot_metrics_options(main_window):
    page = main_window.plot_metrics_options
    stacked_feature_windows = main_window.stacked_feature_windows
    stacked_feature_windows.setCurrentWidget(page)
    return


def load_plot_distribution_metrics_option(main_window):
    page = main_window.plot_distribution_metrics_options
    stacked_feature_windows = main_window.stacked_feature_windows
    stacked_feature_windows.setCurrentWidget(page)
    return


def load_analyze_texture_and_movement_options(main_window):
    page = main_window.movement_and_texture_metrics_options
    stacked_feature_windows = main_window.stacked_feature_windows
    stacked_feature_windows.setCurrentWidget(page)

    main_window.analyze_movement_and_texture_movement_threshold_input.setValue(
        main_window.generate_heat_map_threshold_input.value())
    main_window.analyze_movement_and_texture_texture_image_clusters_input.setValue(
        main_window.texture_classification_image_clusters_input.value())
    main_window.analyze_movement_and_texture_texture_video_clusters_input.setValue(
        main_window.texture_classification_video_clusters_input.value())
    main_window.analyze_movement_and_texture_texture_video_threshold_input.setValue(
        main_window.texture_classification_video_threshold_input.value())

    return


def load_mask_video_path(main_window):
    disable_button(main_window.generate_metrics_load_mask_video_button)
    mask_video_path = video_file_manipulation.get_video_path()
    main_window.generate_metrics_mask_video_input.setText(mask_video_path)
    enable_button(main_window.generate_metrics_load_mask_video_button)


def load_metrics_data_path(main_window):
    disable_button(main_window.plot_metrics_load_dataframe_button)
    dataframe_path = dataframe_file_manipulation.get_dataframe_path()
    main_window.plot_metrics_dataframe_input.setText(dataframe_path)
    enable_button(main_window.plot_metrics_load_dataframe_button)


def generate_metrics(main_window):
    disable_button(main_window.generate_metrics_generate_button)
    mask_video_path = main_window.generate_metrics_mask_video_input.text()
    metrics_dictionary = get_generation_metrics_dictionary(main_window)

    if len(filter_keys(metrics_dictionary)) == 0:
        enable_button(main_window.generate_metrics_generate_button)
        return

    metrics_generator.generate_metrics(mask_video_path, metrics_dictionary)
    progress_bar.force_to_close()
    enable_button(main_window.generate_metrics_generate_button)


def get_generation_metrics_dictionary(main_window):
    metrics_dictionary = {}

    is_perimeter_checked = main_window.generate_metrics_perimeter_checkbox.isChecked()
    metrics_dictionary[algorithm_constants.PERIMETER_METRIC] = is_perimeter_checked

    is_area_checked = main_window.generate_metrics_area_checkbox.isChecked()
    metrics_dictionary[algorithm_constants.AREA_METRIC] = is_area_checked

    is_axis_rate_checked = main_window.generate_metrics_axis_rate_checkbox.isChecked()
    metrics_dictionary[algorithm_constants.AXIS_RATE_METRIC] = is_axis_rate_checked

    return metrics_dictionary


def generate_multiple_cells_metrics(main_window):
    disable_button(main_window.generate_multiple_cells_metrics_generate_button)
    mask_videos_path_list = video_file_manipulation.get_multiple_videos_path()
    metrics_dictionary = get_generation_multiple_cells_metrics_dictionary(main_window)

    if len(filter_keys(metrics_dictionary)) == 0:
        enable_button(main_window.generate_metrics_generate_button)
        return

    metrics_generator.generate_multiple_cells_metrics(mask_videos_path_list, metrics_dictionary)
    progress_bar.force_to_close()
    enable_button(main_window.generate_multiple_cells_metrics_generate_button)


def get_generation_multiple_cells_metrics_dictionary(main_window):
    metrics_dictionary = {}

    is_perimeter_checked = main_window.generate_multiple_cells_metrics_perimeter_checkbox.isChecked()
    metrics_dictionary[algorithm_constants.PERIMETER_METRIC] = is_perimeter_checked

    is_area_checked = main_window.generate_multiple_cells_metrics_area_checkbox.isChecked()
    metrics_dictionary[algorithm_constants.AREA_METRIC] = is_area_checked

    is_axis_rate_checked = main_window.generate_multiple_cells_metrics_axis_rate_checkbox.isChecked()
    metrics_dictionary[algorithm_constants.AXIS_RATE_METRIC] = is_axis_rate_checked

    return metrics_dictionary


def plot_metrics(main_window):
    disable_button(main_window.plot_metrics_generate_button)
    metrics_data_path = main_window.plot_metrics_dataframe_input.text()
    metrics_dictionary = get_plotting_metrics_dictionary(main_window)

    if len(filter_keys(metrics_dictionary)) == 0:
        enable_button(main_window.plot_metrics_generate_button)
        return

    metrics_values_lists, frames_values_lists, titles_list, x_label_list, y_label_list = metrics_plotter.load_metrics(
        metrics_data_path, metrics_dictionary)
    metrics_plotter.plot_metrics(metrics_values_lists, frames_values_lists, titles_list, x_label_list, y_label_list)
    enable_button(main_window.plot_metrics_generate_button)


def get_plotting_metrics_dictionary(main_window):
    metrics_dictionary = {}

    is_perimeter_checked = main_window.plot_metrics_perimeter_checkbox.isChecked()
    metrics_dictionary[algorithm_constants.PERIMETER_METRIC] = is_perimeter_checked

    is_area_checked = main_window.plot_metrics_area_checkbox.isChecked()
    metrics_dictionary[algorithm_constants.AREA_METRIC] = is_area_checked

    is_axis_rate_checked = main_window.plot_metrics_axis_rate_checkbox.isChecked()
    metrics_dictionary[algorithm_constants.AXIS_RATE_METRIC] = is_axis_rate_checked

    return metrics_dictionary


def plot_distribution_metrics(main_window):
    disable_button(main_window.plot_metrics_distribution_button)
    metrics_data_paths = dataframe_file_manipulation.get_multiple_dataframes_path()
    distribution_metrics_dictionary = get_plotting_distribution_metrics_dictionary(main_window)

    if len(filter_keys(distribution_metrics_dictionary)) == 0:
        enable_button(main_window.plot_metrics_distribution_button)
        return

    metrics_avg_lists, titles_list, x_label_list, y_label_list = metrics_plotter.load_distribution_metrics(
        metrics_data_paths, distribution_metrics_dictionary)
    metrics_plotter.plot_distribution_metrics(metrics_avg_lists, titles_list, x_label_list, y_label_list)
    enable_button(main_window.plot_metrics_distribution_button)


def get_plotting_distribution_metrics_dictionary(main_window):
    metrics_dictionary = {}

    is_perimeter_checked = main_window.plot_metrics_distribution_perimeter_checkbox.isChecked()
    metrics_dictionary[algorithm_constants.PERIMETER_METRIC] = is_perimeter_checked

    is_area_checked = main_window.plot_metrics_distribution_area_checkbox.isChecked()
    metrics_dictionary[algorithm_constants.AREA_METRIC] = is_area_checked

    is_axis_rate_checked = main_window.plot_metrics_distribution_axis_rate_checkbox.isChecked()
    metrics_dictionary[algorithm_constants.AXIS_RATE_METRIC] = is_axis_rate_checked

    return metrics_dictionary


def generate_views(main_window):
    disable_button(main_window.analyze_movement_and_texture_generate_views_button)
    generate_movement_view(main_window)
    generate_image_texture_view(main_window)
    generate_video_texture_view(main_window)

    enable_button(main_window.analyze_movement_and_texture_generate_views_button)


def generate_movement_view(main_window):
    project_mastermind = Project_mastermind.get_instance()
    threshold_value = main_window.analyze_movement_and_texture_movement_threshold_input.value()
    uncolored_motion_image_array, uncolored_motion_image_array_normalized, coloured_motion_image_array = create_motion_image(
        threshold_value)
    movement_normalized_image_wrapper = Image_wrapper(uncolored_motion_image_array_normalized, "")
    movement_image_wrapper = Image_wrapper(uncolored_motion_image_array, "")
    movement_heat_map_image_wrapper = Image_wrapper(coloured_motion_image_array, "")
    project_mastermind.set_normalized_movement_image(movement_normalized_image_wrapper)
    project_mastermind.set_movement_image(movement_image_wrapper)
    project_mastermind.set_movement_heat_map_image(movement_heat_map_image_wrapper)
    progress_bar.force_to_close()
    enable_view_button(string_constants.MOVEMENT_VIEW)


def generate_image_texture_view(main_window):
    project_mastermind = Project_mastermind.get_instance()
    current_image_array = project_mastermind.get_last_image()
    clusters_quantity = main_window.analyze_movement_and_texture_texture_image_clusters_input.value()
    message_box = show_wait_message(string_constants.WAIT_TEXTURE_IMAGE_MESSAGE_TITLE,
                                    string_constants.WAIT_TEXTURE_IMAGE_MESSAGE_DESC)
    uncoloured_classified_image, coloured_classified_image = classify_single_image(current_image_array,
                                                                                   clusters_quantity=clusters_quantity)
    message_box.done(0)
    texture_image_wrapper = Image_wrapper(uncoloured_classified_image)
    texture_heat_map_image_wrapper = Image_wrapper(coloured_classified_image)
    project_mastermind.set_texture_image(texture_image_wrapper)
    project_mastermind.set_texture_heat_map_image(texture_heat_map_image_wrapper)
    progress_bar.force_to_close()
    enable_view_button(string_constants.TEXTURE_IMAGE_VIEW)


def generate_video_texture_view(main_window):
    project_mastermind = Project_mastermind.get_instance()
    clusters_quantity = main_window.analyze_movement_and_texture_texture_video_clusters_input.value()
    threshold = main_window.analyze_movement_and_texture_texture_video_threshold_input.value()
    uncoloured_classified_image, coloured_classified_image = create_texture_image_from_video(
        clusters_quantity=clusters_quantity,
        threshold=threshold)
    texture_image_wrapper = Image_wrapper(uncoloured_classified_image)
    texture_heat_map_image_wrapper = Image_wrapper(coloured_classified_image)
    project_mastermind.set_texture_image_video(texture_image_wrapper)
    project_mastermind.set_texture_heat_map_image_video(texture_heat_map_image_wrapper)
    progress_bar.force_to_close()
    enable_view_button(string_constants.TEXTURE_VIDEO_VIEW)


def analyze_texture_and_movement_metrics(main_window):
    disable_button(main_window.analyze_movement_and_texture_button)
    project_mastermind = Project_mastermind.get_instance()
    movement_avg_index = 1
    region = Region()

    if not region.has_region():
        continue_flag = show_confirmation_message(string_constants.NO_REGION_FOUND_TITLE,
                                                  string_constants.NO_REGION_FOUND_DESCRIPTION)
        if not continue_flag:
            enable_button(main_window.analyze_movement_and_texture_button)
            return

    if not all_images_ready():
        show_error(string_constants.NO_ALL_IMAGES_READY_FOR_ANALYZE_METRIC_DESCRIPTION)
        enable_button(main_window.analyze_movement_and_texture_button)
        return

    original_array = project_mastermind.get_original_image()
    movement_array = project_mastermind.get_normalized_movement_wrapper().image_array
    texture_image_array = project_mastermind.get_texture_image().image_array
    texture_video_array = project_mastermind.get_texture_image_video().image_array

    show_movement_array = project_mastermind.get_movement_heat_map_image().image_array
    show_texture_image_array = project_mastermind.get_texture_heat_map_image().image_array
    show_texture_video_array = project_mastermind.get_texture_heat_map_image_video().image_array

    movement_weight_array = project_mastermind.get_movement_image().image_array

    width, height = configuration_constants.IMAGE_VIEWER_WIDTH, configuration_constants.IMAGE_VIEWER_HEIGHT
    weight_image_array_list = [original_array, movement_weight_array, texture_image_array, texture_video_array]
    show_images_array_list = [original_array, show_movement_array, show_texture_image_array, show_texture_video_array]
    avg_values_array = []

    square_region = region.get_region()
    for i in range(0, len(weight_image_array_list)):
        show_image_array = resize_image(show_images_array_list[i], width, height)
        weight_image_array = resize_image(weight_image_array_list[i], width, height)
        pixels_in_region = region.get_pixels_in_region(weight_image_array)
        if i != movement_avg_index:
            normalized_pixels_in_region = normalize_to_range(pixels_in_region, max_value=255)
            avg_values_array.append(normalized_pixels_in_region.mean())
        else:
            avg_values_array.append(pixels_in_region.mean())
        show_images_array_list[i] = QDrawable_label.draw_region_in_image(show_image_array, square_region)

    avg_results = []
    avg_results.append("Promedio de valor de pixel escala grises: " + str(round(avg_values_array[0], 2)))
    avg_results.append("Promedio de valor de pixel de movimiento: " + str(round(avg_values_array[1], 2)))
    avg_results.append("Promedio de valor de pixel de textura de imagen: " + str(round(avg_values_array[2], 2)))
    avg_results.append("Promedio de valor de pixel de textura de video: " + str(round(avg_values_array[3], 2)))

    title = FOUR_GRID_COMPARISON
    sub_titles = [ORIGINAL_TITLE, MOVEMENT_TITLE, TEXTURE_IMAGE_TITLE, TEXTURE_VIDEO_TITLE]
    plot_four_comparison(show_images_array_list, movement_weight_array, title, sub_titles, avg_results)
    enable_button(main_window.analyze_movement_and_texture_button)


def all_images_ready():
    pm = Project_mastermind.get_instance()
    if pm.get_original_image() is None or pm.get_movement_image() is None or pm.get_texture_heat_map_image() is None or pm.get_texture_heat_map_image_video() is None:
        return False
    return True
