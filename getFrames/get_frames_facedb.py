import os
import cv2
import imutils

video_capture = cv2.VideoCapture(r'E:\c_HISW_work_file\智慧工地素材\中共一大\ciga1.mp4')
FPS = video_capture.get(cv2.CAP_PROP_FPS)
print('FPS: ', FPS)
counting = 0
num = 0

# the_compare_img = video_capture.read()[1]
# os.system('-1')
while True:
    success, frame = video_capture.read()

    if not success:
        break

    counting += 1
    print('counting', counting)

    x = round(FPS / 1)
    if counting % x == 0:
        num += 1
        print('num:', num)
    if num == 10:
        break

    # print('here is counting: {}'.format(counting))

video_capture.release()
