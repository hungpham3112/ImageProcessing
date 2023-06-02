import numpy as np
from typing import Iterable, Tuple, List
from collections import Counter
import cv2 as cv


def count(matrix: np.ndarray) -> Counter:
    return Counter(matrix.flatten())

def coordinates(counter: Counter) -> Tuple[List[np.uint8], List[np.uint8]]:
    return [key for key, value in sorted(counter.items())], [value for key, value in sorted(counter.items())]


def equalize_intensity(input_image):
    if input_image.ndim == 3 and input_image.shape[2] >= 3:
        ycrcb = cv.cvtColor(input_image, cv.COLOR_RGB2HLS)
        channels = cv.split(ycrcb)
        cv.equalizeHist(channels[2], channels[2])
        cv.equalizeHist(channels[1], channels[1])
        cv.equalizeHist(channels[0], channels[0])
        cv.merge(channels, ycrcb)
        cv.cvtColor(ycrcb, cv.COLOR_HLS2RGB, input_image)
        np.clip(input_image, 0, 255, out=input_image)
        return input_image
    return None

def median_filter(image, kernel_size):
    # Apply median filter to remove salt and pepper noise
    filtered_image = cv.medianBlur(image, kernel_size)
    return filtered_image

def mean_filter(image, kernel_size):
    # Apply mean filter to remove salt and pepper noise
    kernel = np.ones((kernel_size, kernel_size), np.float32) / (kernel_size**2)
    filtered_image = cv.filter2D(image, -1, kernel)
    return filtered_image

def gaussian_smoothing(image, kernel_size, sigma):
    # Apply Gaussian smoothing for image smoothing
    blurred_image = cv.GaussianBlur(image, (kernel_size, kernel_size), sigma)
    return blurred_image
