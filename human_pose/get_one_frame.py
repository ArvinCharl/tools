#!/user/bin/env python3
# -*- coding: utf-8 -*-
import time

import cv2

video_capature = cv2.VideoCapture(0)

while True:
    success, frame = video_capature.read()
    if not success:break
    cv2.imshow('show', frame)
    key = cv2.waitKey(1)
    if key == ord('s'):
        cv2.imwrite(f'{str(time.time()).replace(".", "_")}.jpg', frame)
