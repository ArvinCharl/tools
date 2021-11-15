import os
import time

import cv2
import numpy
save_Dir = r'./'
video_path = 0
cap = cv2.VideoCapture(video_path)   #调取摄像头
bs = cv2.createBackgroundSubtractorKNN(dist2Threshold=8000, detectShadows=True)
# bs = cv2.createBackgroundSubtractorMOG2(detectShadows=False)
index = 0
frames_num = int(cap.get(7))
while True:
    ret, frame = cap.read()
    if not ret:break
    t1 = time.time()
    # fgmask = cv2.cvtColor(bs.apply(frame), cv2.COLOR_GRAY2RGB)
    # print(time.time() - t1)
    #
    # h,w,c = frame.shape
    # fgmask = numpy.concatenate((frame, fgmask), axis=1)
    # fgmask = cv2.resize(fgmask,(1920,540))
    # cv2.imshow('mog', fgmask)
    cv2.imshow('mog', frame)

    k = cv2.waitKey(500)
    if k == 27:
        break
    elif k == 32:
        while cv2.waitKey(0) != 32:
            z = cv2.waitKey(0)
            if z == 13:
                img_name = os.path.join(save_Dir,f'{index}.jpg')
                cv2.imwrite(img_name,frame)
                print(f'save {img_name}')
            elif z == 97:
                index = index -5 if index > 5 else 0
                cap.set(cv2.CAP_PROP_POS_FRAMES, index)
                ret, frame = cap.read()
                cv2.imshow('mog', frame)
                print('go back 5 frame ')
            elif z == 100:
                index = index + 5 if index < frames_num-5 else frames_num-1
                cap.set(cv2.CAP_PROP_POS_FRAMES, index)
                ret, frame = cap.read()
                cv2.imshow('mog', frame)
                print('go forward 5 frame ')

    index +=1






cap.release()
cv2.destroyAllWindows()
