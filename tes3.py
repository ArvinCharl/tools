#!/user/bin/env python3
# -*- coding: utf-8 -*-
import time

import cv2

stream_path = 'ezopen://open.ys7.com/G24549802/1.hd.live'

videocapture = cv2.VideoCapture(stream_path)
num = 0
while True:
    success, frame = videocapture.read()

    if not success:
        break
    cv2.imwrite(f'look_delay/{time.strftime(r"%Y%m%d%H%M%S", time.localtime())}.jpg', frame)
    # num += 1
