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


def plot_metric_over_time(metric_values):
    time_values = range(0, len(metric_values))

    plt.plot(time_values, metric_values)
    plt.title('Perimetro en el tiempo')
    plt.xlabel('Perimetro en pixeles')
    plt.ylabel('Tiempo')
    plt.show()


def show_image(title, image):
    if title is not None:
        plt.title(title)
    plt.imshow(image, cmap='gray')
    plt.axis('off')
    plt.show()

