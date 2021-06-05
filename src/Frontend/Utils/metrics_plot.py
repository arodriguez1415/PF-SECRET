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


def plot_metric_histogram(metric_values, plot_title=None, x_label=None, y_label=None, show_flag=False):
    plt.hist(metric_values, bins=50)
    plt.title(plot_title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.grid(axis='y', alpha=0.75)
    if show_flag:
        plt.show()