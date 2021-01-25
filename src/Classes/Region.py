from src.Classes.Project_mastermind import Project_mastermind


class Region:

    drawable_label = None
    points = []

    def __init__(self):
        self.set_drawable_label()

    def set_drawable_label(self):
        project_mastermind = Project_mastermind.get_instance()
        drawable_label = project_mastermind.main_window.image_viewer
        self.drawable_label = drawable_label

    def get_actual_region(self):
        region_qpoints = self.drawable_label.get_polygon()
        for qpoint in region_qpoints:
            x_axis = qpoint.x()
            y_axis = qpoint.y()
            point = (x_axis, y_axis)
            self.points.append(point)
        return self.points

    def get_square_region(self):
        image_process_wrapper = Project_mastermind.get_instance().get_last_image_process()
        height = image_process_wrapper.height
        width = image_process_wrapper.width
        top_left_point = (0, 0)
        bottom_left_point = (0, height - 1)
        bottom_right_point = (width - 1, height - 1)
        top_right_point = (width - 1, 0)
        self.points.append(top_left_point)
        self.points.append(bottom_left_point)
        self.points.append(bottom_right_point)
        self.points.append(top_right_point)
        self.points.append(top_left_point)
        return self.points
