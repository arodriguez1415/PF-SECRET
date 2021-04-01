from src.Backend.Image_processing_algorithms.Operations import common_operations


def get_perimeter_over_time(array_images_list):
    perimeter_values_list = []
    threshold_value = 50
    for i in range(0, len(array_images_list)):
        grayscale_array_image = common_operations.rgb_to_gray(array_images_list[i])
        threshold_array_image = common_operations.threshold(grayscale_array_image, threshold_value)
        perimeter = get_perimeter(threshold_array_image)
        perimeter_values_list.append(perimeter)
    return perimeter_values_list


def get_perimeter(matrix):
    rows, cols = matrix.shape
    perimeter = 0
    for row in range(rows):
        for col in range(cols):
            if matrix[row][col] == 255 and is_perimeter(matrix, row, col):
                perimeter += 1
    return perimeter


def is_perimeter(matrix, current_row, current_col):
    rows, cols = matrix.shape

    for i in range(max(0, current_row - 1), min(current_row + 1, rows)):
        for j in range(max(0, current_col - 1), min(current_col + 1, cols)):
            if matrix[i][j] == 0:
                return True
    return False