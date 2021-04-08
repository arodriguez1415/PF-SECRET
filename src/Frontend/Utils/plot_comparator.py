import numpy as np
import matplotlib

matplotlib.use("TkAgg")  # Do this before importing pyplot!
import matplotlib.pyplot as plt


def compare_with_original(original, modified):
    modified = modified.astype(np.uint8)
    plt.subplot(1, 2, 1)
    plt.imshow(original, cmap='gray')
    plt.axis('off')
    plt.subplot(1, 2, 2)
    plt.imshow(modified, cmap='gray')
    plt.axis('off')
    plt.show()


def plot_metric_over_time(metric_values, plot_title, x_label, y_label):
    time_values = range(0, len(metric_values))

    plt.plot(time_values, metric_values)
    plt.title(plot_title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.show()


def plot_metrics_over_time(metrics_values, plot_titles, x_labels, y_label):
    time_values = range(0, len(metrics_values[0]))

    for i in range(0, len(metrics_values)):
        plt.subplot(1, len(metrics_values), i + 1)
        plt.plot(time_values, metrics_values[i])
        plt.title(plot_titles[i])
        plt.xlabel(x_labels[i])
        plt.ylabel(y_label)
    plt.show()


def show_image(title, image):
    if title is not None:
        plt.title(title)
    plt.imshow(image, cmap='gray')
    plt.axis('off')
    plt.show()

