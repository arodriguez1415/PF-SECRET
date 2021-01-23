from tkinter import filedialog, Tk


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
