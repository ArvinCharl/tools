#!/user/bin/env python3
# -*- coding: utf-8 -*-
import cv2

input_video_file = r'out_Video_2021-08-26_172331.mp4'
out_video = r'out_out_Video_2021-08-26_172331.mp4'

video = cv2.VideoCapture(input_video_file)
counting = 0
success, frame = video.read()
h, w, c = frame.shape

# # Find OpenCV version
(major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')
if int(major_ver) < 3:
    fps = video.get(cv2.cv.CV_CAP_PROP_FPS)
    print("Frames per second using video.get(cv2.cv.CV_CAP_PROP_FPS): {0}".format(fps))
else:
    fps = video.get(cv2.CAP_PROP_FPS)
    print("Frames per second using video.get(cv2.CAP_PROP_FPS) : {0}".format(fps))

# fps = 25

fourcc = cv2.VideoWriter_fourcc(*'MPV4')

videoWriter = cv2.VideoWriter(out_video, fourcc, fps, (w, h))

while True:
    success, frame = video.read()

    if not success:
        break

    counting += 1
    print(counting)
    if counting % 3 == 0:
        videoWriter.write(frame)


# if counting >= fps * 45:
    #     videoWriter.write(frame)
    #
    # if counting >= fps * 85:
    #     break

# 释放视频写入器
videoWriter.release()
