import cv2
import numpy as np
from skimage import restoration, color


## --- COMPUTE THE FAST FOURIER TRANSFORM ---
def dft(image_path: str, gamma: float =1) -> tuple[np.ndarray, np.ndarray]:
    '''Compute the Discrete Fourier Transform of an image and apply gamma correction to the magnitude spectrum.

    :param str image_path: The path to the image file.
    :param float gamma: The gamma value to apply to the magnitude spectrum.
    :return tuple[np.ndarray, np.ndarray]: The Discrete Fourier Transform and the magnitude spectrum of the image.
    '''

    # Read the image in grayscale
    img = cv2.imread(image_path, 0)

    # Compute the 2D discrete Fourier Transform
    dft = np.fft.fft2(img)

    # Shift the zero frequency component to the center
    dft_shift = np.fft.fftshift(dft)

    # Compute the magnitude spectrum
    # The magnitude spectrum represents the amplitude of the frequencies present in the image.
    magnitude_spectrum = np.abs(dft_shift)

    # Apply gamma correction
    magnitude_spectrum = np.multiply(magnitude_spectrum, 255 / magnitude_spectrum.max())
    magnitude_spectrum = np.power(magnitude_spectrum, 1/gamma)

    return dft_shift, (magnitude_spectrum * 255).astype(np.uint8)



# --- APPLY A CIRCULAR MASK FOR DISPLAY PURPOSES ---
def apply_circular_mask(image: np.ndarray, radius: float) -> np.ndarray:
    '''Apply a circular mask to an image.
    
    :param np.ndarray image: The image to apply the mask to.
    :param float radius: The radius of the circular mask (as a percentage of the image size).
    :return np.ndarray: The masked image.
    '''
    w, h = image.shape
    r = int(radius * min(w, h) / 100)

    x, y = np.ogrid[:w, :h]
    mask = (x - w // 2) ** 2 + (y - h // 2) ** 2 <= r ** 2

    return np.multiply(image, mask)




# --- WIENER DECONVOLUTION ---

def gaussian_psf(size, sigma):
    # Create a Gaussian Point Spread Function (PSF)
    psf = cv2.getGaussianKernel(size, sigma)
    psf = psf @ psf.T
    return psf


def wiener_deconvolution(image_path, psf):
    image = color.rgb2gray(cv2.imread(image_path))

    # Perform Wiener deconvolution
    deconvolved, _ = restoration.unsupervised_wiener(image, psf)
    return (np.clip(deconvolved, 0, 255) * 255).astype(np.uint8)