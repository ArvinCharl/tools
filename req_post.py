#!/user/bin/env python3
# -*- coding: utf-8 -*-
import base64
import json
import time
import cv2
import requests
import numpy as np


def image_to_base64(image_np):
    """
    把输入图片按base64编码
    """
    image = cv2.imencode('.jpg', image_np)[1]
    image_code = str(base64.b64encode(image))[2:-1]
    # image_code = base64.b64encode(image)

    return image_code


def base64_to_image(base64_code):
    """
    输入的base64解码，还原为numpy类型
    """
    # base64解码
    img_data = base64.b64decode(base64_code)
    # 转换为np数组
    img_array = np.fromstring(img_data, np.uint8)
    # 转换成opencv可用格式
    img = cv2.imdecode(img_array, cv2.COLOR_RGB2BGR)
    return img


img_path = '20200802-175555.jpg'
img = cv2.imread(img_path)
base64_data = image_to_base64(img)

req_data = dict()
req_data["imagebase64"] = base64_data
req_data = json.dumps(req_data)

r = requests.post('https://helmet.3xmt.com/helmet', data=req_data)
r = json.loads(r.text)

out_img_base64 = r.get('imageBase64')
out_img = base64_to_image(out_img_base64)
cv2.imshow('img', out_img)
cv2.waitKey(-1)
