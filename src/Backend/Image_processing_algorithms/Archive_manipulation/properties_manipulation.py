import os
import pickle

from src.Backend.Image_processing_algorithms.Preprocessing import adaptive_threshold
from src.Backend.Image_processing_algorithms.Preprocessing.adaptive_threshold import get_text_method
from src.Classes.Project_mastermind import Project_mastermind
from src.Constants import configuration_constants
from src.Constants import properties_constants as ps


def save_properties(dictionary):
    with open(configuration_constants.PROPERTIES_FILE_PATH, 'wb') as file:
        pickle.dump(dictionary, file, pickle.HIGHEST_PROTOCOL)


def load_properties(main_window, global_routine_params):
    if not os.path.exists(configuration_constants.PROPERTIES_FILE_PATH):
        dictionary = generate_default_properties()
        save_properties(dictionary)
    with open(configuration_constants.PROPERTIES_FILE_PATH, 'rb') as file:
        dictionary = pickle.load(file)

    set_properties(dictionary, main_window, global_routine_params)
    return dictionary


def generate_default_properties():
    default_properties_dict = {ps.IMAGES_SOURCE_FOLDER: configuration_constants.TEST_IMAGES_DIR}

    default_properties_dict[ps.ADAPTIVE_THRESHOLD_WINDOW_SIZE] = ps.ADAPTIVE_THRESHOLD_WINDOW_SIZE_VALUE
    default_properties_dict[ps.ADAPTIVE_THRESHOLD_C_CONSTANT] = ps.ADAPTIVE_THRESHOLD_C_CONSTANT_VALUE
    default_properties_dict[ps.ADAPTIVE_THRESHOLD_METHOD] = ps.ADAPTIVE_THRESHOLD_METHOD_VALUE

    default_properties_dict[ps.MGAC_ITERATIONS] = ps.MGAC_ITERATIONS_VALUE
    default_properties_dict[ps.MGAC_THRESHOLD] = ps.MGAC_THRESHOLD_VALUE
    default_properties_dict[ps.MGAC_SMOOTHING] = ps.MGAC_SMOOTHING_VALUE
    default_properties_dict[ps.MGAC_BALLOON] = ps.MGAC_BALLOON_VALUE
    default_properties_dict[ps.MGAC_ALPHA] = ps.MGAC_ALPHA_VALUE
    default_properties_dict[ps.MGAC_SIGMA] = ps.MGAC_SIGMA_VALUE

    default_properties_dict[ps.TEXTURE_IMAGE_CLUSTERS] = ps.TEXTURE_IMAGE_CLUSTERS_VALUE
    default_properties_dict[ps.TEXTURE_VIDEO_THRESHOLD] = ps.TEXTURE_VIDEO_THRESHOLD_VALUE
    default_properties_dict[ps.TEXTURE_VIDEO_CLUSTERS] = ps.TEXTURE_VIDEO_CLUSTERS_VALUE

    default_properties_dict[ps.TEXTURE_MOVEMENT_THRESHOLD] = ps.TEXTURE_MOVEMENT_THRESHOLD_VALUE

    default_properties_dict[ps.GLOBAL_ROUTINE_ANISOTROPIC_FILTER_TIMES] = ps.GLOBAL_ROUTINE_ANISOTROPIC_FILTER_TIMES_VALUE

    default_properties_dict[ps.GLOBAL_ROUTINE_ADAPTIVE_THRESHOLD_WINDOW_SIZE] = ps.GLOBAL_ROUTINE_ADAPTIVE_THRESHOLD_WINDOW_SIZE_VALUE
    default_properties_dict[ps.GLOBAL_ROUTINE_ADAPTIVE_C_CONSTANT] = ps.GLOBAL_ROUTINE_ADAPTIVE_C_CONSTANT_VALUE
    default_properties_dict[ps.GLOBAL_ROUTINE_ADAPTIVE_METHOD] = ps.GLOBAL_ROUTINE_ADAPTIVE_METHOD_VALUE

    default_properties_dict[ps.GLOBAL_ROUTINE_MGAC_ITERATIONS] = ps.GLOBAL_ROUTINE_MGAC_ITERATIONS_VALUE
    default_properties_dict[ps.GLOBAL_ROUTINE_MGAC_THRESHOLD] = ps.GLOBAL_ROUTINE_MGAC_THRESHOLD_VALUE
    default_properties_dict[ps.GLOBAL_ROUTINE_MGAC_SMOOTHING] = ps.GLOBAL_ROUTINE_MGAC_SMOOTHING_VALUE
    default_properties_dict[ps.GLOBAL_ROUTINE_MGAC_BALLOON] = ps.GLOBAL_ROUTINE_MGAC_BALLOON_VALUE
    default_properties_dict[ps.GLOBAL_ROUTINE_MGAC_ALPHA] = ps.GLOBAL_ROUTINE_MGAC_ALPHA_VALUE
    default_properties_dict[ps.GLOBAL_ROUTINE_MGAC_SIGMA] = ps.GLOBAL_ROUTINE_MGAC_SIGMA_VALUE

    default_properties_dict[ps.GLOBAL_ROUTINE_MOVEMENT_THRESHOLD] = ps.GLOBAL_ROUTINE_MOVEMENT_THRESHOLD_VALUE

    default_properties_dict[ps.GLOBAL_ROUTINE_TEXTURE_THRESHOLD] = ps.GLOBAL_ROUTINE_TEXTURE_THRESHOLD_VALUE
    default_properties_dict[ps.GLOBAL_ROUTINE_TEXTURE_CLUSTERS] = ps.GLOBAL_ROUTINE_TEXTURE_CLUSTERS_VALUE

    return default_properties_dict


def transform_dict(prop_dict):
    for key in prop_dict.keys():
        value_string = str(prop_dict[key])
        if value_string.isnumeric():
            prop_dict[key] = int(prop_dict[key])
        elif is_double(value_string):
            prop_dict[key] = float(prop_dict[key])

    return prop_dict


def is_double(potential_float):
    try:
        float(potential_float)
        return True
    except ValueError:
        return False


def set_properties(prop_dict, main_window, global_routine_params):
    prop_dict = transform_dict(prop_dict)

    set_adaptive_threshold_params(prop_dict, main_window)
    set_mgac_params(prop_dict, main_window)
    set_texture_params(prop_dict, main_window)
    set_movement_params(prop_dict, main_window)

    set_global_routine_params(prop_dict, global_routine_params)


def set_adaptive_threshold_params(prop_dict, main_window):
    main_window.adaptive_threshold_window_size_spinner.setValue(prop_dict[ps.ADAPTIVE_THRESHOLD_WINDOW_SIZE])
    main_window.adaptive_threshold_c_constant_spinner.setValue(prop_dict[ps.ADAPTIVE_THRESHOLD_C_CONSTANT])
    main_window.adaptive_threshold_method_box.setCurrentText(get_text_method(prop_dict[ps.ADAPTIVE_THRESHOLD_METHOD]))


def set_mgac_params(prop_dict, main_window):
    main_window.iterations_mgac_input.setValue(prop_dict[ps.MGAC_ITERATIONS])
    main_window.threshold_mgac_input.setValue(prop_dict[ps.MGAC_THRESHOLD])
    main_window.smoothing_mgac_input.setValue(prop_dict[ps.MGAC_SMOOTHING])
    main_window.balloon_mgac_input.setValue(prop_dict[ps.MGAC_BALLOON])
    main_window.alpha_mgac_input.setValue(prop_dict[ps.MGAC_ALPHA])
    main_window.sigma_mgac_input.setValue(prop_dict[ps.MGAC_SIGMA])


def set_texture_params(prop_dict, main_window):
    main_window.texture_classification_image_clusters_input.setValue(prop_dict[ps.TEXTURE_IMAGE_CLUSTERS])
    main_window.texture_classification_video_clusters_input.setValue(prop_dict[ps.TEXTURE_VIDEO_CLUSTERS])
    main_window.texture_classification_video_threshold_input.setValue(prop_dict[ps.TEXTURE_VIDEO_THRESHOLD])


def set_movement_params(prop_dict, main_window):
    main_window.generate_heat_map_threshold_input.setValue(prop_dict[ps.TEXTURE_MOVEMENT_THRESHOLD])


def set_global_routine_params(prop_dict, global_routine_params):
    global_routine_params.global_routine_params_anisotropic_filter_times_input.setValue(
        prop_dict[ps.GLOBAL_ROUTINE_ANISOTROPIC_FILTER_TIMES])

    global_routine_params.global_routine_params_adaptive_threshold_window_size_input.setValue(
        prop_dict[ps.GLOBAL_ROUTINE_ADAPTIVE_THRESHOLD_WINDOW_SIZE])
    global_routine_params.global_routine_params_adaptive_threshold_c_constant_input.setValue(
        prop_dict[ps.GLOBAL_ROUTINE_ADAPTIVE_C_CONSTANT])
    global_routine_params.global_routine_params_adaptive_threshold_method_box.setCurrentText(
        get_text_method(prop_dict[ps.GLOBAL_ROUTINE_ADAPTIVE_METHOD]))

    global_routine_params.global_routine_params_mgac_iterations_input.setValue(
        prop_dict[ps.GLOBAL_ROUTINE_MGAC_ITERATIONS])
    global_routine_params.global_routine_params_mgac_threshold_input.setValue(
        prop_dict[ps.GLOBAL_ROUTINE_MGAC_THRESHOLD])
    global_routine_params.global_routine_params_mgac_smoothing_input.setValue(
        prop_dict[ps.GLOBAL_ROUTINE_MGAC_SMOOTHING])
    global_routine_params.global_routine_params_mgac_balloon_input.setValue(prop_dict[ps.GLOBAL_ROUTINE_MGAC_BALLOON])
    global_routine_params.global_routine_params_mgac_alpha_input.setValue(prop_dict[ps.GLOBAL_ROUTINE_MGAC_ALPHA])
    global_routine_params.global_routine_params_mgac_sigma_input.setValue(prop_dict[ps.GLOBAL_ROUTINE_MGAC_SIGMA])

    global_routine_params.global_routine_params_movement_threshold_input.setValue(
        prop_dict[ps.GLOBAL_ROUTINE_MOVEMENT_THRESHOLD])

    global_routine_params.global_routine_params_movement_texture_clusters_input.setValue(
        prop_dict[ps.GLOBAL_ROUTINE_TEXTURE_CLUSTERS])
    global_routine_params.global_routine_params_movement_texture_threshold_input.setValue(
        prop_dict[ps.GLOBAL_ROUTINE_TEXTURE_THRESHOLD])


def save_adaptive_threshold_params(main_window):
    project_mastermind = Project_mastermind.get_instance()
    prop_dict = project_mastermind.get_properties_dictionary()

    prop_dict[ps.ADAPTIVE_THRESHOLD_WINDOW_SIZE] = main_window.adaptive_threshold_window_size_spinner.value()
    prop_dict[ps.ADAPTIVE_THRESHOLD_C_CONSTANT] = main_window.adaptive_threshold_c_constant_spinner.value()
    prop_dict[ps.ADAPTIVE_THRESHOLD_METHOD] = int(adaptive_threshold.get_method(main_window.adaptive_threshold_method_box.currentText()))

    project_mastermind.reload_properties(prop_dict)
    save_properties(prop_dict)


def save_mgac_params(main_window):
    project_mastermind = Project_mastermind.get_instance()
    prop_dict = project_mastermind.get_properties_dictionary()

    prop_dict[ps.MGAC_ITERATIONS] = main_window.iterations_mgac_input.value()
    prop_dict[ps.MGAC_THRESHOLD] = main_window.threshold_mgac_input.value()
    prop_dict[ps.MGAC_SMOOTHING] = main_window.smoothing_mgac_input.value()
    prop_dict[ps.MGAC_BALLOON] = main_window.balloon_mgac_input.value()
    prop_dict[ps.MGAC_ALPHA] = main_window.alpha_mgac_input.value()
    prop_dict[ps.MGAC_SIGMA] = main_window.sigma_mgac_input.value()

    project_mastermind.reload_properties(prop_dict)
    save_properties(prop_dict)


def save_image_texture_params(main_window):
    project_mastermind = Project_mastermind.get_instance()
    prop_dict = project_mastermind.get_properties_dictionary()

    prop_dict[ps.TEXTURE_IMAGE_CLUSTERS] = main_window.texture_classification_image_clusters_input.value()

    project_mastermind.reload_properties(prop_dict)
    save_properties(prop_dict)


def save_video_texture_params(main_window):
    project_mastermind = Project_mastermind.get_instance()
    prop_dict = project_mastermind.get_properties_dictionary()

    prop_dict[ps.TEXTURE_VIDEO_THRESHOLD] = main_window.texture_classification_video_clusters_input.value()
    prop_dict[ps.TEXTURE_VIDEO_CLUSTERS] = main_window.texture_classification_video_threshold_input.value()

    project_mastermind.reload_properties(prop_dict)
    save_properties(prop_dict)


def save_movement_params(main_window):
    project_mastermind = Project_mastermind.get_instance()
    prop_dict = project_mastermind.get_properties_dictionary()

    prop_dict[ps.TEXTURE_MOVEMENT_THRESHOLD] = main_window.generate_heat_map_threshold_input.value()

    project_mastermind.reload_properties(prop_dict)
    save_properties(prop_dict)


def save_global_routine_params(global_routine_params):
    project_mastermind = Project_mastermind.get_instance()
    prop_dict = project_mastermind.get_properties_dictionary()

    prop_dict[
        ps.GLOBAL_ROUTINE_ANISOTROPIC_FILTER_TIMES] = global_routine_params.global_routine_params_anisotropic_filter_times_input.value()

    prop_dict[
        ps.GLOBAL_ROUTINE_ADAPTIVE_THRESHOLD_WINDOW_SIZE] = global_routine_params.global_routine_params_adaptive_threshold_window_size_input.value()
    prop_dict[
        ps.GLOBAL_ROUTINE_ADAPTIVE_C_CONSTANT] = global_routine_params.global_routine_params_adaptive_threshold_c_constant_input.value()
    prop_dict[ps.GLOBAL_ROUTINE_ADAPTIVE_METHOD] = int(adaptive_threshold.get_method(
        global_routine_params.global_routine_params_adaptive_threshold_method_box.currentText()))

    prop_dict[
        ps.GLOBAL_ROUTINE_MGAC_ITERATIONS] = global_routine_params.global_routine_params_mgac_iterations_input.value()
    prop_dict[
        ps.GLOBAL_ROUTINE_MGAC_THRESHOLD] = global_routine_params.global_routine_params_mgac_threshold_input.value()
    prop_dict[
        ps.GLOBAL_ROUTINE_MGAC_SMOOTHING] = global_routine_params.global_routine_params_mgac_smoothing_input.value()
    prop_dict[ps.GLOBAL_ROUTINE_MGAC_BALLOON] = global_routine_params.global_routine_params_mgac_balloon_input.value()
    prop_dict[ps.GLOBAL_ROUTINE_MGAC_ALPHA] = global_routine_params.global_routine_params_mgac_alpha_input.value()
    prop_dict[ps.GLOBAL_ROUTINE_MGAC_SIGMA] = global_routine_params.global_routine_params_mgac_sigma_input.value()

    prop_dict[
        ps.GLOBAL_ROUTINE_MOVEMENT_THRESHOLD] = global_routine_params.global_routine_params_movement_threshold_input.value()

    prop_dict[
        ps.GLOBAL_ROUTINE_TEXTURE_CLUSTERS] = global_routine_params.global_routine_params_movement_texture_clusters_input.value()
    prop_dict[
        ps.GLOBAL_ROUTINE_TEXTURE_THRESHOLD] = global_routine_params.global_routine_params_movement_texture_threshold_input.value()

    project_mastermind.reload_properties(prop_dict)
    save_properties(prop_dict)
