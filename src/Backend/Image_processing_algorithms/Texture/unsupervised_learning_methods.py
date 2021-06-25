from sklearn.cluster import KMeans
import numpy as np


def drop_positions(data):
    position_columns = ['row', 'col']

    data_to_use = data.copy()
    data_to_use = data_to_use.drop(position_columns, axis=1)

    return data_to_use


def build_classified_image(dataframe):
    dataframe_rows = len(dataframe.index)
    image_rows = dataframe['row'].iloc[dataframe_rows - 1] + 1
    image_cols = dataframe['col'].iloc[dataframe_rows - 1] + 1
    image_shape = (image_rows, image_cols)

    classified_image = np.zeros(image_shape)

    for observation in range(0, dataframe_rows):
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


def k_means(dataframe):
    data_to_use = drop_positions(dataframe)
    clusters_class = KMeans(n_clusters=5, random_state=0).fit(data_to_use)
    dataframe["classification"] = clusters_class.labels_
    return build_classified_image(dataframe)
