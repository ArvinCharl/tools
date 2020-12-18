import os

import cv2


class CompareImage(object):

    def compare_image(self, image_1, image_2):
        # image_1 = cv2.imread(self.image_1_path, 0)
        # image_2 = cv2.imread(self.image_2_path, 0)
        commutative_image_diff = self.get_image_difference(image_1, image_2)

        # if commutative_image_diff < self.minimum_commutative_image_diff:
        #     print("Matched")
        #     return commutative_image_diff
        return commutative_image_diff
        # return 10000  # random failure value

    @staticmethod
    def get_image_difference(image_1, image_2):
        first_image_hist = cv2.calcHist([image_1], [0], None, [256], [0, 256])
        second_image_hist = cv2.calcHist([image_2], [0], None, [256], [0, 256])

        img_hist_diff = cv2.compareHist(first_image_hist, second_image_hist, cv2.HISTCMP_BHATTACHARYYA)
        img_template_probability_match = \
            cv2.matchTemplate(first_image_hist, second_image_hist, cv2.TM_CCOEFF_NORMED)[0][0]
        img_template_diff = 1 - img_template_probability_match

        # taking only 10% of histogram diff, since it's less accurate than template method
        commutative_image_diff = (img_hist_diff / 10) + img_template_diff
        return commutative_image_diff


video_capture = cv2.VideoCapture(r'E:\c_HISW_work_file\机型识别\视频素材\j10(1)~1.mp4')
counting = 0
num = 0
save_path = 'smilar'
img1 = video_capture.read()[1]
while True:
    success, frame = video_capture.read()

    if not success:
        break

    counting += 1
    # print('here is counting: {}'.format(counting))

    compare_image = CompareImage()
    image_difference = compare_image.compare_image(img1, frame)

    if image_difference <= 0.3:
        img1 = frame
        continue
    else:
        print(image_difference)
        num += 1
        print('here is num:{}'.format(num))
        out_path = os.path.join(save_path, 'smilar_%s.jpg' % num)
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        cv2.imwrite(out_path, frame)
        img1 = frame

    # if counting % 12 == 0:
    #     num += 1
    #     print(num)
    #     out_path = os.path.join(save_path, 'smilar_%s.jpg' % num)
    #     if not os.path.exists(out_path):
    #         os.makedirs(out_path)
    #     cv2.imwrite(out_path, frame)

    if num == 100:
        break

video_capture.release()
