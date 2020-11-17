# -*- coding: utf-8 -*-
import base64
import json
import cv2
import requests
from tool_visualization import draw_bounding_box_on_image_array


def ocr_server(img, billModel="通用OCR", textAngle=False, textLine=False):
    OCR_IP = 'http://172.30.0.135:7020/ocr'
    decode_image = str(base64.b64encode(cv2.imencode('.jpg', img)[1]), encoding='utf8')
    body = json.dumps({
        "billModel": billModel,
        "textAngle": textAngle,
        "textLine": textLine,
        'imgString': decode_image
    })
    content = requests.post(OCR_IP, data=body).text
    r = json.loads(content)
    return r


# video = cv2.VideoCapture("Video_2020-05-20_114939.wmv")
video = cv2.VideoCapture("banner.flv")

counting = 0
success, frame = video.read()
h, w, c = frame.shape

# Find OpenCV version
# (major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')
#
# if int(major_ver) < 3:
#     fps = video.get(cv2.cv.CV_CAP_PROP_FPS)
#     print("Frames per second using video.get(cv2.cv.CV_CAP_PROP_FPS): {0}".format(fps))
# else:
#     fps = video.get(cv2.CAP_PROP_FPS)
#     print("Frames per second using video.get(cv2.CAP_PROP_FPS) : {0}".format(fps))

# fourcc = cv2.VideoWriter_fourcc(*"mp4v")
# done_video_path = 'out_video_2020_05_20.mp4'
# videoWriter = cv2.VideoWriter(done_video_path, fourcc, 25, (w, h))

while True:
    success, frame = video.read()

    if not success:
        break

    counting += 1
    # print(counting)

    # if counting == 67:

    res = ocr_server(frame)

    draw_text_list = []
    draw_box_list = []
    draw_box_slash_list = []

    try:
        for r in res['res']:
            # r 即每个框及其信息
            boxes = r['box']
            text = r['text']

            draw_text_list.append(text)
            draw_box_list.append(boxes)
            slash = ((boxes[4] - boxes[0]) ** 2 + (boxes[5] - boxes[1]) ** 2) ** 0.5
            draw_box_slash_list.append(slash)

            # print(sorted(draw_box_slash_list, reverse=True))
            max_box_index = draw_box_slash_list.index(max(draw_box_slash_list))

            draw_text = draw_text_list[max_box_index]
            draw_box = draw_box_list[max_box_index]
            print('识别的文字: ', draw_text)
            print('该文字坐标点: ', draw_box)
            print('-' * 50)

            draw_bounding_box_on_image_array(frame, draw_box[1], draw_box[0], draw_box[5], draw_box[4], display_str_list=[draw_text])
    #
    #     #     draw_bounding_box_on_image_array(frame, boxes[1], boxes[0], boxes[5], boxes[4], display_str_list=[text])
    #
            cv2.namedWindow('pic')
            cv2.imshow('pic', frame)
            if cv2.waitKey(0) & 0xFF == ord('q'):
                break
    except Exception as e:
        print(e)
cv2.destroyAllWindows()

# 释放视频写入器
# videoWriter.release()
