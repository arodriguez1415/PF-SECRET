import numpy as np
import matplotlib

matplotlib.use("TkAgg")  # Do this before importing pyplot!
import matplotlib.pyplot as plt


def plot_metric_over_time(metric_values, frame_values, plot_title, x_label, y_label, show_flag=False):
    plt.figure(plot_title)
    plt.plot(frame_values, metric_values)
    plt.title(plot_title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    if show_flag:
        plt.show()
