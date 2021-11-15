import os
import traceback

import cv2
import imutils
import time

from getFrames.get_frames import compare_image
from get_url import get_camera_url



def image_get_from_video(video_path, positive_ini_threshold=0):
    video_capture = cv2.VideoCapture(video_path)
    FPS = video_capture.get(cv2.CAP_PROP_FPS)
    print('FPS: ', FPS)
    counting = 0
    num = 0

    positive_totol_score = 0
    positive_num_score = 0
    positive_compare_img = video_capture.read()[1]
    while True:
        # 抽帧传入队列
        success, frame = video_capture.read()
        if not success:
            break
        counting += 1
        x = round(8 / 1)
        if counting % x == 0:
            positive_compare_score = compare_image(positive_compare_img, frame)
            positive_totol_score += positive_compare_score
            positive_num_score += 1

            positive_dynamic_thresh = locals().get(
                'positive_avg_score') if 'positive_avg_score' in locals().keys() else positive_ini_threshold
            print('当前正样本动态阈值: {}'.format(positive_dynamic_thresh))

            if positive_compare_score < positive_dynamic_thresh:
                cv2.imwrite(
                    r'E:\c_data\jg\fire\new\fire_{}.jpg'.format(str(time.time()).replace('.', '_')),
                    frame)
                num += 1
                print('num:', num)
                positive_compare_img = frame
            else:
                positive_avg_score = positive_totol_score / positive_num_score
                # print('当前正样本平均阈值: {}'.format(positive_avg_score))

    video_capture.release()


def image_get_from_stream(stream_id, positive_ini_threshold=0):
    counting = 0
    num = 1
    while True:
        try:
            stream = get_camera_url(stream_id)
            cap = cv2.VideoCapture(stream)
            positive_totol_score = 0
            positive_num_score = 0
            positive_compare_img = cap.read()[1]
            while True:
                try:
                    # 抽帧传入队列
                    success, frame = cap.read()
                    if not success:
                        break
                    counting += 1
                    x = round(8 / 1)
                    if counting % x == 0:
                        positive_compare_score = compare_image(positive_compare_img, frame)
                        positive_totol_score += positive_compare_score
                        positive_num_score += 1

                        positive_dynamic_thresh = (int(
                            locals().get(
                                'positive_avg_score') * 100)) / 100 if 'positive_avg_score' in locals().keys() else positive_ini_threshold
                        print('当前正样本动态阈值: {}'.format(positive_dynamic_thresh))

                        if positive_compare_score < positive_dynamic_thresh:
                            cv2.imwrite(
                                r'E:\c_data\jg\fire\new\fire_{}_{}.jpg'.format(num, str(time.time()).replace('.', '_')),
                                frame)
                            num += 1
                            print('num:', num)
                            positive_compare_img = frame
                        else:
                            positive_avg_score = positive_totol_score / positive_num_score
                            # print('当前正样本平均阈值: {}'.format(positive_avg_score))


                except Exception:
                    print(traceback.print_exc())
                    time.sleep(3)
                    break
        except:
            print(traceback.print_exc())
            time.sleep(3)


if __name__ == '__main__':
    vid_path = r'E:\c海势工作资料\智慧工地素材\fire\new'
    for vid in os.listdir(vid_path):
        vid_file = os.path.join(vid_path, vid)
        image_get_from_video(vid_file)
