from minisom import MiniSom
from sklearn.cluster import KMeans, MeanShift, SpectralClustering, AgglomerativeClustering
# import hdbscan
import numpy as np
from sklearn.model_selection import train_test_split

from src.Backend.Image_processing_algorithms.Texture import glcm
from src.Backend.Image_processing_algorithms.Texture import entropy
from src.Backend.Image_processing_algorithms.Archive_manipulation.dataframe_file_manipulation import \
    normalize_dataframe_values
from src.Backend.Image_processing_algorithms.Operations.common_operations import normalize_to_range
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
    if descriptor_label == algorithm_constants.SHANNON_ENTROPY:
        return entropy.calculate_shannon_entropy(image_array)
    if descriptor_label == algorithm_constants.LOCAL_ENTROPY:
        return entropy.calculate_local_entropy(image_array)
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
        algorithm_constants.MEAN_SHIFT: mean_shift,
        algorithm_constants.KOHONEN: self_organized_map,
        algorithm_constants.K_MEANS: k_means,
        algorithm_constants.HDBSCAN: HDBScan,
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


def mean_shift(dataframe, clusters_quantity=2, training_percentage=0.05):
    training_data, test_data = train_test_split(dataframe, train_size=training_percentage)
    train_data_to_use = drop_positions(training_data)
    train_data_to_use = normalize_dataframe_values(train_data_to_use,
                                                   normalize_method=algorithm_constants.FROM_0_TO_255)
    data_to_use = drop_positions(dataframe)
    data_to_use = normalize_dataframe_values(data_to_use,
                                             normalize_method=algorithm_constants.FROM_0_TO_255)

    clusters_class_train = MeanShift().fit(train_data_to_use)  # predice el bandwidth, hay que mirarlo eso
    clusters_class = clusters_class_train.predict(data_to_use)

    dataframe["classification"] = reorganize_clusters(clusters_class_train.cluster_centers_, clusters_class)
    # dataframe["classification"] = clusters_class
    return build_classified_image(dataframe)


def self_organized_map(dataframe, clusters_quantity=2, network_shape=(5, 5),
                       learning_rate=0.5, sigma=0.3, iterations=5):
    training_data, test_data = train_test_split(dataframe, train_size=1)
    train_data_to_use = drop_positions(training_data)
    train_data_to_use = normalize_dataframe_values(train_data_to_use,
                                                   normalize_method=algorithm_constants.FROM_0_TO_1)
    data_to_use = drop_positions(dataframe)
    data_to_use = normalize_dataframe_values(data_to_use,
                                             normalize_method=algorithm_constants.FROM_0_TO_1)

    columns_length = len(train_data_to_use.columns)
    som = MiniSom(network_shape[0], network_shape[1], columns_length, sigma=sigma, learning_rate=learning_rate)
    som.train(train_data_to_use.to_numpy(), iterations, random_order=True)  # iteration = 100
    winner_coordinates = np.array([som.winner(x) for x in data_to_use.to_numpy()]).T

    clusters_class = np.ravel_multi_index(winner_coordinates, network_shape)
    dataframe["classification"] = clusters_class

    print(len(clusters_class))
    unique, counts = np.unique(clusters_class, return_counts=True)
    print(dict(zip(unique, counts)))

    return build_classified_image(dataframe)


def HDBScan(dataframe, clusters_quantity=2, min_cluster_size=1250, min_samples=1):
    data_to_use = drop_positions(dataframe)
    data_to_use = normalize_dataframe_values(data_to_use,
                                             normalize_method=algorithm_constants.FROM_0_TO_255)
    hsdbscan_clusterer = hdbscan.HDBSCAN(min_cluster_size=min_cluster_size, min_samples=min_samples)
    hsdbscan_clusterer.fit(data_to_use)

    clusters_class = hsdbscan_clusterer.labels_
    max_label = clusters_class.max()

    for i in range(0, len(clusters_class)):
        if clusters_class[i] == -1:
            clusters_class[i] = max_label + 1

    dataframe["classification"] = clusters_class

    unique, counts = np.unique(clusters_class, return_counts=True)
    print(dict(zip(unique, counts)))

    return build_classified_image(dataframe)
