import numpy as np
# https://stackoverflow.com/questions/50313114/what-is-the-entropy-of-an-image-and-how-is-it-calculated
import skimage.measure
import matplotlib.pylab as pl
import matplotlib.gridspec as gridspec
from sklearn.preprocessing import normalize


def fractal_dimension_static_wrapper(image, start_x, start_y, end_x, end_y, width, height):
    float_image = np.float32(image)
    start_x = start_x if start_x >= 0 else 0
    start_y = start_y if start_y >= 0 else 0
    end_x = end_x if end_x < width else width - 1
    end_y = end_y if end_y < height else height - 1
    float_piece = np.zeros((end_y - start_y, end_x - start_x), dtype=float)

    for y in range(start_y, end_y):
        for x in range(start_x, end_x):
            float_piece[y - start_y, x - start_x] = float_image[y, x]

    entropy = skimage.measure.shannon_entropy(float_piece)
    float_piece.shape += (1,)
    fractal_dimension = fractal_dimension_github(float_piece, n_offsets=10)
    return entropy, fractal_dimension


def fractal_dimension_line(image, region):
    start_x = region[0][0]
    end_x = region[1][0]
    start_y = region[0][1]
    end_y = region[1][1]

    all_points = get_line(start_x, start_y, end_x, end_y)
    all_points_size = len(all_points)

    x_coordinates = np.zeros(all_points_size)
    y_coordinates = np.zeros(all_points_size)
    all_fractal_dimensions = np.zeros(all_points_size)
    all_entropy = np.zeros(all_points_size)
    combined_results = np.zeros(all_points_size)

    calculate_texture_in_line(image, x_coordinates, y_coordinates, all_points, all_fractal_dimensions, all_entropy)

    all_fractal_dimensions = normalize([all_fractal_dimensions])
    all_entropy = normalize([all_entropy])
    all_entropy = all_entropy[0]
    all_fractal_dimensions = all_fractal_dimensions[0]
    combined_results = all_entropy * 0.5 + 0.5 * all_fractal_dimensions

    x = []
    y = []
    for i in range(0, len(all_points) - 1):
        x.append(all_points[i][0])
        y.append(all_points[i][1])

    plot_profile_texture(image, x, y, combined_results, x_coordinates, y_coordinates, all_points_size, all_fractal_dimensions,
                         all_entropy)


def calculate_texture_in_line(image, x_coordinates, y_coordinates, all_points,
                              all_fractal_dimensions, all_entropy):
    index = 0
    diff = 5
    width = image.shape[0]
    height = image.shape[1]

    for point in all_points:
        x = point[0]
        y = point[1]
        x_coordinates[index] = x
        y_coordinates[index] = y
        entropy, fractal_dimension = \
            fractal_dimension_static_wrapper(image, x - diff, y - diff, x + diff, y + diff, width, height)
        all_fractal_dimensions[index] = fractal_dimension
        all_entropy[index] = entropy
        index += 1


def plot_profile_texture(image, x_points, y_points, combined_results, x_coordinates, y_coordinates, all_points_size,
                         all_fractal_dimensions, all_entropy):
    gs = gridspec.GridSpec(2, 3, wspace=0.3, hspace=0.3)

    if abs(x_coordinates[0] - x_coordinates[all_points_size - 1]) > abs(
            y_coordinates[0] - y_coordinates[all_points_size - 1]):
        x_axis = x_coordinates
        x_label = "Punto del eje X"
    else:
        x_axis = y_coordinates
        x_label = "Punto del eje Y"

    pl.figure()
    pl.suptitle('Análisis de textura', fontsize=20, fontweight='bold')

    pl.subplot(gs[0, 0])
    pl.plot(x_axis, all_fractal_dimensions, color='green', label='FractalDimension')
    pl.xlabel(x_label, fontsize=11)
    pl.ylabel('Dimensión fractal', fontsize=11)
    pl.title("Dimensión fractal en el perfil", fontsize=15)

    pl.subplot(gs[0, 1])
    pl.plot(x_axis, all_entropy, color='red', label='Entropy')
    pl.xlabel(x_label, fontsize=11)
    pl.ylabel('Entropía', fontsize=11)
    pl.title("Entropía en el perfil", fontsize=15)

    pl.subplot(gs[1, :-1])
    pl.plot(x_axis, combined_results, color='blue', label='Combinated')
    pl.xlabel(x_label, fontsize=11)
    pl.ylabel('Textura', fontsize=11)
    pl.title("Textura en el perfil", fontsize=15)

    pl.subplot(gs[0:, -1])
    pl.title("Imagen con perfil", fontsize=15)
    pl.imshow(image, cmap=pl.cm.gray, vmin=0, vmax=255)
    pl.axis('off')
    pl.plot(x_points, y_points, linewidth=2, color='blue')

    mng = pl.get_current_fig_manager()
    mng.window.showMaximized()
    pl.show()


def get_line(x1, y1, x2, y2):
    points = []
    issteep = abs(y2 - y1) > abs(x2 - x1)
    if issteep:
        x1, y1 = y1, x1
        x2, y2 = y2, x2
    rev = False
    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1
        rev = True
    deltax = x2 - x1
    deltay = abs(y2 - y1)
    error = int(deltax / 2)
    y = y1
    ystep = None
    if y1 < y2:
        ystep = 1
    else:
        ystep = -1
    for x in range(x1, x2 + 1):
        if issteep:
            points.append((y, x))
        else:
            points.append((x, y))
        error -= deltay
        if error < 0:
            y += ystep
            error += deltax
    # Reverse the list if the coordinates were reversed
    if rev:
        points.reverse()
    return points


# https://github.com/ChatzigeorgiouGroup/FractalDimension
def fractal_dimension_github(array, max_box_size=None, min_box_size=1, n_samples=20, n_offsets=0):
    """Calculates the fractal dimension of a 3D numpy array.
    Args:
        array (np.ndarray): The array to calculate the fractal dimension of.
        max_box_size (int): The largest box size, given as the power of 2 so that
                            2**max_box_size gives the sidelength of the largest box.
        min_box_size (int): The smallest box size, given as the power of 2 so that
                            2**min_box_size gives the sidelength of the smallest box.
                            Default value 1.
        n_samples (int): number of scales to measure over.
        n_offsets (int): number of offsets to search over to find the smallest set N(s) to
                       cover  all voxels>0.
        plot (bool): set to true to see the analytical plot of a calculation.
    """
    # determine the scales to measure on

    if max_box_size == None:
        # default max size is the largest power of 2 that fits in the smallest dimension of the array:
        max_box_size = int(np.floor(np.log2(np.min(array.shape))))
    scales = np.floor(np.logspace(max_box_size, min_box_size, num=n_samples, base=2))
    scales = np.unique(scales)  # remove duplicates that could occur as a result of the floor

    # get the locations of all non-zero pixels
    locs = np.where(array > 0)
    # voxels = np.array([(x, y) for x, y in zip(*locs)])
    voxels = np.array([(x, y, z) for x, y, z in zip(*locs)])

    # count the minimum amount of boxes touched
    Ns = []
    # loop over all scales
    for scale in scales:
        touched = []
        if n_offsets == 0:
            offsets = [0]
        else:
            offsets = np.linspace(0, scale, n_offsets)
        # search over all offsets
        for offset in offsets:
            bin_edges = [np.arange(0, i, scale) for i in array.shape]
            bin_edges = [np.hstack([0 - offset, x + offset]) for x in bin_edges]
            H1, e = np.histogramdd(voxels, bins=bin_edges)
            touched.append(np.sum(H1 > 0))
        Ns.append(touched)
    Ns = np.array(Ns)

    # From all sets N found, keep the smallest one at each scale
    Ns = Ns.min(axis=1)

    # Only keep scales at which Ns changed
    scales = np.array([np.min(scales[Ns == x]) for x in np.unique(Ns)])

    Ns = np.unique(Ns)
    Ns = Ns[Ns > 0]

    scales = scales[:len(Ns)]
    # perform fit
    coeffs = np.polyfit(np.log(1 / scales), np.log(Ns), 1)
    return coeffs[0]