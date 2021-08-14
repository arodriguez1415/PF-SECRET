import os
import pickle

from src.Constants import configuration_constants, properties_constants


def save_properties(dictionary):
    with open(configuration_constants.PROPERTIES_FILE_PATH, 'wb') as file:
        pickle.dump(dictionary, file, pickle.HIGHEST_PROTOCOL)


def load_properties():
    if not os.path.exists(configuration_constants.PROPERTIES_FILE_PATH):
        dictionary = generate_default_properties()
        save_properties(dictionary)
        return dictionary
    with open(configuration_constants.PROPERTIES_FILE_PATH, 'rb') as file:
        return pickle.load(file)


def generate_default_properties():
    default_properties_dict = {}

    default_properties_dict[properties_constants.IMAGES_SOURCE_FOLDER] = configuration_constants.TEST_IMAGES_DIR

    return default_properties_dict