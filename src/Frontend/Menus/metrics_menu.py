from src.Backend.Image_processing_algorithms.Archive_manipulation import video_file_manipulation
from src.Backend.Image_processing_algorithms.Metrics import perimeter_metric
from src.Frontend.Utils import plot_comparator

def configure_metrics_menu_connections(main_window):
    main_window.perimeter_over_time_metrics_menu_option.triggered.connect(lambda: show_perimeter_over_time())


def show_perimeter_over_time():
    array_images_list = video_file_manipulation.get_video_as_array()
    perimeter_values_list = perimeter_metric.get_perimeter_over_time(array_images_list)
    plot_comparator.plot_metric_over_time(perimeter_values_list)

