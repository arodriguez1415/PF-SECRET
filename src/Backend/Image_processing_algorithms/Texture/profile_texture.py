import numpy as np
import math
# https://stackoverflow.com/questions/50313114/what-is-the-entropy-of-an-image-and-how-is-it-calculated
import skimage.measure
import matplotlib.pylab as pl
import matplotlib.gridspec as gridspec
from sklearn.preprocessing import normalize


def fractal_dimension_static_wrapper(image, start_x, start_y, end_x, end_y, width, height):
    float_image = np.float32(image)
    piece_width = end_x - start_x
    piece_height = end_y - start_y
    float_piece = np.zeros((piece_width, piece_height), dtype=float)
    for y in range(0, height):
        for x in range(0, width):
            if (start_y <= y < end_y) and (start_x <= x < end_x):
                float_piece[y - start_y, x - start_x] = float_image[y, x]

    entropy = skimage.measure.shannon_entropy(float_piece)
    float_piece.shape += (1,)
    fractal_dimension = fractal_dimension_github(float_piece, n_offsets=10)[0]
    return entropy, fractal_dimension


def fractal_dimension_line(image, region, width, height):
    diff_width = 7
    diff_height = 7

    start_point = region[0]
    end_point = region[1]

    start_x = start_point[0]
    end_x = end_point[0]
    start_y = start_point[1]
    end_y = end_point[1]

    all_points = get_line(start_x, start_y, end_x, end_y)
    all_points_size = len(all_points)

    x_coordinates = np.zeros(all_points_size)
    y_coordinates = np.zeros(all_points_size)
    all_fractal_dimensions = np.zeros(all_points_size)
    all_entropy = np.zeros(all_points_size)
    combinated_results = np.zeros(all_points_size)
    index = 0

    for point in all_points:
        x = point[0]
        y = point[1]
        x_coordinates[index] = x
        y_coordinates[index] = y
        piece_start_x = math.ceil(x - diff_width)
        piece_start_y = math.ceil(y - diff_height)
        piece_end_x = math.ceil(x + diff_width)
        piece_end_y = math.ceil(y + diff_height)
        entropy, fractal_dimension = \
            fractal_dimension_static_wrapper(image, piece_start_x, piece_start_y, piece_end_x, piece_end_y, width, height)
        all_fractal_dimensions[index] = fractal_dimension
        all_entropy[index] = entropy
        index += 1

    all_fractal_dimensions = normalize([all_fractal_dimensions])
    all_entropy = normalize([all_entropy])
    all_entropy = all_entropy[0]
    all_fractal_dimensions = all_fractal_dimensions[0]
    combinated_results = all_entropy * 0.5 + 0.5 * all_fractal_dimensions

    gs = gridspec.GridSpec(2, 2)

    if abs(x_coordinates[0] - x_coordinates[all_points_size - 1]) > abs(y_coordinates[0] - y_coordinates[all_points_size - 1]):
        x_axis = x_coordinates
        x_label = "X Point"
    else:
        x_axis = y_coordinates
        x_label = "Y Point"

    pl.figure()
    ax = pl.subplot(gs[0, 0])
    pl.plot(x_axis, all_fractal_dimensions, color='green', label='FractalDimension')
    pl.xlabel(x_label)
    pl.ylabel('Fractal dimension')

    ax = pl.subplot(gs[0, 1])
    pl.plot(x_axis, all_entropy, color='red', label='Entropy')
    pl.xlabel(x_label)
    pl.ylabel('Entropy')

    ax = pl.subplot(gs[1, :])
    pl.plot(x_axis, combinated_results, color='blue', label='Combinated')
    pl.xlabel(x_label)
    pl.ylabel('Texture')
    pl.show()


def get_line(x1, y1, x2, y2):
    points = []
    issteep = abs(y2-y1) > abs(x2-x1)
    if issteep:
        x1, y1 = y1, x1
        x2, y2 = y2, x2
    rev = False
    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1
        rev = True
    deltax = x2 - x1
    deltay = abs(y2-y1)
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

    # make plot
    # if plot:
    #     fig, ax = plt.subplots(figsize=(8, 6))
    #     ax.scatter(np.log(1 / scales), np.log(np.unique(Ns)), c="teal", label="Measured ratios")
    #     ax.set_ylabel("$\log N(\epsilon)$")
    #     ax.set_xlabel("$\log 1/ \epsilon$")
    #     fitted_y_vals = np.polyval(coeffs, np.log(1 / scales))
    #     ax.plot(np.log(1 / scales), fitted_y_vals, "k--", label=f"Fit: {np.round(coeffs[0], 3)}X+{coeffs[1]}")
    #     ax.legend();
    return [coeffs[0]]