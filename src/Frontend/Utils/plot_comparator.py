import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import ImageGrid


def plot_original_vs_actual(images, title, sub_titles, with_heatmap=False):
    if with_heatmap:
        plot_original_vs_actual_with_heatmap(images, title, sub_titles)
    else:
        fig, ax = plt.subplots(nrows=1, ncols=2)
        fig.suptitle(title, fontsize=20, fontweight='bold')

        for i in range(0, len(images)):
            axis_to_plot = ax[i]
            axis_to_plot.imshow(images[i], cmap="gray")
            axis_to_plot.set_title(sub_titles[i], fontsize=15)
            axis_to_plot.axis('off')

        mng = plt.get_current_fig_manager()
        mng.window.showMaximized()
        plt.show()


def plot_original_vs_actual_with_heatmap(images, title, sub_titles):
    fig = plt.figure(figsize=(9.75, 3))
    cmap = ["gray", "hot"]
    fig.suptitle(title, fontsize=20, fontweight='bold')
    image = None

    grid = ImageGrid(fig, 111,
                     nrows_ncols=(1, 2),
                     axes_pad=0.30,
                     share_all=True,
                     cbar_location="right",
                     cbar_mode="single",
                     cbar_size="7%",
                     cbar_pad=0.15,
                     )

    for i in range(0, len(images)):
        ax = grid[i]
        image = ax.imshow(images[i], cmap=cmap[i])
        ax.set_title(sub_titles[i], fontsize=15)
        grid[i].axis('off')

    # Colorbar
    grid[1].cax.colorbar(image)
    grid[1].cax.toggle_label(True)

    mng = plt.get_current_fig_manager()
    mng.window.showMaximized()
    plt.show()


def plot_comparison(images, title, sub_titles, labels, save_path=None):
    fig = plt.figure(figsize=(9.75, 3))
    fig.suptitle(title, fontsize=20, fontweight='bold')

    grid = ImageGrid(fig, 111,
                     nrows_ncols=(1, 2),
                     axes_pad=0.9,
                     share_all=True,
                     cbar_location="right",
                     cbar_mode="each",
                     cbar_size="7%",
                     cbar_pad=0.15
                     )

    for i in range(0, len(images)):
        im = grid[i].imshow(images[i], cmap="hot")
        grid[i].set_title(sub_titles[i], fontsize=15)
        grid[i].axis('off')
        grid.cbar_axes[i].colorbar(im)
        cax = grid.cbar_axes[i]
        axis = cax.axis[cax.orientation]
        axis.label.set_text(labels[i])

    if save_path is not None:
        fig.set_size_inches(8, 6)
        plt.savefig(save_path, dpi=500)
    else:
        mng = plt.get_current_fig_manager()
        mng.window.showMaximized()
        plt.show()


def show_coloured_image(matrix_values, rgb_coloured_matrix, title, label):
    fig = plt.figure(figsize=(16, 8))
    colorbar_ticks = 6
    fig.suptitle(title, fontsize=20, fontweight='bold')

    grid = ImageGrid(fig, 111,
                     nrows_ncols=(1, 1),
                     axes_pad=1,
                     share_all=True,
                     cbar_location="right",
                     cbar_mode="each",
                     cbar_size="7%",
                     cbar_pad=0.15,
                     )

    max_movement_steps = matrix_values.max()
    colorbar_custom_ticks = [0]
    for j in reversed(range(1, colorbar_ticks)):
        tick = int(max_movement_steps / j)
        colorbar_custom_ticks.append(tick)

    im = grid[0].imshow(rgb_coloured_matrix, cmap=plt.get_cmap("hot"))
    grid[0].axis('off')
    grid.cbar_axes[0].colorbar(im)
    cax = grid.cbar_axes[0]
    axis = cax.axis[cax.orientation]
    axis.label.set_text(label)
    grid.cbar_axes[0].set_yticklabels(colorbar_custom_ticks)

    mng = plt.get_current_fig_manager()
    mng.window.showMaximized()


def plot_four_comparison(images_array_list, weight_image_array_list, title, sub_titles, avg_results):
    fig = plt.figure(figsize=(16, 8))
    colorbar_ticks = 6
    fig.suptitle(title, fontsize=20, fontweight='bold')
    labels = ["", "Movimiento", "Textura", "Textura"]

    grid = ImageGrid(fig, 111,
                     nrows_ncols=(2, 2),
                     axes_pad=1.1,
                     share_all=True,
                     cbar_location="right",
                     cbar_mode="each",
                     cbar_size="7%",
                     cbar_pad=0.15,
                     )

    colorbar_custom_ticks_lists = []

    for i in range(0, len(weight_image_array_list)):
        max_movement_steps = weight_image_array_list[i].max()
        colorbar_custom_ticks = [0]
        for j in reversed(range(1, colorbar_ticks)):
            tick = int(max_movement_steps / j)
            colorbar_custom_ticks.append(tick)
        colorbar_custom_ticks_lists.append(colorbar_custom_ticks)

    color_map_array = [plt.get_cmap("gray"), plt.get_cmap("hot"), plt.get_cmap("hot"), plt.get_cmap("hot")]
    for i in range(0, len(images_array_list)):
        im = grid[i].imshow(images_array_list[i], cmap=color_map_array[i])
        grid[i].set_title(sub_titles[i], fontsize=15)
        grid[i].axis('off')
        grid.cbar_axes[i].colorbar(im)
        cax = grid.cbar_axes[i]
        axis = cax.axis[cax.orientation]
        axis.label.set_text(labels[i])
        grid[i].text(0.5, -0.1, avg_results[i], size=12, ha="center", transform=grid[i].transAxes)
        grid.cbar_axes[i].set_yticklabels(colorbar_custom_ticks_lists[i])

    mng = plt.get_current_fig_manager()
    mng.window.showMaximized()
    plt.show()
