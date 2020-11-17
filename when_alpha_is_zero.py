"""
修改alpha为0处对应的像素值为0
"""
import os

import cv2
import imutils
from PIL import Image, ImageDraw, ImageFilter
import numpy

# img2 = cv2.imread('j20/10000.png', cv2.IMREAD_UNCHANGED)
# print(img2.shape)
# img2 = imutils.resize(img2, 800)
#
# print(img2)
#
# cv2.imshow('img', img2)
# cv2.waitKey(0)

imgs_path = 'j20'
img_list = os.listdir(imgs_path)
for img in img_list:
    img_path = os.path.join(imgs_path, img)
    print(img_path)
    the_img = Image.open(img_path)

# image = img1.convert("L")
# img1 = image.filter(ImageFilter.FIND_EDGES)
# img1 = img1.filter(ImageFilter.Kernel((3, 3), (-1, -1, -1, -1, 8,
#                                                -1, -1, -1, -1), 1, 0))

    w, h = the_img.size
    pix = the_img.load()
    for x in range(int(w)):
        for y in range(int(h)):
            if pix[x, y][3] == 0:
                the_img.putpixel((x, y), (0, 0, 0, 0))

    out_path = os.path.join('j20_20201105', img)
    print(out_path)

    the_img.save(out_path)
    print('----------------------------', '\n')
