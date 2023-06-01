import numpy as np
from typing import Iterable, Tuple, List
from collections import Counter

def count(matrix: np.ndarray) -> Counter:
    return Counter(matrix.flatten())

def coordinates(counter: Counter) -> Tuple[List[np.uint8], List[np.uint8]]:
    return [key for key, value in sorted(counter.items())], [value for key, value in sorted(counter.items())]

def histogram_equalization(image):
    # Convert the image to grayscale
    gray = np.mean(image, axis=2)

    # Calculate the histogram of the grayscale image
    hist, bins = np.histogram(gray.flatten(), bins=256, range=[0, 256])

    # Calculate the cumulative distribution function (CDF)
    cdf = hist.cumsum()

    # Normalize the CDF
    cdf_normalized = cdf * 255 / cdf[-1]

    # Apply histogram equalization by mapping the intensities
    equalized = np.interp(gray.flatten(), bins[:-1], cdf_normalized).reshape(gray.shape)

    # Convert the equalized image back to RGB
    equalized_image = np.stack([equalized] * 3, axis=2).astype(np.uint8)

    # Return the equalized image
    return equalized_image
