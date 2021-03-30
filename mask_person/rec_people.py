#!/user/bin/env python3
# -*- coding: utf-8 -*-
import cv2
import time
from tool.darknet2pytorch import Darknet
from tool.utils import *
from tool.torch_utils import *

"""hyper parameters"""
use_cuda = False


class Detection:
    def __init__(self, cfgfile, weightfile, labelfile):
        self.m = Darknet(cfgfile)
        self.m = self.m.eval()

        # m.print_network()
        self.m.load_weights(weightfile)
        print('Loading weights from %s... Done!' % (weightfile))

        if use_cuda:
            self.m.cuda()

        self.namesfile = labelfile
        self.class_names = load_class_names(self.namesfile)

    def rec_people(self, np_img):
        sized = cv2.resize(np_img, (self.m.width, self.m.height))
        # sized = imutils.resize(img, m.width, m.height)
        sized = cv2.cvtColor(sized, cv2.COLOR_BGR2RGB)

        start = time.time()
        boxes = do_detect(self.m, sized, 0.4, 0.6, use_cuda)
        width = np_img.shape[1]
        height = np_img.shape[0]
        input_boxes = boxes[0]
        # print('input_boxes:', input_boxes)
        # bboxes = {clas: [] for clas in self.class_names}
        bboxes = []
        if input_boxes:
            for idx in range(len(input_boxes)):
                box = input_boxes[idx]
                x1 = int(box[0] * width)
                y1 = int(box[1] * height)
                x2 = int(box[2] * width)
                y2 = int(box[3] * height)

                if len(box) >= 7 and self.class_names:
                    cls_conf = box[5]
                    cls_id = box[6]

                    cls_name = self.class_names[cls_id]
                    if cls_name == 'person':
                        bboxes.append((x1, y1, x2, y2))

        finish = time.time()
        print('Predicted in %f seconds.' % (finish - start))
        print(bboxes, '\n')
        if bboxes:
            people_areas = []
            for person_box in bboxes:
                person_area = (person_box[2] - person_box[0]) * (person_box[3] - person_box[1])
                people_areas.append(person_area)
            result = bboxes[people_areas.index(max(people_areas))]
        else:
            result = []
        return result


if __name__ == '__main__':
    P = Detection('models/yolov4-tiny.cfg', 'models/yolov4-tiny.pth', 'models/coco.names')

    for i in range(1):
        img = cv2.imread(r'z1.png', cv2.IMREAD_UNCHANGED)
        person_boxes = P.rec_people(img)
        print(person_boxes)

