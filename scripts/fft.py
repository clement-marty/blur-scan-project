import numpy as np
import cv2



def dft(image_path: str, gamma: float =1) -> np.ndarray:
    '''Compute the Discrete Fourier Transform of an image and apply gamma correction to the magnitude spectrum.

    :param str image_path: The path to the image file.
    :param float gamma: The gamma value to apply to the magnitude spectrum.
    '''

    # Read the image in grayscale
    img = cv2.imread(image_path, 0)

    # Compute the 2D discrete Fourier Transform
    dft = cv2.dft(np.float32(img), flags=cv2.DFT_COMPLEX_OUTPUT)

    # Shift the zero frequency component to the center
    dft_shift = np.fft.fftshift(dft)

    # Compute the magnitude spectrum
    # The magnitude spectrum represents the amplitude of the frequencies present in the image.
    # It is computed by taking the logarithm of the magnitude of the complex numbers obtained 
    # from the DFT, which helps in visualizing the frequency components more effectively.
    # - dft_shift[:, :, 0] represents the real part of the complex numbers
    # - dft_shift[:, :, 1] represents the imaginary part of the complex numbers
    magnitude_spectrum = 20 * np.log(cv2.magnitude(dft_shift[:, :, 0], dft_shift[:, :, 1]))

    # Apply gamma correction
    magnitude_spectrum = np.multiply(magnitude_spectrum, 255 / magnitude_spectrum.max())
    magnitude_spectrum = np.power(magnitude_spectrum, gamma)

    return magnitude_spectrum