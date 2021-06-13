import numpy as np
from sklearn.cluster import estimate_bandwidth, MeanShift
import matplotlib.pyplot as plt

def mean_shift(image_array):
    flat_image = np.reshape(image_array, [-1, 3])

    # Estimate bandwidth
    bandwidth2 = estimate_bandwidth(flat_image,
                                    quantile=.004, n_samples=1000)
    ms = MeanShift(bandwidth2, bin_seeding=True)
    ms.fit(flat_image)
    labels = ms.labels_

    # Plot image vs segmented image
    plt.figure(0)
    plt.imshow(image_array)
    plt.axis('off')
    # plt.subplot(2, 1, 2)

    plt.figure(1)
    plt.imshow(np.reshape(labels, [256, 320]))  # cmap= 'gray'
    plt.axis('off')

    plt.show()

def mean_shift_scatter()