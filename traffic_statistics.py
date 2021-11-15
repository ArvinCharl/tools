#!/user/bin/env python3
# -*- coding: utf-8 -*-
import cv2
import numpy as np


def line(h, w, h1, w1, h2, w2):
    k = (w2 - w1) / (h2 - h1)  # 直线斜率
    b = w1 - k * h1  # 偏移量
    return (h * k + b) <= w  # 返回bool值，如果该点在斜线下方，返回False


def cut(img, point_A, point_B):
    h1, w1 = point_A[0], point_A[1]
    h2, w2 = point_B[0], point_B[1]
    height, width, _ = img.shape

    up = np.zeros((height, width, 3), dtype='uint8')
    down = np.zeros((height, width, 3), dtype='uint8')  # 黑底, 一定要加uint8

    for i in range(height):
        for j in range(width):
            if not line(i, j, h1, w1, h2, w2):
                up[i, j] = img[i, j]
            else:
                down[i, j] = img[i, j]
    return np.array(up), np.array(down)


path = 'traffic2.jpg'

img = cv2.imread(path)

# 点的坐标由用户来定，这是一个例子
point_A = (530, 653)
point_B = (493, 654)


up, down = cut(img, point_A, point_B)

# cv2.imwrite('up.jpg', up)
# cv2.imwrite('down.jpg', down)
cv2.imshow('up', up)
cv2.imshow('down', down)
cv2.waitKey(0)
cv2.destroyAllWindows()
