import os
import traceback

import cv2
import imutils
import time


def compare_image(img1, img2):
    """
    处理两张图片相似度对比
    :param img1:
    :param img2:
    :return:对比分数, 从0-1
    """
    # 计算图片的直方图
    H1 = cv2.calcHist([img1], [1], None, [256], [0, 256])
    H1 = cv2.normalize(H1, H1, 0, 1, cv2.NORM_MINMAX, -1)  # 对图片进行归一化处理

    # 计算图img2的直方图
    H2 = cv2.calcHist([img2], [1], None, [256], [0, 256])
    H2 = cv2.normalize(H2, H2, 0, 1, cv2.NORM_MINMAX, -1)

    # 利用compareHist（）进行比较相似度
    similarity = cv2.compareHist(H1, H2, 0)

    return similarity


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


if __name__ == '__main__':
    image_get_from_video(r'E:\c海势工作资料\智慧工地素材\fire\徐汇南部医疗生活区_20210616164412_20210616164553.mp4')
