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

    return normalize(classified_image)


def normalize(array):
    array2 = array - array.min()
    if array2.min() == array2.max():
        return array.astype(np.uint8)
    result = array2 * (255.0 / array2.max())
    return result.astype(np.uint8)


def get_method(method_string):
    switcher = {
        algorithm_constants.MEAN_SHIFT: mean_shift,
        algorithm_constants.K_MEANS: k_means
    }
    return switcher.get(method_string, "nothing")


def k_means(dataframe, clusters_quantity=3):
    data_to_use = drop_positions(dataframe)
    print(data_to_use)
    clusters_class = KMeans(n_clusters=clusters_quantity, random_state=0).fit(data_to_use)
    dataframe["classification"] = clusters_class.labels_
    return build_classified_image(dataframe)


def mean_shift(dataframe, clusters_quantity=2):
    training_data, test_data = train_test_split(dataframe, train_size=0.01)
    train_data_to_use = drop_positions(training_data)
    test_data_to_use = drop_positions(test_data)
    clusters_class_train = MeanShift().fit(train_data_to_use)
    clusters_class_test = clusters_class_train.predict(test_data_to_use)
    training_data["classification"] = clusters_class_train.labels_
    test_data["classification"] = clusters_class_test
    dataframe_classified = training_data.append(test_data, ignore_index=True)
    return build_classified_image(dataframe_classified)