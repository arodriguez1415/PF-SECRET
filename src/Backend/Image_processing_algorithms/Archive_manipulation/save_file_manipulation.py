import random
import string


def set_save_name(image_path_sample, save_directory, extension=".avi"):
    image_path_sample = image_path_sample.replace("\\", "/")
    initial_path = save_directory
    min_split_division = 6

    if len(image_path_sample.split('/')) < min_split_division:
        min_split_division = len(image_path_sample.split('/'))

    filename = ""

    for i in reversed(range(1, min_split_division)):
        filename += image_path_sample.split('/')[-i]
        filename += "-"

    filename += ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
    # filename = image_path_sample.split('/')[-5] + " - " + image_path_sample.split('/')[-4] + " - " + \
    #            image_path_sample.split('/')[-3] + " - " + image_path_sample.split('/')[-2]

    save_path = initial_path + filename + extension
    return save_path