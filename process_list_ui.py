# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'process_list_ui.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ProcessList(object):
    def setupUi(self, ProcessList):
        ProcessList.setObjectName("ProcessList")
        ProcessList.resize(541, 371)
        self.process_widget_title = QtWidgets.QLabel(ProcessList)
        self.process_widget_title.setGeometry(QtCore.QRect(30, 20, 471, 51))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.process_widget_title.setFont(font)
        self.process_widget_title.setAlignment(QtCore.Qt.AlignCenter)
        self.process_widget_title.setObjectName("process_widget_title")
        self.process_widget_tree_list = QtWidgets.QTreeView(ProcessList)
        self.process_widget_tree_list.setGeometry(QtCore.QRect(20, 80, 501, 192))
        self.process_widget_tree_list.setObjectName("process_widget_tree_list")
        self.process_widget_close_button = QtWidgets.QPushButton(ProcessList)
        self.process_widget_close_button.setGeometry(QtCore.QRect(180, 310, 171, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.process_widget_close_button.setFont(font)
        self.process_widget_close_button.setObjectName("process_widget_close_button")

        self.retranslateUi(ProcessList)
        QtCore.QMetaObject.connectSlotsByName(ProcessList)

    def retranslateUi(self, ProcessList):
        _translate = QtCore.QCoreApplication.translate
        ProcessList.setWindowTitle(_translate("ProcessList", "Form"))
        self.process_widget_title.setText(_translate("ProcessList", "Procesos realizados sobre la imagen"))
        self.process_widget_close_button.setText(_translate("ProcessList", "Cerrar"))
