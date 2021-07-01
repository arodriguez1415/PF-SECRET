import matplotlib.pyplot as plt
from cv2 import cv2, os

import random
import string

from src.Backend.Image_processing_algorithms.Archive_manipulation import dataframe_file_manipulation
from src.Backend.Image_processing_algorithms.Archive_manipulation.image_file_manipulation import \
    get_multiple_images_path
from src.Backend.Image_processing_algorithms.Texture import unsupervised_learning_methods
from src.Backend.Image_processing_algorithms.Texture.unsupervised_learning_methods import k_means, mean_shift, \
    self_organized_map, HDBScan
from src.Classes.Image_loader import Image_loader
from src.Constants import algorithm_constants, configuration_constants


def generate_tests():
    images_paths = get_multiple_images_path()
    images_arrays = []
    full_combination = [algorithm_constants.GLCM_MEAN, algorithm_constants.GLCM_ENTROPY,
                        algorithm_constants.GLCM_HOMOGENEITY, algorithm_constants.GLCM_DISSIMILARITY,
                        algorithm_constants.LOCAL_ENTROPY]
    glcm_combination = [algorithm_constants.GLCM_MEAN, algorithm_constants.GLCM_ENTROPY,
                        algorithm_constants.GLCM_HOMOGENEITY, algorithm_constants.GLCM_DISSIMILARITY]
    glcm_without_homogeneity = [algorithm_constants.GLCM_MEAN, algorithm_constants.GLCM_ENTROPY,
                                algorithm_constants.GLCM_DISSIMILARITY]
    combinations = [full_combination, glcm_combination, glcm_without_homogeneity]

    for i in range(0, len(images_paths)):
        images_arrays.append(read_image(images_paths[i]))

    #generate_k_means_tests(images_arrays, combinations)
    #generate_kohonen_tests(images_arrays, combinations)
    #generate_mean_shift_tests(images_arrays, combinations)
    generate_HDBScan_tests(images_arrays, combinations)


def get_dataframe_for_test(images_array, combination):
    list_descriptors_dict = []
    list_descriptors_dict = unsupervised_learning_methods.get_descriptors(list_descriptors_dict,
                                                                          images_array,
                                                                          combination)
    dataframe = dataframe_file_manipulation.create_dataframe_from_descriptors(list_descriptors_dict)
    return dataframe


def generate_k_means_tests(images_arrays, combinations):
    clusters = [3, 4, 5]
    for i in range(0, len(images_arrays)):
        for j in range(0, len(combinations)):
            for k in range(0, len(clusters)):
                arguments = [{"label": "Method", "value": "K means"},
                             {"label": "Clusters", "value": str(clusters[k])},
                             {"label": "Combination", "value": get_combinations_string(combinations[j])}]
                dataframe = get_dataframe_for_test(images_arrays[i], combinations[j])
                image_classified = k_means(dataframe, clusters_quantity=clusters[k])
                plot_and_save_result(images_arrays[i], image_classified, arguments)


def generate_mean_shift_tests(images_arrays, combinations):
    training_percentage_list = [0.05, 0.075, 0.1, 0.15]
    for i in range(0, len(images_arrays)):
        for j in range(0, len(combinations)):
            for k in range(0, len(training_percentage_list)):
                arguments = [{"label": "Method", "value": "Mean shift"},
                             {"label": "Combination", "value": get_combinations_string(combinations[j])},
                             {"label": "Training percentage", "value": str(training_percentage_list[k])}]
                dataframe = get_dataframe_for_test(images_arrays[i], combinations[j])
                image_classified = mean_shift(dataframe, training_percentage=training_percentage_list[k])
                plot_and_save_result(images_arrays[i], image_classified, arguments)


def generate_kohonen_tests(images_arrays, combinations):
    network_shape_list = [(3, 3), (5, 5)]
    learning_rate_list = [0.05, 0.1, 0.25]
    sigma_rate_list = [0.001, 0.05, 0.1]
    iterations_list = [5, 10, 25]

    for i in range(0, len(images_arrays)):
        for j in range(0, len(combinations)):
            for ns in range(0, len(network_shape_list)):
                for lr in range(0, len(learning_rate_list)):
                    for sr in range(0, len(sigma_rate_list)):
                        for iter_q in range(0, len(iterations_list)):
                            dataframe = get_dataframe_for_test(images_arrays[i], combinations[j])
                            network_shape = network_shape_list[ns]
                            learning_rate = learning_rate_list[lr]
                            sigma_rate = sigma_rate_list[sr]
                            iterations = iterations_list[iter_q]
                            arguments = [{"label": "Method", "value": "Kohonen"},
                                         {"label": "Combination", "value": get_combinations_string(combinations[j])},
                                         {"label": "Network_shape", "value": str(network_shape)},
                                         {"label": "Learning_rate", "value": str(learning_rate)},
                                         {"label": "Sigma_rate", "value": str(sigma_rate)},
                                         {"label": "Iterations", "value": str(iterations)}]
                            image_classified = self_organized_map(dataframe, network_shape=network_shape,
                                                                  learning_rate=learning_rate, sigma=sigma_rate,
                                                                  iterations=iterations)
                            plot_and_save_result(images_arrays[i], image_classified, arguments)


def generate_HDBScan_tests(images_arrays, combinations):
    min_cluster_size_list = [1250, 1750, 2250]
    min_samples_list = [1, 15, 30]

    for i in range(0, len(images_arrays)):
        for j in range(0, len(combinations)):
            for mcs in range(0, len(min_cluster_size_list)):
                for ms in range(0, len(min_samples_list)):
                    arguments = [{"label": "Method", "value": "HDBScan"},
                                 {"label": "Combination", "value": get_combinations_string(combinations[j])},
                                 {"label": "Min cluster size", "value": min_cluster_size_list[mcs]},
                                 {"label": "Min sample size", "value": min_samples_list[ms]}]
                    dataframe = get_dataframe_for_test(images_arrays[i], combinations[j])
                    image_classified = HDBScan(dataframe, min_cluster_size=min_cluster_size_list[mcs],
                                               min_samples=min_samples_list[ms])
                    plot_and_save_result(images_arrays[i], image_classified, arguments)


def read_image(image_path):
    image_array = Image_loader(image_path, method=None).image_array
    return image_array


def plot_and_save_result(original_image_array, classified_image_array, arguments=None):
    bgr_coloured_matrix = cv2.applyColorMap(classified_image_array, cv2.COLORMAP_HOT)
    rgb_coloured_matrix = cv2.cvtColor(bgr_coloured_matrix, cv2.COLOR_BGR2RGB)

    generate_directories()

    fig = plt.figure(figsize=(35, 15), dpi=80)
    fig.add_subplot(1, 2, 1)
    plt.imshow(original_image_array, cmap='gray', aspect="auto")
    plt.axis('off')
    fig.add_subplot(1, 2, 2)
    plt.imshow(rgb_coloured_matrix, cmap='hot', aspect="auto")
    plt.axis('off')
    fig_title = generate_title(arguments)
    fig.suptitle(fig_title, fontsize=30)
    # plt.colorbar(label="Texture", orientation="vertical", aspect="auto")
    plt_name = generate_random_name(arguments)
    save_dir = get_save_dir(arguments[0]["value"])
    plt.savefig(save_dir + "/" + plt_name)
    plt.close('all')


def generate_directories():
    if not os.path.isdir(configuration_constants.TESTS_TEXTURE_DIRECTORY):
        os.mkdir(configuration_constants.TESTS_TEXTURE_DIRECTORY)

    if not os.path.isdir(configuration_constants.TESTS_K_MEAN_TEXTURE_DIRECTORY):
        os.mkdir(configuration_constants.TESTS_K_MEAN_TEXTURE_DIRECTORY)

    if not os.path.isdir(configuration_constants.TESTS_KOHONEN_TEXTURE_DIRECTORY):
        os.mkdir(configuration_constants.TESTS_KOHONEN_TEXTURE_DIRECTORY)

    if not os.path.isdir(configuration_constants.TESTS_MEAN_SHIFT_TEXTURE_DIRECTORY):
        os.mkdir(configuration_constants.TESTS_MEAN_SHIFT_TEXTURE_DIRECTORY)

    if not os.path.isdir(configuration_constants.TESTS_HDBSCAN_TEXTURE_DIRECTORY):
        os.mkdir(configuration_constants.TESTS_HDBSCAN_TEXTURE_DIRECTORY)


def get_save_dir(method):
    if method == "K means":
        return configuration_constants.TESTS_K_MEAN_TEXTURE_DIRECTORY
    if method == "Kohonen":
        return configuration_constants.TESTS_KOHONEN_TEXTURE_DIRECTORY
    if method == "Mean shift":
        return configuration_constants.TESTS_MEAN_SHIFT_TEXTURE_DIRECTORY
    if method == "HDBScan":
        return configuration_constants.TESTS_HDBSCAN_TEXTURE_DIRECTORY


def get_combinations_string(combination):
    combination_string = ""
    for i in range(0, len(combination)):
        combination_string += combination[i] + " "
    return combination_string


def generate_title(arguments):
    title = ""
    for i in range(0, len(arguments)):
        if i <= 1:
            title += str(arguments[i]["label"] + "=" + str(arguments[i]["value"]) + '\n')
        else:
            title += str(arguments[i]["label"] + "=" + str(arguments[i]["value"]) + ' - ')
    return title


def generate_random_name(arguments):
    name = ''.join(random.choice(string.ascii_letters) for x in range(10)) + "-"

    for i in range(0, len(arguments)):
        name += "-" + str(arguments[i]["label"] + "=" + str(arguments[i]["value"]))
    name += ".jpg"
    return name
