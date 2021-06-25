import numpy as np
import cv2
import matplotlib.pyplot as plt

from src.Backend.Image_processing_algorithms.Operations.common_operations import bgr_to_rgb
from src.Constants import algorithm_constants


def glcm_algorithm(image, descriptors_labels):
    list_descriptors_dict = []

    for descriptor_label in descriptors_labels:
        descriptors_dict = {}
        descriptor_matrix = {
            algorithm_constants.GLCM_MEAN: fast_glcm_mean(image),
            algorithm_constants.GLCM_ENTROPY: fast_glcm_entropy(image),
            algorithm_constants.GLCM_HOMOGENEITY: fast_glcm_homogeneity(image),
            algorithm_constants.GLCM_DISSIMILARITY: fast_glcm_dissimilarity(image)
        }.get(descriptor_label)

        normalized_descriptor_matrix = normalize(descriptor_matrix)
        descriptors_dict["data"] = normalized_descriptor_matrix
        descriptors_dict["label"] = descriptor_label
        list_descriptors_dict.append(descriptors_dict)

        #show_histogram(normalized_descriptor_matrix)
        #bgr_coloured_matrix = cv2.applyColorMap(normalized_descriptor_matrix, cv2.COLORMAP_HOT)
        #show_coloured_image(bgr_coloured_matrix)

    return list_descriptors_dict


def normalize(array):
    array2 = array - array.min()
    if array2.min() == array2.max():
        return array.astype(np.uint8)
    result = array2 * (255.0 / array2.max())
    return result.astype(np.uint8)


def show_coloured_image(bgr_coloured_matrix):
    plt.imshow(bgr_coloured_matrix)
    plt.show()


def show_histogram(image_texture_descriptor):
    dst = cv2.calcHist(image_texture_descriptor, [0], None, [256], [0, 256])

    plt.hist(image_texture_descriptor.ravel(), 256, [0, 256])
    plt.title('Histogram for gray scale image')
    plt.show()


def fast_glcm(img, vmin=0, vmax=255, nbit=8, kernel_size=5):
    mi, ma = vmin, vmax
    ks = kernel_size
    h, w = img.shape

    # digitize
    bins = np.linspace(mi, ma + 1, nbit + 1)
    gl1 = np.digitize(img, bins) - 1
    gl2 = np.append(gl1[:, 1:], gl1[:, -1:], axis=1)

    # make glcm
    glcm = np.zeros((nbit, nbit, h, w), dtype=np.uint8)
    for i in range(nbit):
        for j in range(nbit):
            mask = ((gl1 == i) & (gl2 == j))
            glcm[i, j, mask] = 1

    kernel = np.ones((ks, ks), dtype=np.uint8)
    for i in range(nbit):
        for j in range(nbit):
            glcm[i, j] = cv2.filter2D(glcm[i, j], -1, kernel)
    glcm = glcm.astype(np.float32)

    return glcm


def fast_glcm_mean(img, vmin=0, vmax=255, nbit=8, ks=5):
    '''
    calc glcm mean
    '''
    h, w = img.shape
    glcm = fast_glcm(img, vmin, vmax, nbit, ks)
    mean = np.zeros((h, w), dtype=np.float32)
    for i in range(nbit):
        for j in range(nbit):
            mean += glcm[i, j] * i / (nbit) ** 2

    return mean


def fast_glcm_std(img, vmin=0, vmax=255, nbit=8, ks=5):
    '''
    calc glcm std
    '''
    h, w = img.shape
    glcm = fast_glcm(img, vmin, vmax, nbit, ks)
    mean = np.zeros((h, w), dtype=np.float32)
    for i in range(nbit):
        for j in range(nbit):
            mean += glcm[i, j] * i / (nbit) ** 2

    std2 = np.zeros((h, w), dtype=np.float32)
    for i in range(nbit):
        for j in range(nbit):
            std2 += (glcm[i, j] * i - mean) ** 2

    std = np.sqrt(std2)
    return std


def fast_glcm_contrast(img, vmin=0, vmax=255, nbit=8, ks=5):
    '''
    calc glcm contrast
    '''
    h, w = img.shape
    glcm = fast_glcm(img, vmin, vmax, nbit, ks)
    cont = np.zeros((h, w), dtype=np.float32)
    for i in range(nbit):
        for j in range(nbit):
            cont += glcm[i, j] * (i - j) ** 2

    return cont


def fast_glcm_dissimilarity(img, vmin=0, vmax=255, nbit=8, ks=5):
    '''
    calc glcm dissimilarity
    '''
    h, w = img.shape
    glcm = fast_glcm(img, vmin, vmax, nbit, ks)
    diss = np.zeros((h, w), dtype=np.float32)
    for i in range(nbit):
        for j in range(nbit):
            diss += glcm[i, j] * np.abs(i - j)

    return diss


def fast_glcm_homogeneity(img, vmin=0, vmax=255, nbit=8, ks=5):
    '''
    calc glcm homogeneity
    '''
    h, w = img.shape
    glcm = fast_glcm(img, vmin, vmax, nbit, ks)
    homo = np.zeros((h, w), dtype=np.float32)
    for i in range(nbit):
        for j in range(nbit):
            homo += glcm[i, j] / (1. + (i - j) ** 2)
    return homo


def fast_glcm_ASM(img, vmin=0, vmax=255, nbit=8, ks=5):
    h, w = img.shape
    glcm = fast_glcm(img, vmin, vmax, nbit, ks)
    asm = np.zeros((h, w), dtype=np.float32)
    for i in range(nbit):
        for j in range(nbit):
            asm += glcm[i, j] ** 2

    ene = np.sqrt(asm)
    return asm, ene


def fast_glcm_max(img, vmin=0, vmax=255, nbit=8, ks=5):
    glcm = fast_glcm(img, vmin, vmax, nbit, ks)
    max_ = np.max(glcm, axis=(0, 1))
    return max_


def fast_glcm_entropy(img, vmin=0, vmax=255, nbit=8, ks=5):
    glcm = fast_glcm(img, vmin, vmax, nbit, ks)
    pnorm = glcm / np.sum(glcm, axis=(0, 1)) + 1. / ks ** 2
    ent = np.sum(-pnorm * np.log(pnorm), axis=(0, 1))
    return ent
