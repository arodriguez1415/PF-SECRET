from src.Backend.Image_processing_algorithms.Archive_manipulation.file_manipulation import get_save_path
from src.Backend.Image_processing_algorithms.Operations.string_manipulator import generate_random_string


def set_save_name_for_dir(image_path_sample):
    image_path_sample = image_path_sample.replace("\\", "/")
    min_split_division = 5

    if len(image_path_sample.split('/')) < min_split_division:
        min_split_division = len(image_path_sample.split('/'))

    filename = ""

    for i in reversed(range(2, min_split_division)):
        filename += image_path_sample.split('/')[-i]
        filename += " - "

    filename += generate_random_string(number_of_chars=10)

    save_path = filename
    return save_path


def set_save_name(feature_name, save_directory, extension=".avi"):
    initial_path = save_directory

    if feature_name is None:
        save_path = get_save_path()
    else:
        filename = feature_name + " - "
        filename += generate_random_string(number_of_chars=10)
        save_path = initial_path + filename + extension
    return save_path
