#!/usr/bin/env python
# coding: utf-8
import multiprocessing
import traceback

import cv2
import time
import subprocess as sp
import multiprocessing as mp

# import psutil
# from test import draw_pipe_box

# fps，width，height可配置
from yolo_detect import Detection


class StreamPusher(object):
    def __init__(self, cap, rtmpUrl=None, fps=2, width=704, height=576):
        # Get video information
        # fps = int(cap.get(cv2.CAP_PROP_FPS))
        print('fps: ', fps)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        # ffmpeg command
        command = ['ffmpeg',
                   '-y',
                   '-re',
                   '-f', 'rawvideo',
                   '-vcodec', 'rawvideo',
                   '-pix_fmt', 'bgr24',
                   '-s', "{}x{}".format(width, height),
                   # '-vf', "scale=1920:1080/a"
                   '-r', str(fps),
                   '-i', '-',
                   '-c:v', 'libx264',
                   '-pix_fmt', 'yuv420p',
                   '-preset', 'ultrafast',
                   '-f', 'flv',
                   rtmpUrl]

        # 配置向os传递命令的管道
        self.p = sp.Popen(command, stdin=sp.PIPE)

    def push_frame(self, frame):
        # 把内容放入管道，向服务器推送
        try:
            self.p.stdin.write(frame.tostring())
        except:
            time.sleep(0.01)
            self.p.stdin.write(frame.tostring())


def image_put(q, video_path):
    cap = cv2.VideoCapture(video_path)
    while True:
        try:
            success, frame = cap.read()
            if success:
                # print('success')
                q.put(frame)
                # print('*' * 20, q.qsize())
                q.get() if q.qsize() > 1 else time.sleep(0.01)
            else:
                # print('failed')
                cap = cv2.VideoCapture(video_path)
                time.sleep(3)
        except:
            traceback.print_exc()
            time.sleep(3)


def det(q, result_img_q, cfg, pth, names):
    detector = Detection(cfg, pth, names)
    while True:
        try:
            frame = q.get()
            detector.do_detect(frame)
            result_img_q.put(frame)
        except:
            traceback.print_exc()
            time.sleep(3)


def push_streams(q, pusher):
    while True:
        try:
            frame = q.get()
            pusher.push_frame(frame)
        except:
            traceback.print_exc()
            time.sleep(3)


def run_single_camera(pusher, cfg, pth, names):
    mp.set_start_method(method='fork')  # init
    origin_img_q = mp.Queue(maxsize=4)
    result_img_q = mp.Queue(maxsize=4)
    processes = [mp.Process(target=image_put, args=(origin_img_q, video_path)),
                 mp.Process(target=det, args=(origin_img_q, result_img_q, cfg, pth, names)),
                 mp.Process(target=push_streams, args=(result_img_q, pusher))]

    # [setattr(process, "daemon", True) for process in processes]
    [process.start() for process in processes]
    [process.join() for process in processes]


def run_multi_camera():
    user_name, user_pwd = "admin", "admin123456"
    camera_ip_l = [
        "172.20.114.196",  # ipv4
        "[fe80::3aaf:29ff:fed3:d260]",  # ipv6
    ]

    mp.set_start_method(method='spawn')  # init
    queues = [mp.Queue(maxsize=4) for _ in camera_ip_l]

    processes = []
    for queue, camera_ip in zip(queues, camera_ip_l):
        processes.append(mp.Process(target=image_put, args=(queue, user_name, user_pwd, camera_ip)))
        processes.append(mp.Process(target=image_get_push, args=(queue, camera_ip)))

    for process in processes:
        process.daemon = True
        process.start()
    for process in processes:
        process.join()


if __name__ == '__main__':
    video_path = 'rtmp://58.200.131.2:1935/livetv/hunantv'
    cap = cv2.VideoCapture(video_path)
    pusher = StreamPusher(cap, rtmpUrl="rtmp://172.30.0.145:1935/rtmplive/home")

    run_single_camera(pusher, 'models/yolov4-tiny.cfg', 'checkpoints/yolov4-tiny.pth', 'models/coco.names')

    # cap.release()
