from src.Backend.Routines import global_routine


def configure_routines_menu_connections(main_window):
    main_window.global_routine_menu_option.triggered. \
        connect(lambda: load_global_routine_options(main_window))

    main_window.global_routine_initiate_button.clicked.connect(lambda: initiate_global_routine())


def load_global_routine_options(main_window):
    page = main_window.global_routine_options
    stacked_feature_windows = main_window.stacked_feature_windows
    stacked_feature_windows.setCurrentWidget(page)
    return


def initiate_global_routine():
    global_routine.routine()
