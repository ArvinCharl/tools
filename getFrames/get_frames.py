import os
import cv2
import imutils

from getFrames.tool.darknet2pytorch import Darknet
from getFrames.tool.utils import *
from getFrames.tool.torch_utils import *

"""hyper parameters"""
use_cuda = True


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


class DetectionPeople:
    def __init__(self, cfgfile, weightfile):
        self.m = Darknet(cfgfile)

        # m.print_network()
        self.m.load_weights(weightfile)
        print('Loading weights from %s... Done!' % (weightfile))

        if use_cuda:
            self.m.cuda()

        self.namesfile = 'coco.names'
        self.class_names = load_class_names(self.namesfile)

    def rec_people(self, np_img):
        result = []
        sized = cv2.resize(np_img, (self.m.width, self.m.height))
        # sized = imutils.resize(img, m.width, m.height)
        sized = cv2.cvtColor(sized, cv2.COLOR_BGR2RGB)

        start = time.time()
        boxes = do_detect(self.m, sized, 0.4, 0.6, use_cuda)
        # width = np_img.shape[1]
        # height = np_img.shape[0]
        input_boxes = boxes[0]
        for idx in range(len(input_boxes)):
            box = input_boxes[idx]
            # x1 = int(box[0] * width)
            # y1 = int(box[1] * height)
            # x2 = int(box[2] * width)
            # y2 = int(box[3] * height)

            if len(box) >= 7 and self.class_names:
                cls_conf = box[5]
                cls_id = box[6]

                cls_name = self.class_names[cls_id]

                result.append({
                    cls_name: cls_conf
                })

                # print('%s: %f' % (cls_name, cls_conf))
        finish = time.time()
        # print('Predicted in %f seconds.' % (finish - start))
        print('-' * 200)
        print(result)
        return result


def main(videofile, savefile, positive_ini_threshold=0.97, negative_ini_threshold=0.97):
    video_capture = cv2.VideoCapture(videofile)
    FPS = video_capture.get(cv2.CAP_PROP_FPS)
    print('FPS: ', FPS)
    counting = 0
    negative_num_score = 0
    positive_num_score = 0
    negative_totol_score = 0
    positive_totol_score = 0
    negative_compare_img = video_capture.read()[1]
    positive_compare_img = video_capture.read()[1]
    # os.system('-1')
    while True:
        success, frame = video_capture.read()

        if not success:
            break

        counting += 1
        # print('here is counting: {}'.format(counting))

        if counting % int(FPS) == 0:
            results_p = P.rec_people(frame)

            if results_p:
                for result in results_p:
                    if 'person' not in result.keys():
                        negative_compare_score = compare_image(negative_compare_img, frame)
                        negative_totol_score += negative_compare_score
                        negative_num_score += 1

                        negative_dynamic_thresh = (int(
                            locals().get(
                                'negative_avg_score') * 100)) / 100 if 'negative_avg_score' in locals().keys() else negative_ini_threshold
                        print('当前负样本动态阈值: {}'.format(negative_dynamic_thresh))

                        if negative_compare_score < negative_dynamic_thresh:
                            out_path = os.path.join(
                                savefile, 'negative_ciga_{}.jpg'.format(str(time.time()).replace('.', '_')))
                            if not os.path.exists(savefile):
                                os.makedirs(savefile)
                            cv2.imwrite(out_path, frame)
                            print('已保存负样本: {}'.format(out_path))
                            negative_compare_img = frame
                        else:
                            negative_avg_score = negative_totol_score / negative_num_score
                            # print('当前负样本平均阈值: {}'.format(negative_avg_score))
                        break
                    else:
                        positive_compare_score = compare_image(positive_compare_img, frame)
                        positive_totol_score += positive_compare_score
                        positive_num_score += 1

                        positive_dynamic_thresh = (int(
                            locals().get(
                                'positive_avg_score') * 100)) / 100 if 'positive_avg_score' in locals().keys() else positive_ini_threshold
                        print('当前正样本动态阈值: {}'.format(positive_dynamic_thresh))

                        if positive_compare_score < positive_dynamic_thresh:
                            out_path = os.path.join(
                                savefile, 'positive_ciga_{}.jpg'.format(str(time.time()).replace('.', '_')))
                            if not os.path.exists(savefile):
                                os.makedirs(savefile)
                            cv2.imwrite(out_path, frame)
                            print('已保存正样本: {}'.format(out_path))
                            positive_compare_img = frame
                        else:
                            positive_avg_score = positive_totol_score / positive_num_score
                            # print('当前正样本平均阈值: {}'.format(positive_avg_score))
                        break
            else:
                negative_compare_score = compare_image(negative_compare_img, frame)
                negative_totol_score += negative_compare_score
                negative_num_score += 1

                negative_dynamic_thresh = (int(
                    locals().get(
                        'negative_avg_score') * 100)) / 100 if 'negative_avg_score' in locals().keys() else negative_ini_threshold
                print('当前负样本动态阈值: {}'.format(negative_dynamic_thresh))

                if negative_compare_score < negative_dynamic_thresh:
                    out_path = os.path.join(
                        savefile, 'negative_fire_{}.jpg'.format(str(time.time()).replace('.', '_')))
                    if not os.path.exists(savefile):
                        os.makedirs(savefile)
                    cv2.imwrite(out_path, frame)
                    print('已保存负样本: {}'.format(out_path))
                    negative_compare_img = frame
                else:
                    negative_avg_score = negative_totol_score / negative_num_score
                    # print('当前负样本平均阈值: {}'.format(negative_avg_score))

    video_capture.release()


if __name__ == '__main__':
    # img = cv2.imread('../Snipaste_2021-01-08_11-37-36.jpg')
    # P = DetectionPeople('yolov4-tiny.cfg', 'yolov4-tiny.pth')
    # results_p = P.rec_people(img)
    #
    # for result in results_p:
    #     if 'person' in result.keys():
    #         print(1)

    P = DetectionPeople('yolov4-tiny.cfg', 'yolov4-tiny.pth')
    for root, dirs, files in os.walk(r'E:\c海势工作资料\智慧工地素材\ciga02'):
        for file in files:
            each_file = os.path.join(root, file)
            print(each_file)
            main(each_file, r'E:\c_data\jg\ciga\ciga_positive')
