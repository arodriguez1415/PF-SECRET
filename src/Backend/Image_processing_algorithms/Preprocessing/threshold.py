import cv2


def binary_threshold(threshold, image_array):
    ret, threshold_image_array = cv2.threshold(image_array, threshold, 255, cv2.THRESH_BINARY)
    return threshold_image_array
