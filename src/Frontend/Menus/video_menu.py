from src.Backend.Video_processing_algorithms import video_generator as video_generator
from src.Classes.Project_mastermind import Project_mastermind
from src.Classes.Project_image import Project_image
from PIL import Image


def configure_video_menu_connections(main_window):
    main_window.generate_video_with_processing_menu_option.triggered.connect(
        lambda: generate_video_with_processing())
    main_window.generate_video_without_processing_menu_option.triggered.connect(
        lambda: generate_video_without_processing())


def generate_video_with_processing():
    print("A")
    return


def generate_video_without_processing():
    video_generator.generate_video()
    return
