# -*- coding: utf-8 -*-
from getFrameAndShow.tool_visualization import draw_text_on_image_array
import base64
import json
import cv2
import requests

# video = cv2.VideoCapture("Video_2020-05-20_114939.wmv")
video = cv2.VideoCapture("https://hls01open.ys7.com/openlive/1da763688ac5488e9f67ae93d20f200b.hd.m3u8")
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

fourcc = cv2.VideoWriter_fourcc(*'MPV4')
done_video_path = 'out_wdb.mp4'
videoWriter = cv2.VideoWriter(done_video_path, fourcc, 24, (w, h))

while True:
    try:
        success, frame = video.read()

        if not success:
            break

        counting += 1
        print(counting)

        videoWriter.write(frame)

        if counting == 14400:
            break
    except:
        pass

# 释放视频写入器
videoWriter.release()
