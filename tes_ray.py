#!/user/bin/env python3
# -*- coding: utf-8 -*-
import cv2

img = cv2.imread('Snipaste_2021-01-08_11-37-36.jpg', cv2.IMREAD_UNCHANGED)
cv2.cvtColor(img, cv2.COLOR_RGB2RGBA)
print(img.shape)

