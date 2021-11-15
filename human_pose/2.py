#!/user/bin/env python3
# -*- coding: utf-8 -*-
# import cv2
# from skimage.feature import match_template
#
# img1 = cv2.imread('583a9e3c5ec94b62af6618af5c5dd1a6.png')
# img2 = cv2.imread('583a9e3c5ec94b62af6618af5c5dd1a6.png')
# result = match_template(img1, img2)
# print(result)


# !/usr/bin/env python2

import cv2


def intersected(rc1, rc2):
    if rc1[0] > rc2[2]: return False
    if rc1[1] > rc2[3]: return False
    if rc2[0] > rc1[2]: return False
    if rc2[1] > rc1[3]: return False
    return True


def segment(grey):
    _, thresh = cv2.threshold(grey, 20, 255, cv2.THRESH_BINARY_INV)
    countours, hierarchy = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    rcs = map(cv2.boundingRect, countours)
    rcs = [(rc[0], rc[1], rc[0] + rc[2], rc[1] + rc[3]) for rc in rcs]

    # clustering
    clusters = range(len(rcs))
    for i, rc in enumerate(rcs):
        for j, irc in enumerate(rcs[i + 1:]):
            idx = i + j + 1
            if clusters[idx] != clusters[i] and intersected(rc, irc):
                if clusters[idx] > clusters[i]:
                    clusters[idx] = clusters[i]
                else:
                    clusters[i] = clusters[idx]

    def cluster(v):
        indices = [i for i, x in enumerate(clusters) if x == v]
        xmin = min(rcs[idx][0] for idx in indices)
        ymin = min(rcs[idx][1] for idx in indices)
        xmax = max(rcs[idx][2] for idx in indices)
        ymax = max(rcs[idx][3] for idx in indices)
        return xmin, ymin, xmax, ymax

    rcs = map(cluster, set(clusters))
    h = int(sum((rc[3] - rc[1]) for rc in rcs)) / len(rcs)
    w = thresh.shape[1]
    return sorted(rcs, key=lambda rc: int(rc[1]) / h * w + rc[0]), thresh


def main(path):
    im = cv2.imread(path)

    # segmentation
    grey = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    rcs, thresh = segment(grey)

    # drawing
    draw = im.copy()
    for i, rc in enumerate(rcs):
        cv2.rectangle(draw, rc[0:2], rc[2:4], (0, 0, 255))
        cv2.putText(draw, str(i), (rc[0], rc[3]), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 255, 0))
        # cv2.drawContours(draw, countours, i, (255, 0, 0))

    cv2.imshow(path, draw)
    cv2.imwrite(path + '_draw.png', draw)

    return thresh, rcs


if __name__ == '__main__':
    main('583a9e3c5ec94b62af6618af5c5dd1a6.png')
    main('d1ff5df9ce2d4b50a0f61e5bc1571b8d.png')
    cv2.waitKey(0)
