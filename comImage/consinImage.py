# -*- coding: utf-8 -*-
# !/usr/bin/env python
# @Time    : 2019/6/4 10:05
# @Author  : xhh
# @Desc    :  余弦相似度计算
# @File    : consinImage.py
# @Software: PyCharm
from PIL import Image
from numpy import average, dot, linalg


# 对图片进行统一化处理
def get_thum(image, size=(64, 64), greyscale=False):
    # 利用image对图像大小重新设置, Image.ANTIALIAS为高质量的
    image = image.resize(size, Image.ANTIALIAS)
    if greyscale:
        # 将图片转换为L模式，其为灰度图，其每个像素用8个bit表示
        image = image.convert('L')
    return image


# 计算图片的余弦距离
def image_similarity_vectors_via_numpy(image1, image2):
    image1 = get_thum(image1)
    image2 = get_thum(image2)
    images = [image1, image2]
    vectors = []
    norms = []
    for image in images:
        vector = []
        for pixel_tuple in image.getdata():
            vector.append(average(pixel_tuple))
        vectors.append(vector)
        # linalg=linear（线性）+algebra（代数），norm则表示范数
        # 求图片的范数？？
        norms.append(linalg.norm(vector, 2))
    a, b = vectors
    a_norm, b_norm = norms
    # dot返回的是点积，对二维数组（矩阵）进行计算
    res = dot(a / a_norm, b / b_norm)
    return res


image1 = Image.open(r'D:\Desktop\smi_imgs\Snipaste_2021-01-05_09-30-19.jpg')
image2 = Image.open(r'D:\Desktop\smi_imgs\Snipaste_2021-01-05_09-30-29.jpg')
image3 = Image.open(r'D:\Desktop\smi_imgs\Snipaste_2021-01-04_17-35-59.jpg')
cosin1 = image_similarity_vectors_via_numpy(image1, image2)
cosin2 = image_similarity_vectors_via_numpy(image1, image3)
cosin3 = image_similarity_vectors_via_numpy(image2, image3)
print('img1与img2图片余弦相似度', cosin1)
print('img1与img3图片余弦相似度', cosin2)
print('img2与img3图片余弦相似度', cosin3)
