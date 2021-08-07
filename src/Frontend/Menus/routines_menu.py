from src.Backend.Routines import global_routine
from src.Constants import algorithm_constants
from src.Frontend.Utils.button_controller import disable_button, enable_button


def configure_routines_menu_connections(main_window):
    main_window.global_routine_menu_option.triggered. \
        connect(lambda: load_global_routine_options(main_window))

    main_window.global_routine_initiate_button.clicked.connect(lambda: initiate_global_routine(main_window))
    main_window.global_routine_subroutines_contour_checkbox.stateChanged.connect(lambda:
                                                                                 set_metrics_sub_routine(main_window))


def load_global_routine_options(main_window):
    page = main_window.global_routine_options
    stacked_feature_windows = main_window.stacked_feature_windows
    stacked_feature_windows.setCurrentWidget(page)
    return


def initiate_global_routine(main_window):
    disable_button(main_window.global_routine_initiate_button)
    sub_routines_list = get_sub_routines(main_window)
    global_routine.routine(sub_routines_list)
    enable_button(main_window.global_routine_initiate_button)


def get_sub_routines(main_window):
    sub_routines_list = []

    if main_window.global_routine_subroutines_contour_checkbox.isChecked():
        sub_routines_list.append(algorithm_constants.CONTOUR_SUBROUTINE)

    if main_window.global_routine_subroutines_contour_metrics.isChecked():
        sub_routines_list.append(algorithm_constants.METRICS_SUBROUTINE)

    if main_window.global_routine_subroutines_contour_movement_map_checkbox.isChecked():
        sub_routines_list.append(algorithm_constants.MOVEMENT_SUBROUTINE)

    if main_window.global_routine_subroutines_contour_checkbox_texture_map_checkbox.isChecked():
        sub_routines_list.append(algorithm_constants.TEXTURE_SUBROUTINE)

    return sub_routines_list


def set_metrics_sub_routine(main_window):
    checked = main_window.global_routine_subroutines_contour_checkbox.isChecked()
    main_window.global_routine_subroutines_contour_metrics.setChecked(checked)
