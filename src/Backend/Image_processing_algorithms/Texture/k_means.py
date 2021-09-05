import numpy as np
from sklearn.cluster import KMeans

from src.Backend.Image_processing_algorithms.Archive_manipulation.dataframe_file_manipulation import \
    normalize_dataframe_values
from src.Backend.Image_processing_algorithms.Operations.common_operations import normalize_to_range
from src.Backend.Image_processing_algorithms.Texture import glcm
from src.Constants import algorithm_constants


def get_descriptor_matrix(image_array, descriptor_label):
    if descriptor_label == algorithm_constants.GLCM_MEAN:
        return glcm.fast_glcm_mean(image_array)
    if descriptor_label == algorithm_constants.GLCM_ENTROPY:
        return glcm.fast_glcm_entropy(image_array)
    if descriptor_label == algorithm_constants.GLCM_HOMOGENEITY:
        return glcm.fast_glcm_homogeneity(image_array)
    if descriptor_label == algorithm_constants.GLCM_DISSIMILARITY:
        return glcm.fast_glcm_dissimilarity(image_array)
    return None


def get_descriptors(list_descriptors_dict, image_array, descriptors_labels):
    for descriptor_label in descriptors_labels:
        descriptors_dict = {}
        descriptor_matrix = get_descriptor_matrix(image_array, descriptor_label)
        descriptors_dict["data"] = descriptor_matrix
        descriptors_dict["label"] = descriptor_label
        list_descriptors_dict.append(descriptors_dict)

    return list_descriptors_dict


def drop_positions(data):
    position_columns = ['row', 'col']

    data_to_use = data.copy()
    data_to_use = data_to_use.drop(position_columns, axis=1)

    return data_to_use


def build_classified_image(dataframe):
    image_rows = dataframe['row'].max()
    image_cols = dataframe['col'].max()
    image_shape = (image_rows + 1, image_cols + 1)

    classified_image = np.zeros(image_shape)

    for observation in range(0, len(dataframe.index)):
        row = dataframe['row'][observation]
        col = dataframe['col'][observation]
        classified_image[row][col] = dataframe['classification'][observation]

    return normalize_to_range(classified_image, max_value=algorithm_constants.FROM_0_TO_255)


def get_method(method_string):
    switcher = {
        algorithm_constants.K_MEANS: k_means,
    }
    return switcher.get(method_string, "nothing")


def k_means(dataframe, clusters_quantity=3):
    data_to_use = drop_positions(dataframe)
    data_to_use = normalize_dataframe_values(data_to_use,
                                             normalize_method=algorithm_constants.FROM_0_TO_255)
    clusters_class = KMeans(n_clusters=clusters_quantity, random_state=0).fit(data_to_use)
    dataframe["classification"] = reorganize_clusters(clusters_class.cluster_centers_, clusters_class.labels_)
    # dataframe["classification"] = clusters_class.labels_
    return build_classified_image(dataframe)


def reorganize_clusters(cluster_centers, labels):
    centers = []
    for attribute_centers in cluster_centers:
        centers.append(np.sum(attribute_centers))

    index = np.argsort(centers)
    new_labels = []
    for i in range(0, len(labels)):
        new_labels.append(list(index).index([labels[i]]))

    return new_labels
