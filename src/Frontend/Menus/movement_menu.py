def configure_movement_menu_connections(main_window):
    main_window.generate_heat_map_menu_option.triggered. \
        connect(lambda: load_heat_map_options(main_window))


def load_heat_map_options(main_window):
    page = main_window.heat_map_options
    stacked_feature_windows = main_window.stacked_feature_windows
    stacked_feature_windows.setCurrentWidget(page)
    return