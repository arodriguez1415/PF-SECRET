from PyQt5 import QtWidgets
import sys
import src.Frontend.main_window as main_window_functions
from src.Classes.Project_mastermind import Project_mastermind
from main_window import Ui_MainWindow


def catch_exceptions(t, val, tb):
    QtWidgets.QMessageBox.critical(None, "An exception was raised", "Exception type: {}".format(t))
    old_hook(t, val, tb)


app = QtWidgets.QApplication(sys.argv)
old_hook = sys.excepthook
sys.excepthook = catch_exceptions
main_window_widget = QtWidgets.QMainWindow()
main_window = Ui_MainWindow()
main_window.setupUi(main_window_widget)
main_window_functions.configure_windows(main_window, app)
Project_mastermind = Project_mastermind(app, main_window)
main_window_widget.show()
sys.exit(app.exec_())
