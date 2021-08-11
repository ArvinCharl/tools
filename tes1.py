#!/user/bin/env python3
# -*- coding: utf-8 -*-
import json
import time
import cv2

import requests


def get_rtsp_url(url_list):
    rtsp_list = []
    for url in url_list:
        result = requests.get(url).text
        result = json.loads(result)
        r = result["url"]
        rtsp_list.append(r)
    print(rtsp_list)
    return rtsp_list


# play_url = eval(r).get('url')
# print(play_url)
# video_capture = cv2.VideoCapture(play_url)
#
# while True:
#     success, frame = video_capture.read()
#     if success:
#         cv2.imshow('show', frame)
#         if cv2.waitKey(25) & 0xFF == ord('q'):
#             cv2.destroyAllWindows()
#             print('Exited')
#             break
#     else:break

if __name__ == '__main__':
    url_list = [
        'http://116.228.215.13:8080/interface_mysql/getVideoURLServlet?s_camera_id=8',
        'http://116.228.215.13:8080/interface_mysql/getVideoURLServlet?s_camera_id=5',
    ]
    get_rtsp_url(url_list)
