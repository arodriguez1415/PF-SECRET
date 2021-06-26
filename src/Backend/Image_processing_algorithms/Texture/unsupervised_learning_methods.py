from minisom import MiniSom
from sklearn.cluster import KMeans, MeanShift
import numpy as np
from sklearn.model_selection import train_test_split

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

    return normalize_256(classified_image)


def normalize_256(array):
    array2 = array - array.min()
    if array2.min() == array2.max():
        return array.astype(np.uint8)
    result = array2 * (255.0 / array2.max())
    return result.astype(np.uint8)

def normalize_zero_to_one(array):
    array2 = array - array.min()
    if array2.min() == array2.max():
        return array.astype(np.uint8)
    result = array2 * (1.0 / array2.max())
    return result.astype(np.uint8)


def get_method(method_string):
    switcher = {
        algorithm_constants.MEAN_SHIFT: mean_shift,
        algorithm_constants.KOHONEN: self_organized_map,
        algorithm_constants.K_MEANS: k_means
    }
    return switcher.get(method_string, "nothing")


def k_means(dataframe, clusters_quantity=3):
    data_to_use = drop_positions(dataframe)
    clusters_class = KMeans(n_clusters=clusters_quantity, random_state=0).fit(data_to_use)
    dataframe["classification"] = clusters_class.labels_
    return build_classified_image(dataframe)


def mean_shift(dataframe, clusters_quantity=2):
    training_data, test_data = train_test_split(dataframe, train_size=0.01)
    train_data_to_use = drop_positions(training_data)
    data_to_use = drop_positions(dataframe)

    clusters_class_train = MeanShift().fit(train_data_to_use) # predice el bandwidth, hay que mirarlo eso
    clusters_class_test = clusters_class_train.predict(data_to_use)

    dataframe["classification"] = clusters_class_test

    return build_classified_image(dataframe)


def self_organized_map(dataframe, clusters_quantity=2):
    training_data, test_data = train_test_split(dataframe, train_size=0.2)
    train_data_to_use = drop_positions(training_data)
    data_to_use = drop_positions(dataframe)
    print(train_data_to_use)
    print(len(train_data_to_use.columns))
    som = MiniSom(6, 6, len(train_data_to_use.columns), sigma=0.3, learning_rate=0.5)
    som.train(train_data_to_use.to_numpy(), 100, random_order=True) # iteration = 100
    winner_coordinates = np.array([som.winner(x) for x in data_to_use]).T
    # cluster_index = np.ravel_multi_index(winner_coordinates, som_shape)
    print(winner_coordinates)
