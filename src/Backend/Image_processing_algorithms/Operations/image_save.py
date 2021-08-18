from PIL import Image
from tkinter import filedialog, Tk
import numpy as np
from src.Constants.configuration_constants import GENERATED_IMAGES_DIR
import src.Backend.Image_processing_algorithms.Operations.common_operations as common_operations
from src.Constants.string_constants import WRITE_FILENAME


def get_save_path(image_array):
    root = Tk()
    root.withdraw()
    if common_operations.is_RGB(image_array):
        save_extension = "ppm"
    else:
        save_extension = "pgm"
    save_file_path = filedialog.asksaveasfilename(initialdir=GENERATED_IMAGES_DIR,
                                                  title=WRITE_FILENAME,
                                                  defaultextension=save_extension)
    root.destroy()
    return save_file_path


def save_image(image_array, save_path):
    if common_operations.is_RGB(image_array):
        save_image_rgb(image_array, save_path)
    else:
        save_image_gray(image_array, save_path)


def save_image_gray(image_array, save_path):
    image = Image.fromarray(image_array)
    image = image.convert("L")
    image.save(save_path)
    return


def save_image_rgb(image_array, save_path):
    image = Image.fromarray(np.uint8(image_array))
    image.save(save_path)
    return
