import base64
import json
import numpy as np
from flask import request


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


def GlobalToBase64(file):
    with open(file, 'rb') as fileObj:
        image_data = fileObj.read()
        base64_data = base64.b64encode(image_data)
        return base64_data


def base64_to_file(input_base64_file, out_ori_file):
    with open(input_base64_file, 'r') as f:
        base64_data = f.read()
        ori_data = base64.b64decode(base64_data)
        with open(out_ori_file, 'wb') as f1:
            f1.write(ori_data)


def file_to_base64(infile, outfile):
    with open(infile, 'rb') as fileObj:
        file_data = fileObj.read()
        base64_data = base64.b64encode(file_data)
        with open(outfile, 'wb') as f:
            f.write(base64_data)
        return base64_data


#
#
# with open('no_mask.mp4', 'rb') as fileObj:    # 视频, 音频文件从base64读取后, 似乎只能先写成文件, 再读才可使用
#     file_data = fileObj.read()
#     base64_data = base64.b64encode(file_data)
#     print(base64_data.decode())
# #     # with open('no_mask.txt', 'wb') as f:
# #     #     f.write(base64_data)
# #     f = open('no_mask.txt', '')
#
# with open('no_mask.txt', 'rb') as f:
#     base64_data = f.read()
# with open('out_mask.mp4', 'wb') as f1:
#     f1.write(base64_data)
#
#
# def do_helmet():
#     post_data = request.get_data()
#     post_data = json.loads(post_data)
#     imgbase64 = post_data['img']
#     img_bytes = base64.b64decode(imgbase64)
#     img_array = np.fromstring(img_bytes, np.uint8)  # 转换np序列
#     img = cv2.imdecode(img_array, cv2.COLOR_BGR2RGB)  # 转换Opencv格式


if __name__ == '__main__':
    file_to_base64(r'tt_paddleocr/Lark20200923-110618.jpeg', 'tt_paddleocr/test.txt')
    # base64_to_file('result_pic_base64.txt', 'lllll.png')
    # import cv2
    # img = cv2.imread('llll.jpg')
    # out = image_to_base64(img)
    # print(out)
