import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import ImageGrid


def plot_original_vs_actual(images, title, sub_titles):
    fig, ax = plt.subplots(nrows=1, ncols=2)
    fig.suptitle(title)

    for i in range(0, len(images)):
        axis_to_plot = ax[i]
        axis_to_plot.imshow(images[i], cmap="gray")
        axis_to_plot.set_title(sub_titles[i])
        axis_to_plot.axis('off')

    plt.show()


def plot_comparison(images, title, sub_titles, save_path=None):
    fig = plt.figure(figsize=(9.75, 3))
    fig.suptitle(title)
    image = None

    grid = ImageGrid(fig, 111,
                     nrows_ncols=(1, 2),
                     axes_pad=0.15,
                     share_all=True,
                     cbar_location="right",
                     cbar_mode="single",
                     cbar_size="7%",
                     cbar_pad=0.15,
                     )

    for i in range(0, len(images)):
        ax = grid[i]
        image = ax.imshow(images[i], cmap="hot")
        ax.set_title(sub_titles[i])
        grid[i].axis('off')

    # Colorbar
    grid[1].cax.colorbar(image)
    grid[1].cax.toggle_label(True)

    if save_path is not None:
        plt.savefig(save_path)
    else:
        plt.show()


def plot_four_comparison(images, movement_weight_array, title, sub_titles, avg_results):
    fig = plt.figure(figsize=(16, 8))
    movement_heatmap_index = 1
    colorbar_ticks = 6
    fig.suptitle(title)

    grid = ImageGrid(fig, 111,
                     nrows_ncols=(2, 2),
                     axes_pad=0.35,
                     share_all=True,
                     cbar_location="right",
                     cbar_mode="each",
                     cbar_size="7%",
                     cbar_pad=0.15,
                     )

    max_movement_steps = movement_weight_array.max()
    colorbar_custom_ticks = [0]

    for i in reversed(range(1, colorbar_ticks)):
        tick = int(max_movement_steps / i)
        colorbar_custom_ticks.append(tick)

    color_map_array = [plt.get_cmap("gray"), plt.get_cmap("hot"), plt.get_cmap("hot"), plt.get_cmap("hot")]
    for i in range(0, len(images)):
        im = grid[i].imshow(images[i], cmap=color_map_array[i])
        grid[i].set_title(sub_titles[i], fontdict=None, loc='center', color="k")
        grid[i].axis('off')
        grid.cbar_axes[i].colorbar(im)
        if i == movement_heatmap_index:
            grid.cbar_axes[i].set_yticklabels(colorbar_custom_ticks)

    # Set movement for cbar

    fig.text(0.15, 0.5, avg_results, fontsize=18, horizontalalignment='center', verticalalignment='center',
             style='italic', bbox={'facecolor': 'gray', 'alpha': 0.85, 'pad': 10})

    plt.show()
