#!/user/bin/env python3
# -*- coding: utf-8 -*-
import os
import cv2
import imutils


def resize_img(np_img, width=800):
    if np_img.shape[1] > width:
        np_img = imutils.resize(np_img, width)
    return np_img


if __name__ == '__main__':
    imgs_path = r'E:\c_data\jg\no_helmet-helmet\ori-ciga\2'
    # for dir in os.listdir(imgs_path):
    #     dir_path = os.path.join(imgs_path, dir)
    #     print(dir_path)

    for img in os.listdir(imgs_path):
        img_path = os.path.join(imgs_path, img)
        print(img_path)
        # resize
        if not img_path.endswith('xml'):
            out_img = cv2.imread(img_path)
            out_img = resize_img(out_img, 800)

            cv2.imwrite(os.path.join(imgs_path, img), out_img)

        # delete xml file
        # if img_path.endswith('xml'):
        #     os.remove(img_path)
