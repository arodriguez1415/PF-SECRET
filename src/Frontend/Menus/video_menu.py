from src.Backend.Video_processing_algorithms import border_video_generator


def configure_video_menu_connections(main_window):
    main_window.borders_video_menu_option.triggered.connect(
        lambda: generate_borders_video())
    main_window.mask_borders_video_menu_option.triggered.connect(
        lambda: generate_mask_borders_video())


def generate_borders_video():
    border_video_generator.generate_border_detection_video()

def generate_mask_borders_video():
    border_video_generator.generate_mask_video()

