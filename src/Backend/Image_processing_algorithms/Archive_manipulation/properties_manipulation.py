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

    return default_properties_dict


def save_global_routine_params(global_routine_params):
    project_mastermind = Project_mastermind.get_instance()
    prop_dict = project_mastermind.get_properties_dictionary()

    prop_dict[ps.GLOBAL_ROUTINE_ANISOTROPIC_FILTER_TIMES] = global_routine_params.global_routine_params_anisotropic_filter_times_input.text()

    prop_dict[ps.GLOBAL_ROUTINE_ADAPTIVE_THRESHOLD_WINDOW_SIZE] = global_routine_params.global_routine_params_adaptive_threshold_window_size_input.value()
    prop_dict[ps.GLOBAL_ROUTINE_ADAPTIVE_C_CONSTANT] = global_routine_params.global_routine_params_adaptive_threshold_c_constant_input.value()
    prop_dict[ps.GLOBAL_ROUTINE_ADAPTIVE_METHOD] = int(adaptive_threshold.get_method(global_routine_params.global_routine_params_adaptive_threshold_method_box.currentText()))

    prop_dict[ps.GLOBAL_ROUTINE_MGAC_ITERATIONS] = global_routine_params.global_routine_params_mgac_iterations_input.value()
    prop_dict[ps.GLOBAL_ROUTINE_MGAC_THRESHOLD] = global_routine_params.global_routine_params_mgac_threshold_input.value()
    prop_dict[ps.GLOBAL_ROUTINE_MGAC_SMOOTHING] = global_routine_params.global_routine_params_mgac_smoothing_input.value()
    prop_dict[ps.GLOBAL_ROUTINE_MGAC_BALLOON] = global_routine_params.global_routine_params_mgac_balloon_input.value()
    prop_dict[ps.GLOBAL_ROUTINE_MGAC_ALPHA] = global_routine_params.global_routine_params_mgac_alpha_input.value()
    prop_dict[ps.GLOBAL_ROUTINE_MGAC_SIGMA] = global_routine_params.global_routine_params_mgac_sigma_input.value()

    prop_dict[ps.GLOBAL_ROUTINE_MOVEMENT_THRESHOLD] = global_routine_params.global_routine_params_movement_threshold_input.value()

    prop_dict[ps.GLOBAL_ROUTINE_TEXTURE_CLUSTERS] = global_routine_params.global_routine_params_movement_texture_clusters_input.value()
    prop_dict[ps.GLOBAL_ROUTINE_TEXTURE_THRESHOLD] = global_routine_params.global_routine_params_movement_texture_threshold_input.value()

    project_mastermind.reload_properties(prop_dict)
    save_properties(prop_dict)


def set_properties(prop_dict, main_window, global_routine_params):
    for key in prop_dict.keys():
        if key != ps.IMAGES_SOURCE_FOLDER:
            prop_dict[key] = int(prop_dict[key])

    global_routine_params.global_routine_params_anisotropic_filter_times_input.setValue(prop_dict[ps.GLOBAL_ROUTINE_ANISOTROPIC_FILTER_TIMES])

    global_routine_params.global_routine_params_adaptive_threshold_window_size_input.setValue(prop_dict[ps.GLOBAL_ROUTINE_ADAPTIVE_THRESHOLD_WINDOW_SIZE])
    global_routine_params.global_routine_params_adaptive_threshold_c_constant_input.setValue(prop_dict[ps.GLOBAL_ROUTINE_ADAPTIVE_C_CONSTANT])
    global_routine_params.global_routine_params_adaptive_threshold_method_box.setCurrentText(get_text_method(prop_dict[ps.GLOBAL_ROUTINE_ADAPTIVE_METHOD]))

    global_routine_params.global_routine_params_mgac_iterations_input.setValue(prop_dict[ps.GLOBAL_ROUTINE_MGAC_ITERATIONS])
    global_routine_params.global_routine_params_mgac_threshold_input.setValue(prop_dict[ps.GLOBAL_ROUTINE_MGAC_THRESHOLD])
    global_routine_params.global_routine_params_mgac_smoothing_input.setValue(prop_dict[ps.GLOBAL_ROUTINE_MGAC_SMOOTHING])
    global_routine_params.global_routine_params_mgac_balloon_input.setValue(prop_dict[ps.GLOBAL_ROUTINE_MGAC_BALLOON])
    global_routine_params.global_routine_params_mgac_alpha_input.setValue(prop_dict[ps.GLOBAL_ROUTINE_MGAC_ALPHA])
    global_routine_params.global_routine_params_mgac_sigma_input.setValue(prop_dict[ps.GLOBAL_ROUTINE_MGAC_SIGMA])

    global_routine_params.global_routine_params_movement_threshold_input.setValue(prop_dict[ps.GLOBAL_ROUTINE_MOVEMENT_THRESHOLD])

    global_routine_params.global_routine_params_movement_texture_clusters_input.setValue(prop_dict[ps.GLOBAL_ROUTINE_TEXTURE_CLUSTERS])
    global_routine_params.global_routine_params_movement_texture_threshold_input.setValue(prop_dict[ps.GLOBAL_ROUTINE_TEXTURE_THRESHOLD])

