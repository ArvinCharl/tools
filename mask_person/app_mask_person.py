# -*- coding: UTF-8 -*-
import time
import cv2
import json
from flask import request
import numpy as np
import base64
from pixellib.tune_bg import alter_bg
from flask import Flask
from rec_people import Detection

# 初始化flask
app = Flask(__name__)

# 初始化模型
# 人形检测
P = Detection('models/yolov4-tiny.cfg', 'models/yolov4-tiny.pth', 'models/coco.names')

# mask
change_bg = alter_bg(model_type="pb")
change_bg.load_pascalvoc_model("xception_pascalvoc.pb")


@app.route('/do_mask', methods=["POST"])
def do_mask():
    # 接收数据
    post_data = request.get_data()
    post_data = json.loads(post_data)
    imgbase64 = post_data['img']
    img_bytes = base64.b64decode(imgbase64)
    img_array = np.fromstring(img_bytes, np.uint8)  # 转换np序列
    img = cv2.imdecode(img_array, cv2.COLOR_BGR2RGB)  # 转换Opencv格式

    # 处理图片
    z = process_pic(img)

    # 返回结果
    z_base64 = cv2.imencode('.png', z)[1]
    z_base64 = str(base64.b64encode(z_base64))[2:-1]

    result = {
        "img": z_base64
    }
    with open('result_pic_base64.txt', 'w')as f:
        f.write(z_base64)

    return result


def process_pic(img):
    """
    处理图片
    :param img:
    :return:
    """
    # 先进行目标人形检测
    # max_person_box = P.rec_people(img)
    # roi = img[max_person_box[1]:max_person_box[3], max_person_box[0]:max_person_box[2]]
    # img = roi

    # 推理图片
    seg_image = change_bg.segmentAsPascalvoc(img, process_frame=True)
    target_class = change_bg.target_obj('person')
    seg_image[1][seg_image[1] != target_class] = 0

    # 推理结果增加alpha通道
    b_channel, g_channel, r_channel = cv2.split(seg_image[1])
    alpha_channel = np.ones(b_channel.shape, dtype=b_channel.dtype) * 255
    img_BGRA = cv2.merge((b_channel, g_channel, r_channel, alpha_channel))

    # 黑色部分透明
    img_BGRA[np.all(img_BGRA[:, :, 0:3] == (0, 0, 0), 2)] = 0

    # 原图增加alpha通道
    y_b_channel, y_g_channel, y_r_channel = cv2.split(img)
    y_alpha_channel = np.ones(y_b_channel.shape, dtype=y_b_channel.dtype) * 255
    y_BGRA = cv2.merge((y_b_channel, y_g_channel, y_r_channel, y_alpha_channel))

    # 推理结果和原图合并
    y = cv2.resize(y_BGRA, (img_BGRA.shape[1], img_BGRA.shape[0]))
    z = cv2.bitwise_and(img_BGRA, y)

    # cv2.imwrite('max_person.png', z)

    return z


if __name__ == '__main__':
    # app.run(
    #     host='0.0.0.0',
    #     port=2311,
    #     debug=True
    # )
    img = cv2.imread('Snipaste_2021-03-10_17-51-29.jpg', cv2.IMREAD_UNCHANGED)
    z = process_pic(img)
    cv2.imshow('img', z)
    cv2.waitKey(-1)
