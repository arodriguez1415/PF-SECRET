from minisom import MiniSom
from sklearn.cluster import KMeans, MeanShift
import numpy as np
from sklearn.model_selection import train_test_split

from src.Backend.Image_processing_algorithms.Archive_manipulation.dataframe_file_manipulation import \
    normalize_dataframe_values
from src.Backend.Image_processing_algorithms.Operations.common_operations import normalize_to_range
from src.Constants import algorithm_constants


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
        algorithm_constants.K_MEANS: k_means
    }
    return switcher.get(method_string, "nothing")


def k_means(dataframe, clusters_quantity=3):
    data_to_use = drop_positions(dataframe)
    data_to_use = normalize_dataframe_values(data_to_use,
                                             normalize_method=algorithm_constants.FROM_0_TO_255)
    clusters_class = KMeans(n_clusters=clusters_quantity, random_state=0).fit(data_to_use)
    dataframe["classification"] = clusters_class.labels_
    return build_classified_image(dataframe)


def mean_shift(dataframe, clusters_quantity=2):
    training_data, test_data = train_test_split(dataframe, train_size=0.01)
    train_data_to_use = drop_positions(training_data)
    train_data_to_use = normalize_dataframe_values(train_data_to_use,
                                                   normalize_method=algorithm_constants.FROM_0_TO_255)
    data_to_use = drop_positions(dataframe)
    data_to_use = normalize_dataframe_values(data_to_use,
                                             normalize_method=algorithm_constants.FROM_0_TO_255)

    clusters_class_train = MeanShift().fit(train_data_to_use)  # predice el bandwidth, hay que mirarlo eso
    clusters_class = clusters_class_train.predict(data_to_use)

    dataframe["classification"] = clusters_class

    return build_classified_image(dataframe)


def self_organized_map(dataframe, clusters_quantity=2):
    training_data, test_data = train_test_split(dataframe, train_size=1)
    train_data_to_use = drop_positions(training_data)
    train_data_to_use = normalize_dataframe_values(train_data_to_use,
                                                   normalize_method=algorithm_constants.FROM_0_TO_255)
    data_to_use = drop_positions(dataframe)
    data_to_use = normalize_dataframe_values(data_to_use,
                                             normalize_method=algorithm_constants.FROM_0_TO_255)

    network_shape = (25, 25)
    columns_length = len(train_data_to_use.columns)
    som = MiniSom(network_shape[0], network_shape[1], columns_length, sigma=0.05, learning_rate=0.2)
    som.train(train_data_to_use.to_numpy(), 5, random_order=True)  # iteration = 100
    winner_coordinates = np.array([som.winner(x) for x in data_to_use.to_numpy()]).T

    clusters_class = np.ravel_multi_index(winner_coordinates, network_shape)
    dataframe["classification"] = clusters_class

    unique, counts = np.unique(clusters_class, return_counts=True)

    #print(len(clusters_class))
    #print(dict(zip(unique, counts)))

    return build_classified_image(dataframe)