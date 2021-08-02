from src.Classes.Project_mastermind import Project_mastermind
import src.Frontend.Utils.plot_comparator as plot_comparator
from src.Constants import string_constants


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
    image_viewer_wrapper = image_viewer.actual_image_wrapper
    actual_image_array = image_viewer_wrapper.image_array
    images_array_list = [original_image, actual_image_array]
    title = string_constants.ORIGINAL_VS_ACTUAL_TITLE
    sub_titles_list = [string_constants.ORIGINAL_TITLE, string_constants.ACTUAL_TITLE]
    plot_comparator.plot_original_vs_actual(images_array_list, title, sub_titles_list)


def compare_movement_vs_texture_image():
    project_mastermind = Project_mastermind.get_instance()
    movement_image_wrapper = project_mastermind.get_movement_heat_map_image()
    texture_image_wrapper = project_mastermind.get_texture_heat_map_image()
    movement_image_array = movement_image_wrapper.image_array
    texture_image_array = texture_image_wrapper.image_array
    images_array_list = [movement_image_array, texture_image_array]
    title = string_constants.MOVEMENT_VS_TEXTURE_IMAGE_TITLE
    sub_titles_list = [string_constants.MOVEMENT_TITLE, string_constants.TEXTURE_IMAGE_TITLE]
    plot_comparator.plot_comparison(images_array_list, title, sub_titles_list)


def compare_movement_vs_texture_video():
    project_mastermind = Project_mastermind.get_instance()
    movement_image_wrapper = project_mastermind.get_movement_heat_map_image()
    texture_image_video_wrapper = project_mastermind.get_texture_heat_map_image_video()
    movement_image_array = movement_image_wrapper.image_array
    texture_image_video_array = texture_image_video_wrapper.image_array
    images_array_list = [movement_image_array, texture_image_video_array]
    title = string_constants.MOVEMENT_VS_TEXTURE_VIDEO_TITLE
    sub_titles_list = [string_constants.MOVEMENT_TITLE, string_constants.TEXTURE_VIDEO_TITLE]
    plot_comparator.plot_comparison(images_array_list, title, sub_titles_list)


def compare_texture_image_vs_texture_video():
    project_mastermind = Project_mastermind.get_instance()
    texture_image_wrapper = project_mastermind.get_texture_heat_map_image()
    texture_image_video_wrapper = project_mastermind.get_texture_heat_map_image_video()
    texture_image_array = texture_image_wrapper.image_array
    texture_image_video_array = texture_image_video_wrapper.image_array
    images_array_list = [texture_image_array, texture_image_video_array]
    title = string_constants.TEXTURE_IMAGE_VS_TEXTURE_VIDEO
    sub_titles_list = [string_constants.TEXTURE_IMAGE_TITLE, string_constants.TEXTURE_VIDEO_TITLE]
    plot_comparator.plot_comparison(images_array_list, title, sub_titles_list)