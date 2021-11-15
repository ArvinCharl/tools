import time

import numpy as np
import cv2


def img2byt(img):
    byt = img.tobytes() + np.array(img.shape, dtype=np.int32).tobytes()
    return byt


def byt2img(byt, batch=False):
    nparr = np.frombuffer(byt[:-12 if not batch else -16], dtype=np.uint8).reshape(
        tuple(np.frombuffer(byt[-12 if not batch else -16:], dtype=np.int32)))
    return nparr


if __name__ == '__main__':
    for i in range(10):

        img = cv2.imread('../yolov5/tes_imgs/2/162667563619564_P8618326.jpeg.jpg')
        start_time = time.time()
        byt = img2byt(img)
        print(f'img2byt cost : {time.time() - start_time}')

        start_time2 = time.time()
        np_img = byt2img(byt)
        # cv2.imwrite('byt2img.jpg', np_img)
        print(f'byt2img cost : {time.time() - start_time2}')
        print('*' * 200)
