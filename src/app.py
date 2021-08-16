from PyQt5 import QtWidgets
import sys
import src.Frontend.main_window as main_window_functions
import src.Frontend.process_list as process_list_functions
import src.Frontend.global_routine_params as global_routine_params_functions
from global_routine_params_ui import Ui_GlobalRoutine
from process_list_ui import Ui_ProcessList
from src.Classes.Project_mastermind import Project_mastermind
from main_window import Ui_MainWindow


def catch_exceptions(t, val, tb):
    if t == SystemExit or t == KeyboardInterrupt or t == GeneratorExit:
        sys.exit()
    QtWidgets.QMessageBox.critical(None, "An exception was raised", "Exception type: {t}\nMessage: {val}")
    old_hook(t, val, tb)

app = QtWidgets.QApplication(sys.argv)
old_hook = sys.excepthook
sys.excepthook = catch_exceptions
main_window_widget = QtWidgets.QMainWindow()
main_window = Ui_MainWindow()
main_window.setupUi(main_window_widget)

process_list_widget = QtWidgets.QDialog()
process_list = Ui_ProcessList()
process_list.setupUi(process_list_widget)

global_routine_params_widget = QtWidgets.QDialog()
global_routine_params = Ui_GlobalRoutine()
global_routine_params.setupUi(global_routine_params_widget)

main_window_functions.configure_windows(main_window, global_routine_params)
process_list_functions.configure_window(process_list)
global_routine_params_functions.configure_window(global_routine_params)

Project_mastermind = Project_mastermind(app, main_window,
                                        process_list, process_list_widget,
                                        global_routine_params, global_routine_params_widget)
main_window_widget.show()
sys.exit(app.exec_())
