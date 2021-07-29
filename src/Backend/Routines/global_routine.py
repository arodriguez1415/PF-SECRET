from src.Backend.Image_processing_algorithms.Metrics import metrics_generator, metrics_plotter
from src.Backend.Video_processing_algorithms.multiple_cells_video_generator import generate_mask_video_of_all_cells
from src.Constants import algorithm_constants


def routine():
    # Mask stage
    masked_videos_paths_list = generate_mask_video_of_all_cells()

    # Generate metrics stage
    metrics_excel_paths_list = []
    metrics_dictionary = {algorithm_constants.AXIS_RATE_METRIC: True, algorithm_constants.PERIMETER_METRIC: True,
                          algorithm_constants.AREA_METRIC: True}
    distribution_metrics_dictionary = metrics_dictionary
    for masked_video_path in masked_videos_paths_list:
        metrics_excel_path = metrics_generator.generate_metrics(masked_video_path, metrics_dictionary)
        metrics_excel_paths_list.append(metrics_excel_path)

    # Save simple metrics stage
    #for metrics_excel_path in metrics_excel_paths_list:
    #    metrics_values_lists, frames_values_lists, titles_list, x_label_list, y_label_list = metrics_plotter.load_metrics(metrics_excel_path, metrics_dictionary)
    #    metrics_plotter.save_metrics(metrics_values_lists, frames_values_lists, titles_list, x_label_list, y_label_list)

    # Save distribution metrics stage
    metrics_avg_lists, titles_list, x_label_list, y_label_list = metrics_plotter.load_distribution_metrics(
            metrics_excel_paths_list, distribution_metrics_dictionary)
    metrics_plotter.save_distribution_metrics(metrics_avg_lists, titles_list, x_label_list, y_label_list)
