#!/user/bin/env python3
# -*- coding: utf-8 -*-

# import pixellib
from pixellib.instance import instance_segmentation
import time

segment_image = instance_segmentation()
segment_image.load_model("mask_rcnn_coco.h5")
start_time = time.time()
segment_image.segmentImage("Snipaste_2021-01-08_11-37-36.jpg", extract_segmented_objects=True,
                           save_extracted_objects=True)
# print(time.time() - start_time)
import time

import cv2
import numpy as np
from pixellib.tune_bg import alter_bg

change_bg = alter_bg(model_type="pb")
change_bg.load_pascalvoc_model("mask_person/xception_pascalvoc.pb")
# change_bg.change_bg_img(f_image_path = "Snipaste_2021-01-08_11-37-36.jpg",b_image_path = "Lark20200923-110622.jpeg", output_image_name="new_img.jpg")
start_time = time.time()
img = cv2.imread("Snipaste_2021-01-08_11-37-36.jpg")
seg_image = change_bg.segmentAsPascalvoc(img, process_frame=True)
print(seg_image[0])
# target_class = change_bg.target_obj('person')
# seg_image[1][seg_image[1] != target_class] = 0
# b_channel, g_channel, r_channel = cv2.split(seg_image[1])
# alpha_channel = np.ones(b_channel.shape, dtype=b_channel.dtype) * 255
# img_BGRA = cv2.merge((b_channel, g_channel, r_channel, alpha_channel))
# print(img_BGRA)
# print(img_BGRA.shape)
# cv2.imwrite('look.png', img_BGRA)
print(time.time() - start_time)

# import cv2
# import numpy as np
# import imutils
#
# x = cv2.imread('look.png', cv2.IMREAD_UNCHANGED)
# print(x)
#
#
# x[np.all(x[:, :, 0:3] == (0, 0, 0), 2)] = 0
#
# print(x.shape)
#
# y = cv2.imread('Snipaste_2021-01-08_11-37-36.jpg', cv2.IMREAD_UNCHANGED)
# y_b_channel, y_g_channel, y_r_channel = cv2.split(y)
# y_alpha_channel = np.ones(y_b_channel.shape, dtype=y_b_channel.dtype) * 255
# y_BGRA = cv2.merge((y_b_channel, y_g_channel, y_r_channel, y_alpha_channel))
# y = cv2.resize(y_BGRA, (x.shape[1], x.shape[0]))
# z = cv2.bitwise_and(x, y)
# print(z.shape)
# cv2.imwrite('z.png', z)
# cv2.imshow('img', z)
# cv2.waitKey(-1)
