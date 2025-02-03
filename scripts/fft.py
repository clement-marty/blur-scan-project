import numpy as np
import cv2



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

    return dft_shift, (magnitude_spectrum *255).astype(np.uint8)



def inverse_dft(dft: np.ndarray) -> np.ndarray:
    '''Compute the inverse Discrete Fourier Transform of an image.

    :param np.ndarray dft: The Discrete Fourier Transform of the image.
    :return np.ndarray: The inverse Discrete Fourier Transform of the image.
    '''
    # Shift the zero frequency component back to the original position
    dft_ishift = np.fft.ifftshift(dft)

    # Compute the inverse 2D discrete Fourier Transform
    idft = np.fft.ifft2(dft_ishift)
    img = np.abs(idft)

    return img




# import matplotlib.pyplot as plt

# a, b = dft('/mnt/DEV2/blur-scan-project/images/Bis_Mag_2000_P_0_DW_1e-6_1675162602_res_1536x1024/focus_0.tif')
# c = inverse_dft(a)


# plt.subplot(121)
# plt.imshow(cv2.imread('/mnt/DEV2/blur-scan-project/images/Bis_Mag_2000_P_0_DW_1e-6_1675162602_res_1536x1024/focus_0.tif'), cmap = 'gray')
# plt.subplot(122)
# plt.imshow(c, cmap = 'gray')
# plt.show()