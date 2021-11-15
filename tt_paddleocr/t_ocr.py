#!/user/bin/env python3
# -*- coding: utf-8 -*-
from paddleocr import PaddleOCR, draw_ocr
import cv2

ocr = PaddleOCR()  # need to run only once to download and load model into memory
img_path = 'Lark20200923-110622.jpeg'
do_img = cv2.imread(img_path)
result = ocr.ocr(do_img)
print(result)

# 显示结果
from PIL import Image

# image = Image.open(img_path).convert('RGB')
boxes = [line[0] for line in result]
txts = [line[1][0] for line in result]
scores = [line[1][1] for line in result]

im_show = draw_ocr(do_img, boxes, txts, scores, font_path='/path/to/PaddleOCR/doc/fonts/simfang.ttf')
im_show = cv2.cvtColor(im_show, cv2.COLOR_BGR2RGB)
im_show = Image.fromarray(im_show)
print(type(im_show))
im_show.show('result.jpg')
