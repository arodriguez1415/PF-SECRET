import src.Frontend.Utils.plot_comparator as plot_comparator

from src.Constants import string_constants
from src.Frontend.Utils.button_controller import disable_button, enable_button, is_enabled
from src.Classes.Project_mastermind import Project_mastermind


def configure_viewer_buttons_connections(main_window):
    image_viewer = main_window.image_viewer
    main_window.main_image_button.clicked.connect(lambda: show_main_image(image_viewer))
    main_window.movement_image.clicked.connect(lambda: show_movement_image(image_viewer))
    main_window.texture_image.clicked.connect(lambda: show_texture_image(image_viewer))
    main_window.texture_image_from_video.clicked.connect(lambda: show_texture_image_video(image_viewer))
    main_window.actual_compare_to_original.clicked.connect(lambda: compare_to_original(image_viewer))
    main_window.movement_compare_to_texture_image.clicked.connect(lambda: compare_movement_vs_texture_image())
    main_window.movement_compare_to_texture_video.clicked.connect(lambda: compare_movement_vs_texture_video())
    main_window.texture_image_compare_to_texture_video.clicked.connect(lambda: compare_texture_image_vs_texture_video())


def disable_main_view(main_window):
    disable_button(main_window.main_image_button)
    disable_button(main_window.actual_compare_to_original)


def disable_extra_views(main_window):
    disable_button(main_window.movement_image)
    disable_button(main_window.texture_image)
    disable_button(main_window.texture_image_from_video)
    disable_button(main_window.movement_compare_to_texture_image)
    disable_button(main_window.movement_compare_to_texture_video)
    disable_button(main_window.texture_image_compare_to_texture_video)


def enable_view_button(view_name):
    project_mastermind = Project_mastermind.get_instance()
    main_window = project_mastermind.main_window

    if view_name == string_constants.MAIN_VIEW:
        enable_button(main_window.main_image_button)
        enable_button(main_window.actual_compare_to_original)
    elif view_name == string_constants.MOVEMENT_VIEW:
        enable_button(main_window.movement_image)
        enable_related_button(main_window.texture_image, main_window.movement_compare_to_texture_image)
        enable_related_button(main_window.texture_image_from_video, main_window.movement_compare_to_texture_video)
    elif view_name == string_constants.TEXTURE_IMAGE_VIEW:
        enable_button(main_window.texture_image)
        enable_related_button(main_window.movement_image, main_window.movement_compare_to_texture_image)
        enable_related_button(main_window.texture_image_from_video, main_window.texture_image_compare_to_texture_video)
    elif view_name == string_constants.TEXTURE_VIDEO_VIEW:
        enable_button(main_window.texture_image_from_video)
        enable_related_button(main_window.movement_image, main_window.movement_compare_to_texture_video)
        enable_related_button(main_window.texture_image, main_window.texture_image_compare_to_texture_video)


def enable_related_button(view_button, comparison_view_button):
    enable_flag = is_enabled(view_button)

    if enable_flag:
        enable_button(comparison_view_button)


def show_main_image(image_viewer):
    project_mastermind = Project_mastermind.get_instance()
    original_image_wrapper = project_mastermind.get_last_image_wrapper()
    image_viewer.set_screen_image(original_image_wrapper)


def show_movement_image(image_viewer):
    project_mastermind = Project_mastermind.get_instance()
    movement_heat_map_image_wrapper = project_mastermind.get_movement_heat_map_image()
    image_viewer.set_screen_image(movement_heat_map_image_wrapper)


def show_texture_image(image_viewer):
    project_mastermind = Project_mastermind.get_instance()
    texture_heat_map_image_wrapper = project_mastermind.get_texture_heat_map_image()
    image_viewer.set_screen_image(texture_heat_map_image_wrapper)


def show_texture_image_video(image_viewer):
    project_mastermind = Project_mastermind.get_instance()
    texture_heat_map_image_video_wrapper = project_mastermind.get_texture_heat_map_image_video()
    image_viewer.set_screen_image(texture_heat_map_image_video_wrapper)


def compare_to_original(image_viewer):
    project_mastermind = Project_mastermind.get_instance()
    original_image = project_mastermind.get_original_image()
    original_dim = original_image.ndim
    image_viewer_wrapper = image_viewer.actual_image_wrapper
    actual_image_array = image_viewer_wrapper.image_array
    actual_dim = actual_image_array.ndim
    images_array_list = [original_image, actual_image_array]
    title = string_constants.ORIGINAL_VS_ACTUAL_TITLE
    sub_titles_list = [string_constants.ORIGINAL_TITLE, string_constants.ACTUAL_TITLE]
    with_heatmap = False if actual_dim == original_dim else True
    plot_comparator.plot_original_vs_actual(images_array_list, title, sub_titles_list, with_heatmap)


def compare_movement_vs_texture_image():
    project_mastermind = Project_mastermind.get_instance()
    movement_image_wrapper = project_mastermind.get_movement_heat_map_image()
    texture_image_wrapper = project_mastermind.get_texture_heat_map_image()
    movement_image_array = movement_image_wrapper.image_array
    texture_image_array = texture_image_wrapper.image_array
    images_array_list = [movement_image_array, texture_image_array]
    title = string_constants.MOVEMENT_VS_TEXTURE_IMAGE_TITLE
    sub_titles_list = [string_constants.MOVEMENT_TITLE, string_constants.TEXTURE_IMAGE_TITLE]
    labels = ["Movimiento", "Textura"]
    plot_comparator.plot_comparison(images_array_list, title, sub_titles_list, labels)


def compare_movement_vs_texture_video():
    project_mastermind = Project_mastermind.get_instance()
    movement_image_wrapper = project_mastermind.get_movement_heat_map_image()
    texture_image_video_wrapper = project_mastermind.get_texture_heat_map_image_video()
    movement_image_array = movement_image_wrapper.image_array
    texture_image_video_array = texture_image_video_wrapper.image_array
    images_array_list = [movement_image_array, texture_image_video_array]
    title = string_constants.MOVEMENT_VS_TEXTURE_VIDEO_TITLE
    sub_titles_list = [string_constants.MOVEMENT_TITLE, string_constants.TEXTURE_VIDEO_TITLE]
    labels = ["Movimiento", "Textura"]
    plot_comparator.plot_comparison(images_array_list, title, sub_titles_list, labels)


def compare_texture_image_vs_texture_video():
    project_mastermind = Project_mastermind.get_instance()
    texture_image_wrapper = project_mastermind.get_texture_heat_map_image()
    texture_image_video_wrapper = project_mastermind.get_texture_heat_map_image_video()
    texture_image_array = texture_image_wrapper.image_array
    texture_image_video_array = texture_image_video_wrapper.image_array
    images_array_list = [texture_image_array, texture_image_video_array]
    title = string_constants.TEXTURE_IMAGE_VS_TEXTURE_VIDEO
    sub_titles_list = [string_constants.TEXTURE_IMAGE_TITLE, string_constants.TEXTURE_VIDEO_TITLE]
    labels = ["Textura", "Textura"]
    plot_comparator.plot_comparison(images_array_list, title, sub_titles_list, labels)
