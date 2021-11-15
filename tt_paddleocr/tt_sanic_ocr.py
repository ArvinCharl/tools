#!/user/bin/env python3
# -*- coding: utf-8 -*-
import base64
import traceback

import cv2
import numpy as np
from PIL import Image
from sanic import Sanic, response
from sanic.response import json
from cors import add_cors_headers
from options import setup_options

app = Sanic("My OCR app")

# 加载ocr模型
from paddleocr import PaddleOCR, draw_ocr

ocr = PaddleOCR()


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


def image_to_base64(image_np):
    """
    把输入图片按base64编码
    """
    image = cv2.imencode('.jpg', image_np)[1]
    image_code = base64.b64encode(image).decode()

    return image_code


@app.route('/', methods=['GET', 'POST'])
async def index(request):
    return json({"Here is Nothing~."})


@app.route('/ocr', methods=['POST'])
async def tt_ocr(request):
    try:
        # 获取数据
        req_json = request.json
        imgbase64 = req_json['imageBase64']
        do_img = base64_to_image(imgbase64)

        # 处理图片
        img_result = ocr.ocr(do_img)

        # 画图
        boxes = [line[0] for line in img_result]
        txts = [line[1][0] for line in img_result]
        scores = [line[1][1] for line in img_result]
        done_img = draw_ocr(do_img, boxes, txts, scores, font_path='/path/to/PaddleOCR/doc/fonts/simfang.ttf')

        # out图片转base64
        imgbase64 = image_to_base64(done_img)

        ret_data = {
            'out_imageBase64': imgbase64
        }

        return response.json(ret_data)
    except:
        traceback.print_exc()


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000)
    # Add OPTIONS handlers to any route that is missing it
    app.register_listener(setup_options, "before_server_start")
    # Fill in CORS headers
    app.register_middleware(add_cors_headers, "response")
