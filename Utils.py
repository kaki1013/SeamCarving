import cv2
import numpy as np
from colorthief import ColorThief


def load_image(filepath, is_color, scale_factor):
    """
    Load an image.

    This function loads an image from the specified filepath with options to control colorfulness and scale.

    Args:
        filepath (str): The path to the image file.
        is_color (bool): A boolean indicating whether the image is color or grayscale.
        scale_factor (float): A scaling factor for resizing the loaded image.

    Returns:
        np.ndarray: The loaded image.
    """
    img_array = np.fromfile(filepath, np.uint8)
    color_option = cv2.IMREAD_COLOR if is_color else cv2.IMREAD_GRAYSCALE
    image = cv2.imdecode(img_array, color_option)
    image = cv2.resize(image, (0, 0), fx=scale_factor, fy=scale_factor, interpolation=cv2.INTER_LINEAR)  # 스케일 팩터 이용
    return image


def calculate_energy(image):
    """
    Calculate the energy of each pixel using gradients.

    This function calculates the energy of the input image using gradients, specifically the Sobel operator.

    Args:
        image (np.ndarray): The loaded image.

    Returns:
        np.ndarray: The energy of the image.
    """
    dx = cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize=3)
    dy = cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize=3)
    energy = np.abs(dx) + np.abs(dy)
    return energy


def min_color(*nums):
    """
    Find the value with the smallest norm value.

    Args:
        *nums: Variable number of arguments representing pixel values.
            If the image is color, it's like (array([0., 0., 0.]), array([6., 6., 6.])).
            If the image is grayscale, it's like (0.0, 6.0).

    Returns:
        int: The minimum value.
    """
    errors = [np.linalg.norm(a) for a in nums]  # norm : color, gray
    idx = np.argmin(errors)
    return nums[idx]


def argmin_color(*nums):
    """
    Find the index of the value with the smallest norm value.

    Args:
        *nums: Variable number of arguments representing pixel values.
            When the image is color, it's like (array([0., 0., 0.]), array([6., 6., 6.])).
            When the image is grayscale, it's like (0.0, 6.0).

    Returns:
        int: The index of the minimum value.
    """
    errors = [np.linalg.norm(a) for a in nums]  # norm : color, gray
    idx = np.argmin(errors)
    return idx


def get_dominant(filepath):
    """
    Retrieve the dominant color from the image.

    This function calculates the dominant color from the specified image file.

    Args:
        filepath (str): The path to the image file.

    Returns:
        np.ndarray: An array representing the dominant color with three integers representing red, green, and blue values.
    """
    ct = ColorThief(filepath)
    dominant_color = ct.get_color(quality=1)
    return dominant_color


def normalize_2d(array):
    """
    Normalize a 2D array.

    This function normalizes a 2D array representing pixel values of a grayscale image with shape (H, W).

    Args:
        array (np.ndarray): The 2D array representing pixel values of the grayscale image.

    Returns:
        np.ndarray: The normalized image.
    """
    array_normal = (array - array.mean()) / array.std()
    return array_normal


def normalize_3d(array):
    """
    Normalize a 3D array.

    This function normalizes a 3D array representing pixel values of a grayscale image with shape (H, W, C).

    Args:
        array (np.ndarray): The 3D array representing pixel values of the color image.

    Returns:
        np.ndarray: The normalized image.
    """
    r, g, b = array[:, :, 0], array[:, :, 1], array[:, :, 2]
    r = normalize_2d(r)
    g = normalize_2d(g)
    b = normalize_2d(b)
    array_normal = np.stack((r, g, b), axis=2)
    return array_normal
