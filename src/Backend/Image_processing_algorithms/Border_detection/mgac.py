from itertools import cycle

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.path import Path
from scipy import ndimage as ndi


def save_image_with_contours_mask(image, contour, save_path):
    fig = plt.figure(figsize=(7, 7))
    fig.clf()
    ax2 = fig.add_subplot(1, 1, 1)
    ax_u = ax2.imshow(np.zeros_like(image), cmap='binary_r', vmin=0, vmax=1)
    ax_u.set_data(contour)
    fig.canvas.draw()
    plt.axis('off')
    extent = ax2.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
    plt.savefig(save_path, bbox_inches=extent)
    plt.close('all')
    return save_path


def save_image_with_contours(image, contour, save_path):
    fig = plt.figure(figsize=(7, 7))
    fig.clf()
    ax1 = fig.add_subplot(1, 1, 1)
    ax1.imshow(image, cmap=plt.cm.gray, vmin=0, vmax=255)
    ax1.contour(contour, [0.5], colors='r', linewidths=1)
    fig.canvas.draw()
    plt.axis('off')
    extent = ax1.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
    plt.savefig(save_path, bbox_inches=extent)
    plt.close('all')
    return save_path


def mgac_border_detection(polygon_region, img, iterations, threshold, smoothing, ballon, alpha, sigma):
    gimg = inverse_gaussian_gradient(img, alpha=alpha, sigma=sigma)
    callback = visual_callback_2d(img)
    init_ls = polygon_level_set(polygon_region, gimg.shape[0], gimg.shape[1])
    final_contour = morphological_geodesic_active_contour(gimg, iterations=iterations,
                                                          iter_callback=callback,
                                                          init_level_set=init_ls,
                                                          smoothing=smoothing, threshold=threshold,
                                                          balloon=ballon)
    return final_contour


class _fcycle(object):
    def __init__(self, iterable):
        """Call functions from the iterable each time it is called."""
        self.funcs = cycle(iterable)

    def __call__(self, *args, **kwargs):
        f = next(self.funcs)
        return f(*args, **kwargs)


# SI and IS operators for 2D and 3D.
_P2 = [np.eye(3),
       np.array([[0, 1, 0]] * 3),
       np.flipud(np.eye(3)),
       np.rot90([[0, 1, 0]] * 3)]
_P3 = [np.zeros((3, 3, 3)) for i in range(9)]

_P3[0][:, :, 1] = 1
_P3[1][:, 1, :] = 1
_P3[2][1, :, :] = 1
_P3[3][:, [0, 1, 2], [0, 1, 2]] = 1
_P3[4][:, [0, 1, 2], [2, 1, 0]] = 1
_P3[5][[0, 1, 2], :, [0, 1, 2]] = 1
_P3[6][[0, 1, 2], :, [2, 1, 0]] = 1
_P3[7][[0, 1, 2], [0, 1, 2], :] = 1
_P3[8][[0, 1, 2], [2, 1, 0], :] = 1


def sup_inf(u):
    """SI operator."""

    if np.ndim(u) == 2:
        P = _P2
    elif np.ndim(u) == 3:
        P = _P3
    else:
        raise ValueError("u has an invalid number of dimensions "
                         "(should be 2 or 3)")

    erosions = []
    for P_i in P:
        erosions.append(ndi.binary_erosion(u, P_i))

    return np.array(erosions, dtype=np.int8).max(initial=0)


def inf_sup(u):
    """IS operator."""

    if np.ndim(u) == 2:
        P = _P2
    elif np.ndim(u) == 3:
        P = _P3
    else:
        raise ValueError("u has an invalid number of dimensions "
                         "(should be 2 or 3)")

    dilations = []
    for P_i in P:
        dilations.append(ndi.binary_dilation(u, P_i))

    return np.array(dilations, dtype=np.int8).min(initial=0)


_curvop = _fcycle([lambda u: sup_inf(inf_sup(u)),  # SIoIS
                   lambda u: inf_sup(sup_inf(u))])  # ISoSI


def visual_callback_2d(background, fig=None):
    if fig is None:
        fig = plt.figure(figsize=(10, 5))
    fig.clf()
    ax1 = fig.add_subplot(1, 2, 1)
    ax1.imshow(background, cmap=plt.cm.gray)

    ax2 = fig.add_subplot(1, 2, 2)
    ax_u = ax2.imshow(np.zeros_like(background), vmin=0, vmax=1)
    plt.pause(0.001)

    def callback(levelset):
        if ax1.collections:
            del ax1.collections[0]
        ax1.contour(levelset, [0.5], colors='r', linewidths=1)
        ax_u.set_data(levelset)
        fig.canvas.draw()
        plt.pause(0.001)

    return callback


def _check_input(image, init_level_set):
    if len(image.shape) != len(init_level_set.shape):
        raise ValueError("The dimensions of the initial level set do not "
                         "match the dimensions of the image.")


def _init_level_set(init_level_set, image_shape):
    if isinstance(init_level_set, str):
        if init_level_set == 'checkerboard':
            res = checkerboard_level_set(image_shape)
        elif init_level_set == 'circle':
            res = circle_level_set(image_shape)
        else:
            raise ValueError("`init_level_set` not in "
                             "['checkerboard', 'circle']")
    else:
        res = init_level_set
    return res


def rgb2gray(img):
    """Convert a RGB image to gray scale."""
    return 0.2989 * img[..., 0] + 0.587 * img[..., 1] + 0.114 * img[..., 2]


def polygon_level_set(polygon_region, width, height):
    x, y = np.meshgrid(np.arange(width), np.arange(height))
    x, y = x.flatten(), y.flatten()
    points = np.vstack((x, y)).T

    p = Path(polygon_region)
    grid = p.contains_points(points)
    mask = grid.reshape(width, height)

    return mask


def circle_level_set(image_shape, center=None, radius=None):
    if center is None:
        center = tuple(i // 2 for i in image_shape)

    if radius is None:
        radius = min(image_shape) * 3.0 / 8.0

    grid = np.mgrid[[slice(i) for i in image_shape]]
    grid = (grid.T - center).T
    phi = radius - np.sqrt(np.sum((grid) ** 2, 0))
    res = np.int8(phi > 0)
    return res


def checkerboard_level_set(image_shape, square_size=5):
    grid = np.ogrid[[slice(i) for i in image_shape]]
    grid = [(grid_i // square_size) & 1 for grid_i in grid]

    checkerboard = np.bitwise_xor.reduce(grid, axis=0)
    res = np.int8(checkerboard)
    return res


def inverse_gaussian_gradient(image, alpha=100.0, sigma=5.0):
    gradnorm = ndi.gaussian_gradient_magnitude(image, sigma, mode='nearest')
    return 1.0 / np.sqrt(1.0 + alpha * gradnorm)


def morphological_chan_vese(image, iterations, init_level_set='checkerboard',
                            smoothing=1, lambda1=1, lambda2=1,
                            iter_callback=lambda x: None):
    init_level_set = _init_level_set(init_level_set, image.shape)

    _check_input(image, init_level_set)

    u = np.int8(init_level_set > 0)

    iter_callback(u)

    for _ in range(iterations):

        # inside = u > 0
        # outside = u <= 0
        c0 = (image * (1 - u)).sum() / float((1 - u).sum() + 1e-8)
        c1 = (image * u).sum() / float(u.sum() + 1e-8)

        # Image attachment
        du = np.gradient(u)
        abs_du = np.abs(du).sum(0)
        aux = abs_du * (lambda1 * (image - c1) ** 2 - lambda2 * (image - c0) ** 2)

        u[aux < 0] = 1
        u[aux > 0] = 0

        # Smoothing
        for _ in range(smoothing):
            u = _curvop(u)

        iter_callback(u)

    return u


def morphological_geodesic_active_contour(gimage, iterations,
                                          init_level_set, smoothing,
                                          threshold, balloon,
                                          iter_callback=lambda x: None):
    image = gimage
    init_level_set = _init_level_set(init_level_set, image.shape)

    _check_input(image, init_level_set)

    if threshold == 'auto':
        threshold = np.percentile(image, 40)

    structure = np.ones((3,) * len(image.shape), dtype=np.int8)
    dimage = np.gradient(image)
    # threshold_mask = image > threshold
    if balloon != 0:
        threshold_mask_balloon = image > threshold / np.abs(balloon)

    u = np.int8(init_level_set > 0)

    iter_callback(u)

    for _ in range(iterations):

        # Balloon
        if balloon > 0:
            aux = ndi.binary_dilation(u, structure)
        elif balloon < 0:
            aux = ndi.binary_erosion(u, structure)
        if balloon != 0:
            u[threshold_mask_balloon] = aux[threshold_mask_balloon]

        # Image attachment
        aux = np.zeros_like(image)
        du = np.gradient(u)
        for el1, el2 in zip(dimage, du):
            aux += el1 * el2
        u[aux > 0] = 1
        u[aux < 0] = 0

        # Smoothing
        for _ in range(smoothing):
            u = _curvop(u)

        iter_callback(u)
    return u
