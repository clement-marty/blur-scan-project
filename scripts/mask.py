import numpy as np



def get_circular_mask(h, w, radius) -> np.ndarray:
    '''Create a circular mask of the given radius and size.
    
    :param int h: The height of the array.
    :param int w: The width of the array.
    :param int radius: The radius of the circle.
    :return np.ndarray: The circular mask.
    '''
    Y, X = np.ogrid[:h, :w]
    distance = (X - w // 2) ** 2 + (Y - h // 2) ** 2
    mask = distance <= radius ** 2
    return mask


def apply_circular_mask(magnitude_spectrum: np.ndarray, radius: int) -> np.ndarray:
    '''Apply a circular mask to the magnitude spectrum of the image.

    :param np.ndarray magnitude_spectrum: The magnitude spectrum of the image.
    :param int radius: The radius of the circle in the frequency domain. (as a percentage of the image size)
    :return np.ndarray: The magnitude spectrum with the circular mask applied.
    '''
    if radius != 0:
        r = int(radius * min(magnitude_spectrum.shape) / 100)
        mask = get_circular_mask(*magnitude_spectrum.shape, r)
        masked_spectrum = magnitude_spectrum.copy()
        masked_spectrum[~mask] = 0
        return masked_spectrum
    else:
        return magnitude_spectrum
