import matplotlib.pyplot as plt

from src.Constants.string_constants import GLOBAL_ROUTINE_SIMPLE_METRICS_PLOT_TITLE, \
    GLOBAL_ROUTINE_DISTRIBUTION_METRICS_PLOT_TITLE


def plot_metric_over_time(metric_values, frame_values, plot_title, y_label,
                          x_label, show_flag=False):
    plt.figure(plot_title)
    plt.plot(frame_values, metric_values)
    plt.title(plot_title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    show_plot(show_flag)


def plot_metric_histogram(metric_values, plot_title=None, x_label=None,
                          y_label=None, show_flag=False):
    plt.figure(plot_title)
    plt.hist(metric_values, bins=50)
    plt.title(plot_title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.grid(axis='y', alpha=0.75)
    show_plot(show_flag)


def save_plot_metrics(metric_values_lists, frame_values_lists, plot_title_list, y_label_list,
                      x_label_list, cell_image_array, save_path):
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)
    metrics_axis = [ax2, ax3, ax4]
    fig.suptitle(GLOBAL_ROUTINE_SIMPLE_METRICS_PLOT_TITLE)

    ax1.imshow(cell_image_array, cmap='gray', vmin=0, vmax=255)

    for i in range(0, 3):
        axis_to_plot = metrics_axis[i]
        axis_to_plot.plot(frame_values_lists[i], metric_values_lists[i])
        axis_to_plot.set_title(plot_title_list[i])
        axis_to_plot.set_xlabel(x_label_list[i])
        axis_to_plot.set_ylabel(y_label_list[i])

    plt.savefig(save_path)


def save_plot_distribution_metrics(metrics_avg_lists, plot_title_list, x_label_list, y_label_list, save_path):
    fig, ax = plt.subplots(figsize=(15, 4), nrows=1, ncols=3)
    fig.suptitle(GLOBAL_ROUTINE_DISTRIBUTION_METRICS_PLOT_TITLE)

    for i in range(0, 3):
        axis_to_plot = ax[i]
        axis_to_plot.hist(metrics_avg_lists[i])
        axis_to_plot.set_title(plot_title_list[i])
        axis_to_plot.set_xlabel(x_label_list[i])
        axis_to_plot.set_ylabel(y_label_list[i])

    plt.savefig(save_path)


def show_plot(show_flag):
    if show_flag:
        plt.show()
