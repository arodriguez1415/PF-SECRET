import matplotlib.pyplot as plt


def plot_metric_over_time(metric_values, frame_values, plot_title, y_label,
                          x_label, show_flag=False, save_flag=False):
    # Sacar esto porque ya funciona !
    frame_values = []
    for i in range(0, len(metric_values)):
        frame_values.append(i)
    plt.figure(plot_title)
    plt.plot(frame_values, metric_values)
    plt.title(plot_title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    if show_flag:
        plt.show()


def plot_metric_histogram(metric_values, plot_title=None, x_label=None,
                          y_label=None, show_flag=False, save_flag=False):
    plt.figure(plot_title)
    plt.hist(metric_values, bins=50)
    plt.title(plot_title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.grid(axis='y', alpha=0.75)
    show_plot(show_flag)
    save_plot(save_flag)


def show_plot(show_flag):
    if show_flag:
        plt.show()


def save_plot(save_flag):
    if save_flag:
        plt.savefig("ASD")
