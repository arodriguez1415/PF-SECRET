import matplotlib.pyplot as plt


def plot_movement_vs_texture(movement_image_array, texture_image_array):
    plt.subplot(1, 2, 1)
    plt.imshow(movement_image_array)
    plt.axis('off')
    plt.subplot(1, 2, 2)
    plt.imshow(texture_image_array)
    plt.axis('off')
    plt.show()