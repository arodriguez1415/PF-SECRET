import numpy as np
import cv2 as cv
import math

from PIL import Image

import matplotlib.pyplot as plt

from src.Backend.Image_processing_algorithms.Operations import common_operations


def show_and_generate_final_image(im, sorted_fd, coordinates, x_length, y_length):
    image_mark = generate_image(im, im.shape[0], im.shape[1])

    for i in range(0, 4):  # rojo
        index = (sorted_fd[i])[1]
        image_mark = generate_image_with_mark(im.shape[0], im.shape[1], coordinates[index], x_length, y_length,
                                              image_mark, 2)

    for i in range(4, 8):  # verde
        index = (sorted_fd[i])[1]
        image_mark = generate_image_with_mark(im.shape[0], im.shape[1], coordinates[index], x_length, y_length,
                                              image_mark, 1)

    cv.imshow("fd mark", image_mark)
    return image_mark


def generate_image(pixels, image_height, image_width):
    border_image = np.zeros((image_height, image_width, 3), dtype=np.uint8)
    for y in range(0, image_height):
        for x in range(0, image_width):
            border_image[y, x, 0] = np.uint8(pixels[y, x])
            border_image[y, x, 1] = np.uint8(pixels[y, x])
            border_image[y, x, 2] = np.uint8(pixels[y, x])

    return border_image


def generate_image_with_mark(image_height, image_width, coordinate, x_length, y_length, border_image, color):
    space = 5
    coordinate[0] = coordinate[0] - space
    coordinate[1] = coordinate[1] - space
    x_length = x_length - space
    y_length = y_length - space

    for y in range(0, image_height):
        for x in range(0, image_width):
            if (coordinate[0] == y or y == coordinate[0] + x_length) and (
                    coordinate[1] <= x <= coordinate[1] + y_length) \
                    or (coordinate[0] <= y <= coordinate[0] + x_length) and (
                    coordinate[1] == x or x == coordinate[1] + y_length):
                border_image[y, x, color] = np.uint8(255)

    return border_image


def calculate_pieces(size):
    big_pieces = [8, 9, 10, 11, 12]
    small_pieces = [4, 5, 6, 7]
    default = 4

    if size > 256:
        pieces = big_pieces
    else:
        pieces = small_pieces

    for piece in pieces:
        if size % piece == 0:
            default = piece

    return default


def generate_pieces(im):
    width = im.shape[0]
    height = im.shape[1]

    x_pieces = calculate_pieces(width)
    y_pieces = calculate_pieces(height)
    x_length = width // x_pieces
    y_length = height // y_pieces
    tiles = []
    for x in range(0, im.shape[0], x_length):
        for y in range(0, im.shape[1], y_length):
            tiles.append(im[x:x + x_length, y:y + y_length])

    coordinates = [[x, y] for x in range(0, im.shape[0], x_length) for y in range(0, im.shape[1], y_length)]

    return [tiles, coordinates, x_length, y_length]


def fractal_dimension_texture(image, function):
    # image = anisotropic_medical_filter_function(image)
    im = np.float16(image)

    if function == "Github":
        # im = np.reshape(im, im.shape + (1,))
        im.shape += (1,)

    ans = generate_pieces(im)
    tiles = ans[0]
    coordinates = ans[1]
    x_length = ans[2]
    y_length = ans[3]

    if function == "StackOverflow":
        sorted_fd = fractal_dimension_texture_stackoverflow(tiles, len(tiles))
    else:
        sorted_fd = fractal_dimension_texture_github(tiles, len(tiles))

    return show_and_generate_final_image(im, sorted_fd, coordinates, x_length, y_length)


def generate_tile_from_region(image, region_points):
    if len(region_points) > 4:
        print("Son mas de 4 puntos")

    tile_array = image[region_points[0][1]: region_points[3][1], region_points[0][0]: region_points[3][0]]

    return tile_array


def get_fractal_dimension_texture(image, region_points):
    image = np.float16(image)
    image.shape += (1,)
    tiles = generate_tile_from_region(image, region_points)
    fractal_dimension_value = fractal_dimension_github(tiles, n_offsets=10)
    return fractal_dimension_value


def fractal_dimension_texture_stackoverflow(tiles, tiles_length):
    fdDict = {}
    for i in range(tiles_length):
        ans = fractal_dimension_stackoverflow(tiles[i])
        if math.isnan(ans[0]):
            print("NAN!!!!!\n")
        fdDict[i] = (ans[0] + ans[1] * 0.005, i, ans[0], ans[1])

    sorted_fd = sorted(fdDict.values(), key=lambda x: x[0], reverse=True)

    return sorted_fd


def fractal_dimension_texture_github(tiles, tiles_length):
    fdDict = {}
    for i in range(tiles_length):
        ans = fractal_dimension_github(tiles[i], n_offsets=10)
        if math.isnan(ans[0]):
            print("NAN!!!!!\n")
        fdDict[i] = (ans[0], i)

    sorted_fd = sorted(fdDict.values(), key=lambda x: x[0], reverse=True)

    return sorted_fd


def show_and_generate_heat_map(fractal_im):
    img = Image.fromarray(fractal_im)
    normalized = common_operations.normalize(img)
    normalized_np = np.uint8(normalized)
    color_np = cv.applyColorMap(normalized_np, cv.COLORMAP_MAGMA)
    color_image = Image.fromarray(color_np)
    color_image.show()


# def generate_fractal_heat_map(image, function):
#     # image = anisotropic_medical_filter_function(image)
#     im = np.uint8(image)
#
#     if function == 2:
#         im.shape += (1,)
#
#     x_pieces = calculate_pieces(im.shape[0])
#     y_pieces = calculate_pieces(im.shape[1])
#
#     x_length = 30
#     y_length = 30
#
#     if function == 1:
#         fractal_im = fractal_dimension_map_stackoverflow(im, x_length, y_length)
#     else:
#         fractal_im = fractal_dimension_map_github(im, x_length, y_length)
#
#     print("ready")
#
#     show_and_generate_heat_map(fractal_im)
#
#
# def fractal_dimension_map_stackoverflow(im, x_length, y_length):
#     fractal_im = np.zeros((im.shape[1], im.shape[0]), dtype=np.float64)
#     for y in range(0, im.shape[1]):
#         for x in range(0, im.shape[0]):
#             if (x > x_length and y > y_length) and (x < im.shape[0] - x_length and y < im.shape[1] - y_length):
#                 Z = calculate_map_pieces(im, x, y, x_length, y_length)
#                 ans = fractal_dimension_stackoverflow(Z)
#                 if math.isnan(ans[0]):
#                     fractal_im[y, x] = 0
#                 else:
#                     fractal_im[y, x] = ans[0]
#
#     fractal_im = fractal_im[y_length + 1:im.shape[1]-y_length-1:1, x_length+1:im.shape[0]-x_length-1:1]
#     return fractal_im
#
#
# def fractal_dimension_map_github(im, x_length, y_length):
#     fractal_im = np.zeros((im.shape[1], im.shape[0]), dtype=np.float64)
#     for y in range(0, im.shape[1]):
#         for x in range(0, im.shape[0]):
#             if (x > 200 and y > 400) and (x < im.shape[0] - 300 and y < im.shape[1] - 100):
#                 Z = calculate_map_pieces(im, x, y, x_length, y_length)
#                 ans = fractal_dimension_github(Z, n_offsets=10)
#                 print("x: " + str(x) + " - y: " + str(y) + " -- VALUE: " + str(ans[0]))
#                 if math.isnan(ans[0]):
#                     fractal_im[y, x] = 0
#                 else:
#                     fractal_im[y, x] = ans[0]
#     fractal_im = fractal_im[y_length + 1:im.shape[1] - y_length - 1:1, x_length + 1:im.shape[0] - x_length - 1:1]
#     return fractal_im
#
#
# def calculate_map_pieces(im, x, y, x_pieces, y_pieces):
#     height = im.shape[1]
#     width = im.shape[0]
#
#     start_x = (x-x_pieces) if (x-x_pieces) >= 0 else 0
#     start_y = (y-y_pieces) if (y-y_pieces) >= 0 else 0
#     end_x = (x+x_pieces) if (x+x_pieces) <= width else width
#     end_y = (y+y_pieces) if (y+y_pieces) <= height else height
#
#     return im[start_y:end_y:1, start_x:end_x:1]


def fractal_dimension_stackoverflow(Z):
    # Only for 2d image
    assert (len(Z.shape) == 2)
    threshold = np.mean(Z)

    # From https://github.com/rougier/numpy-100 (#87)
    # How to get the block-sum ?
    # https://gist.github.com/viveksck/1110dfca01e4ec2c608515f0d5a5b1d1 explanation

    def boxcount(Z, k):
        x = np.arange(0, Z.shape[0], k)
        y = np.arange(0, Z.shape[1], k)
        first_reduce = np.add.reduceat(Z, x, axis=0)
        S = np.add.reduceat(first_reduce, y, axis=1)

        # We count non-empty (0) and non-full boxes (k*k)
        return len(np.where((S > 0) & (S < k * k))[0])

    # Transform Z into a binary array
    Z = (Z < threshold)
    # print(threshold)

    # Minimal dimension of image
    p = min(Z.shape)

    # Greatest power of 2 less than or equal to p
    n = 2 ** np.floor(np.log(p) / np.log(2))

    # Extract the exponent
    n = int(np.log(n) / np.log(2))

    # Build successive box sizes (from 2**n down to 2**1)
    sizes = 2 ** np.arange(n, 1, -1)

    # Actual box counting with decreasing size
    counts = []
    for size in sizes:
        counts.append(boxcount(Z, size))

    # Fit the successive log(sizes) with log (counts)
    coeffs = np.polyfit(np.log(sizes), np.log(counts), 1)
    return [-coeffs[0], threshold]


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
