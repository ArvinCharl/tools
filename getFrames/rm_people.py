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


def main(img_path):

    img = cv2.imread(img_path)

    results_p = P.rec_people(img)
    print(results_p)

    if results_p:
        for result in results_p:
            if 'person' not in result.keys():
                continue
            else:
                # os.remove(img_path)
                print('removed: {}'.format(img_path))




if __name__ == '__main__':
    # img = cv2.imread('../Snipaste_2021-01-08_11-37-36.jpg')
    # P = DetectionPeople('yolov4-tiny.cfg', 'yolov4-tiny.pth')
    # results_p = P.rec_people(img)
    #
    # for result in results_p:
    #     if 'person' in result.keys():
    #         print(1)

    P = DetectionPeople('yolov4.cfg', 'yolov4.pth')
    for root, dirs, files in os.walk(r'E:\c_data\baoshan_kitchen\baoshan20210322'):
        for file in files:
            each_file = os.path.join(root, file)
            print(each_file)
            main(each_file)

