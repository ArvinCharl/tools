# -*- coding: utf-8 -*-
import os

from getFrameAndShow.tool_visualization import draw_text_on_image_array
import base64
import json
import cv2
import requests

# video = cv2.VideoCapture("Video_2020-05-20_114939.wmv")

apple_url01 = 'http://devimages.apple.com.edgekey.net/streaming/examples/bipbop_16x9/gear5/prog_index.m3u8'
apple_url02 = 'http://devimages.apple.com.edgekey.net/streaming/examples/bipbop_4x3/gear2/prog_index.m3u8'
lihua_xiwan = 'rtsp://61.151.156.6:8554/cam/realmonitor?vcuid=xz46DizuB1CIOTV1C1S7U1&subtype=0&urlType=agentPull&manufacturer=HIKVISION&protocoltype=HIKVISION&streamType=0&token=1614037580_2e6cb92bc53ebf5452ed76ee06d7bfa8d2c31dc3&mapNet=ExtNet'
xiwan_list = [apple_url01]
while True:
    for i in xiwan_list:
        video = cv2.VideoCapture(i)
        counting = 0
        # success, frame = video.read()
        # h, w, c = frame.shape

        # Find OpenCV version
        # (major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')
        #
        # if int(major_ver) < 3:
        #     fps = video.get(cv2.cv.CV_CAP_PROP_FPS)
        #     print("Frames per second using video.get(cv2.cv.CV_CAP_PROP_FPS): {0}".format(fps))
        # else:
        #     fps = video.get(cv2.CAP_PROP_FPS)
        #     print("Frames per second using video.get(cv2.CAP_PROP_FPS) : {0}".format(fps))

        # fourcc = cv2.VideoWriter_fourcc(*'MPV4')
        # done_video_path = 'out_wdb.mp4'
        # videoWriter = cv2.VideoWriter(done_video_path, fourcc, 24, (w, h))

        while True:
            success, frame = video.read()

            if not success:
                break

            counting += 1
            print(counting)

            cv2.imshow('show', frame)

            out_file_path = 'out_pics'
            if not os.path.exists(out_file_path):
                os.makedirs(out_file_path)
            cv2.imwrite('out_pics/{}.jpg'.format(str(counting)), frame)

            if cv2.waitKey(25) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                print('Exited')
                break

            if counting == 100:
                break

# 释放视频写入器
# videoWriter.release()
