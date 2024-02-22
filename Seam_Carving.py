import cv2
import numpy as np
import os
from Utils import calculate_energy, min_color, argmin_color, get_dominant, normalize_3d, normalize_2d


def seam_carving(filepath, save_dir, image, is_color=True, is_red_line=False, is_preservation=False, is_dom=False, num_iterations=10, save_step=1, xxyy=(0,0,0,0)):
    """
    Perform "Seam Carving".

    Seam carving is a content-aware image resizing technique that resizes an image while attempting to preserve important visual content.

    Args:
        filepath (str): The path to the input image file.
        save_dir (str): The directory path where the resulting image file will be saved.
        image (np.ndarray): The array representing pixel values of the input image.
        is_color (bool): A boolean indicating whether the image is color or grayscale.
        is_red_line (bool): A boolean indicating whether to save an image with a red line corresponding to the seam.
        is_preservation (bool): A boolean indicating whether there is an area to be preserved.
        is_dom (bool): A boolean indicating whether the dominant color method is applied.
        num_iterations (int): An integer indicating how many columns are reduced (# of seam carving iteration).
        save_step (int): An integer indicating how often the image is saved during the seam carving process.
        xxyy (tuple[int]): A tuple indicating the area of the image to be preserved (x1, x2, y1, y2).

    Returns:
        np.ndarray: The resized image after applying seam carving.
    """
    # unpack the argument
    x1, x2, y1, y2 = xxyy

    # dominant option can be chosen only in color image
    is_dom = is_dom and is_color

    # make directory for saving image
    os.mkdir(save_dir)
    if is_red_line:
        os.mkdir(f"{save_dir}/red_line")

    # save original image
    cv2.imwrite(f'{save_dir}/0th_original.jpg', image)

    # make table whose element indicating if preserve or not
    if is_preservation:
        preserve = np.zeros(image.shape, dtype=int)
        if is_color:  # color
            for ch in range(3):
                preserve[y1:y2 + 1, x1:x2 + 1, ch] = 1
        else:  # gray
            preserve[y1:y2 + 1, x1:x2 + 1] = 1

    # delete seam
    for iter in range(1, num_iterations + 1):
        # get energy table
        energy = calculate_energy(image)

        # adjusting the energy table with preserve table
        h, w = image.shape[:2]
        for row in range(h):
            for col in range(w):
                if is_preservation:
                    if preserve[row, col].all():
                        if is_color:  # color
                            for ch in range(3):
                                energy[row, col, ch] += 1e10
                        else:  # gray
                            energy[row, col] += 1e10

        # dynamic programming table
        dp = energy.copy()
        if is_dom:
            dp = normalize_3d(dp) if dp.ndim == 3 else normalize_2d(dp)

        # find dominant color
        if is_dom:
            dominant = get_dominant(filepath)
            diff = (image - dominant) ** 2
            diff = normalize_3d(diff) if diff.ndim == 3 else normalize_2d(diff)

        # compensate dp table with dominant color
        if is_dom:
            dp = dp + diff * 0.1

        # make reverse table
        h, w = image.shape[:2]
        reverse = np.zeros((h, w), dtype=int)

        # calculate cumulative minimum energy
        for i in range(1, h):
            for j in range(w):
                if j == 0:
                    temp = min_color(dp[i - 1, j], dp[i - 1, j + 1])
                    for jj in [j, j + 1]:
                        if (temp == dp[i - 1, jj]).all():
                            reverse[i, j] = jj
                elif j == w - 1:
                    temp = min_color(dp[i - 1, j - 1], dp[i - 1, j])
                    for jj in [j - 1, j]:
                        if (temp == dp[i - 1, jj]).all():
                            reverse[i, j] = jj
                else:
                    temp = min_color(dp[i - 1, j - 1], dp[i - 1, j], dp[i - 1, j + 1])
                    for jj in [j - 1, j, j + 1]:
                        if (temp == dp[i - 1, jj]).all():
                            reverse[i, j] = jj
                dp[i, j] += temp

        # list that saves the indices corresponding to seam (1D based)
        delete_idx = []
        # initial column (from bottom)
        min_idx = argmin_color(dp[h - 1])
        # position that is not concerning channel
        pos = (h - 1) * w + min_idx
        if is_color:  # color
            for ch in range(3):
                delete_idx.append(pos * 3 + ch)
        else:  # gray
            delete_idx.append(pos)

        # determine which pixels to be deleted, from bottom to top (upward)
        for row in range(h - 2, -1, -1):
            min_idx = reverse[row + 1, min_idx]
            pos = row * w + min_idx
            if is_color:  # color
                for ch in range(3):
                    delete_idx.append(pos * 3 + ch)
            else:  # gray
                delete_idx.append(pos)

        # make the image including red line corresponding to seam
        if is_red_line:
            red_line_image = image.copy()  # before delete
            if is_color:  # color
                for idx in range(len(delete_idx) // 3):
                    del_idx = delete_idx[3 * idx]
                    # index restored to 2D (row, column)
                    hh = del_idx // (3 * w)
                    ww = (del_idx % (3 * w)) // 3
                    for ch in range(3):
                        red_line_image[hh, ww, ch] = 0 if ch != 2 else 255
            else:  # gray
                for idx in range(len(delete_idx)):
                    del_idx = delete_idx[idx]
                    # index restored to 2D (row, column)
                    hh = del_idx // w
                    ww = del_idx % w
                    red_line_image[hh, ww] = 0  # black line, actually

        # delete the pixel in 'delete_idx' list
        image = np.delete(image, delete_idx)
        image = np.reshape(image, (h, w - 1, 3) if is_color else (h, w - 1))

        # same operation on 'preserve' table
        if is_preservation:
            preserve = np.delete(preserve, delete_idx)
            preserve = np.reshape(preserve, (h, w - 1, 3) if is_color else (h, w - 1))

        # save the image every 'save_step' iterations
        if iter % save_step == 0:
            print(f'{iter}th iteration')
            cv2.imwrite(f'{save_dir}/{iter}th_carved{"_preserved" if is_preservation else ""}.jpg', image)
            if is_red_line:
                cv2.imwrite(f'{save_dir}/red_line/{iter}th_red_line.jpg', red_line_image)
    return image
