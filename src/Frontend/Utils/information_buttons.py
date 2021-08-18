from src.Constants import string_constants
from src.Frontend.Utils.message import show_information_message


def configure_information_buttons(main_window, global_routine_params):
    # Main window

    main_window.adaptive_threshold_window_size_help.clicked.connect(
        lambda: show_information(string_constants.ADAPTIVE_THRESHOLD_WINDOW_SIZE_HELP))
    main_window.adaptive_threshold_c_constant_help.clicked.connect(
        lambda: show_information(string_constants.ADAPTIVE_THRESHOLD_C_CONSTANT_HELP))
    main_window.adaptive_threshold_method_help.clicked.connect(
        lambda: show_information(string_constants.ADAPTIVE_THRESHOLD_METHOD_HELP))
    main_window.adaptive_threshold_algoritm_help.clicked.connect(
        lambda: show_information(string_constants.ADAPTIVE_THRESHOLD_ALGORITHM_HELP))

    main_window.apply_anisotropic_filter_times_help.clicked.connect(
        lambda: show_information(string_constants.ANISOTROPIC_FILTER_TIMES_HELP)
    )
    main_window.anisotropic_filter_algoritm_help.clicked.connect(
        lambda: show_information(string_constants.ANISOTROPIC_FILTER_ALGORITHM_HELP))

    main_window.mgac_iterations_help.clicked.connect(lambda: show_information(string_constants.MGAC_ITERATIONS_HELP))
    main_window.mgac_threshold_help.clicked.connect(lambda: show_information(string_constants.MGAC_THRESHOLD_HELP))
    main_window.mgac_smoothing_help.clicked.connect(lambda: show_information(string_constants.MGAC_SMOOTHING_HELP))
    main_window.mgac_balloon_help.clicked.connect(lambda: show_information(string_constants.MGAC_BALLOON_HELP))
    main_window.mgac_alpha_help.clicked.connect(lambda: show_information(string_constants.MGAC_ALPHA_HELP))
    main_window.mgac_sigma_help.clicked.connect(lambda: show_information(string_constants.MGAC_SIGMA_HELP))
    main_window.mgac_algorithm_help.clicked.connect(lambda: show_information(string_constants.MGAC_ALGORITHM_HELP))

    main_window.texture_profile_algorithm_help.clicked.connect(
        lambda: show_information(string_constants.TEXTURE_PROFILE_ALGORITHM_HELP))

    main_window.texture_classification_image_clusters_help.clicked.connect(
        lambda: show_information(string_constants.TEXTURE_CLASSIFICATION_IMAGE_CLUSTERS_HELP))
    main_window.texture_classification_image_algorithm_help.clicked.connect(
        lambda: show_information(string_constants.TEXTURE_CLASSIFICATION_IMAGE_ALGORITHM_HELP))
    main_window.texture_classification_video_threshold_help.clicked.connect(
        lambda: show_information(string_constants.TEXTURE_CLASSIFICATION_VIDEO_THRESHOLD_HELP))
    main_window.texture_classification_video_clusters_help.clicked.connect(
        lambda: show_information(string_constants.TEXTURE_CLASSIFICATION_VIDEO_CLUSTERS_HELP))
    main_window.texture_classification_video_algorithm_help.clicked.connect(
        lambda: show_information(string_constants.TEXTURE_CLASSIFICATION_VIDEO_ALGORITHM_HELP))

    main_window.analyze_movement_and_texture_movement_theshold_help.clicked.connect(
        lambda: show_information(string_constants.GENERATE_MOVEMENT_HEAT_MAP_THRESHOLD_HELP))
    main_window.analyze_movement_and_texture_texture_image_clusters_help.clicked.connect(
        lambda: show_information(string_constants.TEXTURE_CLASSIFICATION_IMAGE_CLUSTERS_HELP))
    main_window.analyze_movement_and_texture_texture_video_clusters_help.clicked.connect(
        lambda: show_information(string_constants.TEXTURE_CLASSIFICATION_VIDEO_THRESHOLD_HELP))
    main_window.analyze_movement_and_texture_texture_video_threshold_help.clicked.connect(
        lambda: show_information(string_constants.TEXTURE_CLASSIFICATION_VIDEO_CLUSTERS_HELP))
    main_window.analyze_movement_and_texture_generate_views_help.clicked.connect(
        lambda: show_information(string_constants.ANALYZE_MOVEMENT_AND_TEXTURE_GENERATE_VIEWS_HELP))
    main_window.analyze_movement_and_texture_algorithm_help.clicked.connect(
        lambda: show_information(string_constants.ANALYZE_MOVEMENT_AND_TEXTURE_ALGORITHM_HELP))

    main_window.generate_heat_map_threshold_help.clicked.connect(
        lambda: show_information(string_constants.GENERATE_MOVEMENT_HEAT_MAP_THRESHOLD_HELP))
    main_window.generate_heat_map_algorithm_help.clicked.connect(
        lambda: show_information(string_constants.GENERATE_MOVEMENT_HEAT_MAP_ALGORITHM_HELP))

    main_window.generate_metrics_load_metrics_help.clicked.connect(
        lambda: show_information(string_constants.GENERATE_METRICS_LOAD_HELP))
    main_window.generate_metrics_algoritm_help.clicked.connect(
        lambda: show_information(string_constants.GENERATE_METRICS_ALGORITHM_HELP))

    main_window.generate_multiple_cells_metrics_algorithm_help.clicked.connect(
        lambda: show_information(string_constants.GENERATE_MULTIPLE_CELLS_METRICS_ALGORITHM_HELP))

    main_window.plot_metrics_load_metrics_help.clicked.connect(
        lambda: show_information(string_constants.PLOT_METRICS_LOAD_HELP))
    main_window.plot_metrics_algorithm_help.clicked.connect(
        lambda: show_information(string_constants.PLOT_METRICS_ALGORITHM_HELP))

    main_window.plot_metrics_distribution_algorithm_metrics.clicked.connect(
        lambda: show_information(string_constants.PLOT_METRICS_DISTRIBUTION_ALGORITHM_HELP))

    main_window.global_routine_algorithm_help.clicked.connect(
        lambda: show_information(string_constants.GLOBAL_ROUTINE_ALGORITHM_HELP))

    # Global routine params

    global_routine_params.global_routine_params_anisotropic_filter_times_help.clicked.connect(
        lambda: show_information(string_constants.ANISOTROPIC_FILTER_TIMES_HELP))

    global_routine_params.global_routine_params_adaptive_threshold_window_size_help.clicked.connect(
        lambda: show_information(string_constants.ADAPTIVE_THRESHOLD_WINDOW_SIZE_HELP))
    global_routine_params.global_routine_params_adaptive_threshold_c_constant_help.clicked.connect(
        lambda: show_information(string_constants.ADAPTIVE_THRESHOLD_C_CONSTANT_HELP))
    global_routine_params.global_routine_params_adaptive_threshold_method_help.clicked.connect(
        lambda: show_information(string_constants.ADAPTIVE_THRESHOLD_METHOD_HELP))

    global_routine_params.global_routine_params_mgac_iterations_help.clicked.connect(
        lambda: show_information(string_constants.MGAC_ALGORITHM_HELP))
    global_routine_params.global_routine_params_mgac_threshold_help.clicked.connect(
        lambda: show_information(string_constants.MGAC_THRESHOLD_HELP))
    global_routine_params.global_routine_params_mgac_smoothing_help.clicked.connect(
        lambda: show_information(string_constants.MGAC_SMOOTHING_HELP))
    global_routine_params.global_routine_params_mgac_balloon_help.clicked.connect(
        lambda: show_information(string_constants.MGAC_BALLOON_HELP))

    global_routine_params.global_routine_params_mgac_alpha_help.clicked.connect(
        lambda: show_information(string_constants.MGAC_ALPHA_HELP))
    global_routine_params.global_routine_params_mgac_sigma_help.clicked.connect(
        lambda: show_information(string_constants.MGAC_SIGMA_HELP))

    global_routine_params.global_routine_params_movement_threshold_help.clicked.connect(
        lambda: show_information(string_constants.GENERATE_MOVEMENT_HEAT_MAP_THRESHOLD_HELP))

    global_routine_params.global_routine_params_movement_texture_clusters_help.clicked.connect(
        lambda: show_information(string_constants.TEXTURE_CLASSIFICATION_VIDEO_THRESHOLD_HELP))
    global_routine_params.global_routine_params_movement_texture_threshold_help.clicked.connect(
        lambda: show_information(string_constants.TEXTURE_CLASSIFICATION_VIDEO_CLUSTERS_HELP))


def show_information(message_id):
    show_information_message(message_id)
    return
