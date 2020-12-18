#!/user/bin/env python3
# -*- coding: utf-8 -*-
import os
from PIL import Image
import imutils
import cv2


def img_resize(infile, width, outfile='', ):
    """
    :param infile:
    :param outfile:
    :param width:
    :return:
    """
    img = cv2.imread(infile)
    print(img.shape)
    img = imutils.resize(img, width)
    cv2.imwrite(outfile, img)
    out_img = cv2.imread(outfile)
    print(out_img.shape)
    cv2.imshow('ccc', out_img)
    cv2.waitKey(3000)


def get_size(file):
    # 获取文件大小:KB
    size = os.path.getsize(file)
    print(size / 1024)
    return size / 1024


def get_outfile(infile, outfile):
    if outfile:
        return outfile
    dir, suffix = os.path.splitext(infile)
    outfile = '{}-out{}'.format(dir, suffix)
    print(outfile)
    return outfile


def compress_image(infile, outfile='', mb=10, step=10, quality=80):
    """不改变图片尺寸压缩到指定大小
    :param infile: 压缩源文件
    :param outfile: 压缩文件保存地址
    :param mb: 压缩目标，KB
    :param step: 每次调整的压缩比率
    :param quality: 初始压缩比率
    :return: 压缩文件地址，压缩文件大小
    """
    o_size = get_size(infile)
    if o_size <= mb:
        return infile
    outfile = get_outfile(infile, outfile)
    while o_size > mb:
        im = Image.open(infile)
        im.save(outfile, quality=quality)
        if quality - step < 0:
            break
        quality -= step
        o_size = get_size(outfile)
    return outfile, get_size(outfile)


if __name__ == '__main__':
    img_resize(r'D:\Desktop\yzh\cat_yzh.jpg', 350, r'D:\Desktop\yzh\out_cat_yzh.jpg')
    compress_image(r'D:\Desktop\yzh\out_cat_yzh.jpg', r'D:\Desktop\yzh\out_out_cat_yzh.jpg')
