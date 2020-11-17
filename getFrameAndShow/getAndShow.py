# -*- coding: utf-8 -*-
from tool_visualization import draw_text_on_image_array
import base64
import json
import cv2
import requests

# video = cv2.VideoCapture("Video_2020-05-20_114939.wmv")
video = cv2.VideoCapture("no_mask.mp4")
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

fourcc = cv2.VideoWriter_fourcc('A', 'V', 'C', '1')
done_video_path = 'out_no_mask.mp4'
videoWriter = cv2.VideoWriter(done_video_path, fourcc, 24, (w, h))

while True:
    success, frame = video.read()

    if not success:
        break

    counting += 1
    print(counting)


    videoWriter.write(frame)

# 释放视频写入器
videoWriter.release()
