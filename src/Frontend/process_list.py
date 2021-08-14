from PyQt5.QtGui import QStandardItemModel, QStandardItem

from src.Classes.Project_mastermind import Project_mastermind


def configure_window(process_list):
    process_list.process_widget_close_button.clicked.connect(lambda: dismiss_window())


def dismiss_window():
    project_mastermind = Project_mastermind.get_instance()
    project_mastermind.process_list_widget.done(0)


def populate_process_list():
    project_mastermind = Project_mastermind.get_instance()
    process_list = project_mastermind.process_list
    image_wrapper_list = project_mastermind.get_image_processing_list()
    view = process_list.process_widget_tree_list
    model = QStandardItemModel()
    model.setHorizontalHeaderLabels(["Procesos realizados:"])
    view.setModel(model)
    view.setUniformRowHeights(True)

    for i in range(0, len(image_wrapper_list)):
        process = image_wrapper_list[i].get_method()
        process_item = QStandardItem('Método: {}'.format(process.get_method_name()))
        process_attributes_dict = process.get_attributes_dict()
        for attribute_name, attribute_value in process_attributes_dict.items():
            attribute = QStandardItem('{}: '.format(attribute_name) + '{}'.format(attribute_value))
            process_item.appendRow(attribute)
        model.appendRow(process_item)
        # span container columns
        view.setFirstColumnSpanned(i, view.rootIndex(), True)