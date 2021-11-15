#!/user/bin/env python3
# -*- coding: utf-8 -*-
import math
import cv2
import time
import paddlehub as hub

video_capature = cv2.VideoCapture(0)


def image_get(q, stream, timeout=3):
    while True:
        try:
            cap = cv2.VideoCapture(stream)
            idx = 0
            while True:
                try:
                    # 计数第几帧
                    ret = cap.grab()
                    if ret:
                        idx += 1
                        # 将指定帧投入队列等待推理
                        if idx >= 25:
                            ret, frame = cap.retrieve()
                            if ret:
                                # frame = imutils.resize(frame, 800)
                                q.put(frame)
                                q.get() if q.qsize() > 1 else time.sleep(0.01)
                                idx = 0

                    else:
                        time.sleep(timeout)
                        break
                except Exception:
                    time.sleep(timeout)
                    break
        except:
            time.sleep(timeout)


def det(frame):
    t1 = time.time()
    # frame = q.get()
    res = module.predict(
        img=frame,
        visualization=True,
        save_path='keypoint_output')
    print(res)
    print(f'cost: {(t := (time.time() - t1))}, fps: {1 / t}')

    if (p_left_ := res['all_peaks'][7]):
        p_left = (int(p_left_[0][0]), int(p_left_[0][1]))
    elif (p_right_ := res['all_peaks'][4]):
        p_right = (int(p_right_[0][0]), int(p_right_[0][1]))
    else:
        p_left = ()
        p_right = ()

    # cv2.line(frame, p_left, p_right, color=(0, 0, 255), thickness=3)
    # cv2.imwrite(f'{str(time.time()).replace(".", "_")}.jpg', frame)
    return p_left, p_right


def getDist_P2P(Point0, PointA):
    """
    求两点之间距离
    :param Point0:
    :param PointA:
    :return:
    """
    distance = math.pow((Point0[0] - PointA[0]), 2) + math.pow((Point0[1] - PointA[1]), 2)
    distance = math.sqrt(distance)
    return distance


if __name__ == '__main__':
    # module = hub.Module(name="openpose_body_estimation", version="1.0.0")
    # module = hub.Module(name="openpose_body_estimation")
    module = hub.Module(name="openpose_hands_estimation")

    img1_path = 'out_img5.jpg'
    img2_path = 'out_img6.jpg'
    np_img1 = cv2.imread(img1_path)
    np_img2 = cv2.imread(img2_path)
    out_img1_pleft, out_img1_pright = det(np_img1)
    out_img2_pleft, out_img2_pright = det(np_img2)
    left_distance = getDist_P2P(out_img1_pleft, out_img2_pleft)
    right_distance = getDist_P2P(out_img1_pright, out_img2_pright)
    print(f'left distance: {left_distance}')
    print(f'right distance: {right_distance}')
    cv2.line(np_img1, out_img1_pleft, out_img2_pleft, color=(0, 0, 255), thickness=3)
    cv2.line(np_img2, out_img1_pright, out_img2_pright, color=(0, 0, 255), thickness=3)
    cv2.imwrite(f'out_{img1_path.split(".")[0]}.jpg', np_img1)
    cv2.imwrite(f'out_{img2_path.split(".")[0]}.jpg', np_img2)
    # x = getDist_P2P((348, 380), (356, 348))
    # print(x)
