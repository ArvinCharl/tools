# -*- coding: utf-8 -*-
# !/usr/bin/env python
# @Time    : 2019/6/4 9:51
# @Author  : xhh
# @Desc    :  opencv计算两个图片之间的直方图
# @File    : calcImage.py
# import matplotlib.pyplot as plt
import cv2

img1 = cv2.imread(r'D:\Desktop\Snipaste_2021-07-02_18-17-22.jpg')
img2 = cv2.imread(r'D:\Desktop\Snipaste_2021-07-02_18-17-36.jpg')
img3 = cv2.imread(r'D:\Desktop\Snipaste_2021-07-02_18-17-43.jpg')
img4 = cv2.imread(r'D:\Desktop\Snipaste_2021-07-02_18-17-51.jpg')

# 计算图img1的直方图
H1 = cv2.calcHist([img1], [1], None, [256], [0, 256])
H1 = cv2.normalize(H1, H1, 0, 1, cv2.NORM_MINMAX, -1)  # 对图片进行归一化处理

# 计算图img2的直方图
H2 = cv2.calcHist([img2], [1], None, [256], [0, 256])
H2 = cv2.normalize(H2, H2, 0, 1, cv2.NORM_MINMAX, -1)

# 计算图img3的直方图
H3 = cv2.calcHist([img3], [1], None, [256], [0, 256])
H3 = cv2.normalize(H3, H3, 0, 1, cv2.NORM_MINMAX, -1)

# 计算图img3的直方图
H4 = cv2.calcHist([img4], [1], None, [256], [0, 256])
H4 = cv2.normalize(H4, H4, 0, 1, cv2.NORM_MINMAX, -1)

# 利用compareHist（）进行比较相似度
similarity1 = cv2.compareHist(H1, H2, 0)
similarity2 = cv2.compareHist(H3, H4, 0)
similarity3 = cv2.compareHist(H1, H3, 0)
similarity4 = cv2.compareHist(H1, H4, 0)
print("img1和img2的相似度：", similarity1)
print("img3和img4的相似度：", similarity2)
print("img1和img3的相似度：", similarity3)
print("img1和img4的相似度：", similarity4)

# img和img1直方图展示
# plt.subplot(2, 1, 1)
# plt.plot(H1, label="img1")
# plt.plot(H2, label="img2")
# plt.plot(H3, label="img3")
# plt.legend()
# plt.savefig("./imageData/Hist.png")
# plt.show()
