#!/user/bin/env python3
# -*- coding: utf-8 -*-
import cv2
import base64
import json
import time
import numpy

from flask import Flask, request

app = Flask(__name__)


def base64_to_image(base64_code):
    """
    输入的base64解码，还原为numpy类型
    """
    # base64解码
    img_data = base64.b64decode(base64_code)
    # 转换为np数组
    img_array = numpy.fromstring(img_data, numpy.uint8)
    # 转换成opencv可用格式
    img = cv2.imdecode(img_array, cv2.COLOR_RGB2BGR)
    return img


@app.route('/123', methods=['GET', 'POST'])
def index():
    a = request.get_data()
    dict1 = json.loads(a)
    req_token = dict1["token"]
    req_algorithmInstanceId = dict1["algorithmInstanceId"]
    req_eventType = dict1["eventType"]
    req_data = dict1["data"]

    req_cameraId = req_data["cameraId"]
    req_violateType = req_data["violateType"]
    req_violateDescription = req_data["violateDescription"]
    req_imageBase64 = req_data["imageBase64"][0]
    req_img = base64_to_image(req_imageBase64)
    cv2.imwrite('heluni_tes/{}.jpg'.format(time.strftime(r"%Y%m%d-%H%M%S", time.localtime())), req_img)
    time.sleep(0.5)
    req_videoBase64 = req_data["videoBase64"]
    req_time = req_data["time"]
    req_extensionData = req_data["extensionData"]
    print(
        f'token: {req_token} "\n" algorithmInstanceId: {req_algorithmInstanceId} "\n" eventType: {req_eventType} "\n" cameraId: {req_cameraId} "\n" violateType: {req_violateType} "\n" violateDescription: {req_violateDescription} "\n" videoBase64: {req_videoBase64} "\n" time: {req_time} "\n" extensionData: {req_extensionData} "\n"')
    return 'OK'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8972)
