from PyQt5 import QtWidgets
import sys
import src.Frontend.main_window as main_window_functions

from main_window import Ui_MainWindow


def catch_exceptions(t, val, tb):
    QtWidgets.QMessageBox.critical(None, "An exception was raised", "Exception type: {}".format(t))
    old_hook(t, val, tb)


app = QtWidgets.QApplication(sys.argv)
old_hook = sys.excepthook
sys.excepthook = catch_exceptions
main_window_widget = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(main_window_widget)
main_window_functions.configure_windows(ui, app)
# setupUi.set_style(ui)
# main_window_widget.setWindowFlags(QtCore.Qt.FramelessWindowHint)
main_window_widget.show()
sys.exit(app.exec_())
