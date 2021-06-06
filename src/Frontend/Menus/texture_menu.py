import src.Backend.Image_processing_algorithms.Texture.lbp as texture_lbp
from src.Backend.Image_processing_algorithms.Texture import fractal_dimention
from src.Backend.Image_processing_algorithms.Texture import profile_texture
from src.Backend.Image_processing_algorithms.Texture import texture_heatmap
from src.Classes.Image_wrapper import Image_wrapper
from src.Classes.Project_mastermind import Project_mastermind
from src.Classes.Region import Region
from src.Frontend.Utils.message import show_message


def configure_texture_menu_connections(main_window):
    main_window.lbp_menu_option.triggered.connect(lambda: lbp_options(main_window))
    main_window.fractal_dimension_menu_option.triggered.connect(lambda: fractal_dimension_options(main_window))
    main_window.texture_profile_menu_option.triggered.connect(lambda: texture_profile_options(main_window))
    main_window.texture_heatmap_menu_option.triggered.connect(lambda: texture_heatmap_options(main_window))

    main_window.lbp_add_process_button.clicked.connect(lambda: add_process(main_window))

    main_window.lbp_symmetric_points_slider.valueChanged.connect(lambda: show_lbp(main_window))
    main_window.lbp_radius_slider.valueChanged.connect(lambda: show_lbp(main_window))
    main_window.lbp_method_box.currentTextChanged.connect(lambda: show_lbp(main_window))

    main_window.lbp_symmetric_points_information_button.clicked.connect(lambda: show_symmetric_points_info())
    main_window.lbp_method_information_button.clicked.connect(lambda: show_method_info())
    main_window.fractal_dimension_apply_button.clicked.connect(lambda: generate_fractal_dimension(main_window))
    main_window.texture_profile_apply_button.clicked.connect(lambda: generate_profile_texture())
    main_window.texture_heatmap_apply_button.clicked.connect(lambda: generate_heatmap())


def lbp_options(main_window):
    page = main_window.lbp_options
    stacked_feature_windows = main_window.stacked_feature_windows
    stacked_feature_windows.setCurrentWidget(page)
    return


def fractal_dimension_options(main_window):
    page = main_window.fractal_dimension_options
    stacked_feature_windows = main_window.stacked_feature_windows
    stacked_feature_windows.setCurrentWidget(page)
    return


def texture_profile_options(main_window):
    page = main_window.texture_profile_options
    stacked_feature_windows = main_window.stacked_feature_windows
    stacked_feature_windows.setCurrentWidget(page)
    return


def texture_heatmap_options(main_window):
    page = main_window.texture_heatmap_options
    stacked_feature_windows = main_window.stacked_feature_windows
    stacked_feature_windows.setCurrentWidget(page)
    return


def generate_fractal_dimension(main_window):
    project_mastermind = Project_mastermind.get_instance()
    current_image_array = project_mastermind.get_last_image()
    method = main_window.fractal_dimension_function_combobox.currentText()

    fractal_dimension_image = fractal_dimention.fractal_dimension_texture(current_image_array, method)
    image_wrapper = Image_wrapper(fractal_dimension_image)
    main_window.image_viewer.set_screen_image(image_wrapper)


def generate_profile_texture():
    project_mastermind = Project_mastermind.get_instance()
    current_image_array = project_mastermind.get_last_image()

    line_region = Region()
    profile_texture.fractal_dimension_line(current_image_array, line_region.get_region())


def generate_heatmap():
    project_mastermind = Project_mastermind.get_instance()
    current_image_array = project_mastermind.get_last_image()

    texture_heatmap.texture_heatmap(current_image_array)


def show_lbp(main_window):
    project_mastermind = Project_mastermind.get_instance()
    symmetric_points_slider = main_window.lbp_symmetric_points_slider
    radius_slider = main_window.lbp_radius_slider
    method_box = main_window.lbp_method_box
    current_image_array = project_mastermind.get_last_image()
    symmetric_points = symmetric_points_slider.value()
    radius = radius_slider.value()
    method = texture_lbp.get_method(method_box.currentText())

    lpb_image = texture_lbp.local_binary_pattern(current_image_array, symmetric_points, radius,
                                                 method)
    image_wrapper = Image_wrapper(lpb_image)
    main_window.image_viewer.set_screen_image(image_wrapper)


def add_process(main_window):
    actual_image_wrapper = main_window.image_viewer.actual_image_wrapper
    project_mastermind = Project_mastermind.get_instance()
    project_mastermind.add_image_process(actual_image_wrapper)


def show_symmetric_points_info():
    show_message("Número de puntos de ajuste vecinos circularmente simétricos (cuantificación del espacio angular)")

def show_method_info():
    default = "Predeterminado: patrón binario local original que es una escala de " + \
    "grises pero no invariante de rotación.\n\n"

    ror = "Ror: extensión de la implementación predeterminada que es la escala de grises e " + \
    "invariante de rotación.\n\n"

    uniforme = "Uniforme: invariancia de rotación mejorada con patrones uniformes y " + \
    "cuantificación más fina del espacio angular que es invariante en la escala de grises y la rotación.\n\n"

    nri_uniform = "Nri_uniform: variante de patrones uniformes no invariantes en rotación " + \
    "que es solo invariante en la escala de grises.\n"

    show_message(default + ror + uniforme + nri_uniform)

