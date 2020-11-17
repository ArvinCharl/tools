import cv2

video_capture = cv2.VideoCapture('smoking3.mp4')
counting = 0
num = 0
while True:
    success, frame = video_capture.read()

    if not success:
        break

    counting += 1

    if counting % 12 == 0:
        num += 1
        print(num)
        cv2.imwrite('smoke_last/smk_%s.jpg' % num, frame)

    # if num == 1:
    #     break

video_capture.release()
