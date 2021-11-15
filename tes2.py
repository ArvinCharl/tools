#!/user/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import cv2

sdThresh = 12
font = cv2.FONT_HERSHEY_SIMPLEX


def distMap(frame1, frame2):
    """outputs pythagorean distance between two frames"""
    frame1_32 = np.float32(frame1)
    frame2_32 = np.float32(frame2)
    diff32 = frame1_32 - frame2_32
    norm32 = np.sqrt(diff32[:, :, 0] ** 2 + diff32[:, :, 1] ** 2 + \
                     diff32[:, :, 2] ** 2) / np.sqrt(255 ** 2 + 255 ** 2 + 255 ** 2)
    dist = np.uint8(norm32 * 255)
    return dist



if __name__ == '__main__':
    img1 = cv2.imread(r'D:\Desktop\Snipaste_2021-06-21_11-35-23.jpg')
    img2 = cv2.imread(r'D:\Desktop\Snipaste_2021-06-21_11-37-17.jpg')
    dist = distMap(img1, img2)
    # apply Gaussian smoothing
    mod = cv2.GaussianBlur(dist, (9, 9), 0)
    # apply thresholding
    _, thresh = cv2.threshold(mod, 100, 255, 0)
    # calculate st dev test
    _, stDev = cv2.meanStdDev(mod)
    if stDev > sdThresh:
        print(1)
    print(stDev)
