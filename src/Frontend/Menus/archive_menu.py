from tkinter import filedialog, Tk
from src.Classes.Project_mastermind import Project_mastermind
from src.Classes.Project_image import Project_image


def configure_archive_menu_connections(main_window):
    image_viewer = main_window.image_viewer
    main_window.load_image_menu_option.triggered.connect(lambda: load_image(image_viewer))


def load_image(image_viewer):
    project_mastermind = Project_mastermind.get_instance()
    image_path = get_image_path()
    if image_path:
        project_mastermind.clear_processing()
        image_wrapper = Project_image(image_path)
        project_mastermind.add_image_process(image_wrapper)
        set_image_on_screen(image_wrapper, image_viewer)


def set_image_on_screen(image_wrapper, image_viewer):
    image_viewer.set_screen_image(image_wrapper)


def get_image_path():
    root = Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(initialdir="", title='Choose Image',
                                               filetypes=[("tif", "*.TIF"),
                                                          ("ppm", "*.PPM"),
                                                          ("jpg", "*.JPG"),
                                                          ("png", "*.PNG")])
    root.destroy()
    return file_path
