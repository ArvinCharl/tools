#!/user/bin/env python3
# -*- coding: utf-8 -*-
import time

import cv2


# img1 = cv2.imread(r'D:\Desktop\smi_imgs\Snipaste_2021-01-05_09-30-19.jpg')
# img2 = cv2.imread(r'D:\Desktop\smi_imgs\Snipaste_2021-01-05_09-30-29.jpg')
# img3 = cv2.imread(r'D:\Desktop\smi_imgs\Snipaste_2021-01-05_09-30-38.jpg')
#
# # 计算图img1的直方图
# H1 = cv2.calcHist([img1], [1], None, [256], [0, 256])
# H1 = cv2.normalize(H1, H1, 0, 1, cv2.NORM_MINMAX, -1)  # 对图片进行归一化处理
#
# H2 = cv2.calcHist([img2], [1], None, [256], [0, 256])
# H2 = cv2.normalize(H2, H2, 0, 1, cv2.NORM_MINMAX, -1)
#
# H3 = cv2.calcHist([img3], [1], None, [256], [0, 256])
# H3 = cv2.normalize(H3, H3, 0, 1, cv2.NORM_MINMAX, -1)
#
# similarity1 = cv2.compareHist(H1, H2, 0)
# similarity2 = cv2.compareHist(H1, H3, 0)
# similarity3 = cv2.compareHist(H2, H3, 0)
#
# print(similarity1, similarity2, similarity3, sep='\n')


# 将图片转化为RGB
def make_regular_image(img, size=(64, 64)):
    gray_image = img.resize(size).convert('RGB')
    return gray_image


# 计算直方图
def hist_similar(lh, rh):
    assert len(lh) == len(rh)
    hist = sum(1 - (0 if l == r else float(abs(l - r)) / max(l, r)) for l, r in zip(lh, rh)) / len(lh)
    return hist


# 计算相似度
def calc_similar(li, ri):
    calc_sim = hist_similar(li.histogram(), ri.histogram())
    return calc_sim


if __name__ == '__main__':
    start_time = time.time()

    print(time.time() - start_time)
