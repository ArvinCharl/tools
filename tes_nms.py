#!/user/bin/env python3
# -*- coding: utf-8 -*-
import torch
import numpy as np


def nms(boxes, scores, overlap=0.5, top_k=200):
    keep = torch.Tensor(scores.size(0)).fill_(0).long()
    if boxes.numel() == 0:
        return keep
    x1 = boxes[:, 0]
    y1 = boxes[:, 1]
    x2 = boxes[:, 2]
    y2 = boxes[:, 3]
    area = torch.mul(x2 - x1, y2 - y1)  # IoU初步准备
    v, idx = scores.sort(0)  # sort in ascending order，对应step-2，不过是升序操作，非降序
    # I = I[v >= 0.01]
    idx = idx[-top_k:]  # indices of the top-k largest vals，依然是升序的结果
    xx1 = boxes.new()
    yy1 = boxes.new()
    xx2 = boxes.new()
    yy2 = boxes.new()
    w = boxes.new()
    h = boxes.new()

    # keep = torch.Tensor()
    count = 0
    while idx.numel() > 0:  # 对应step-4，若所有pred bbox都处理完毕，就可以结束循环啦~
        i = idx[-1]  # index of current largest val，top-1 score box，因为是升序的，所有返回index = -1的最后一个元素即可
        # keep.append(i)
        keep[count] = i
        count += 1  # 不仅记数NMS保留的bbox个数，也作为index存储bbox
        if idx.size(0) == 1:
            break
        idx = idx[:-1]  # remove kept element from view，top-1已保存，不需要了~~~
        # load bboxes of next highest vals
        torch.index_select(x1, 0, idx, out=xx1)
        torch.index_select(y1, 0, idx, out=yy1)
        torch.index_select(x2, 0, idx, out=xx2)
        torch.index_select(y2, 0, idx, out=yy2)
        # store element-wise max with next highest score
        xx1 = torch.clamp(xx1, min=x1[i])  # 对应 np.maximum(x1[i], x1[order[1:]])
        yy1 = torch.clamp(yy1, min=y1[i])
        xx2 = torch.clamp(xx2, max=x2[i])
        yy2 = torch.clamp(yy2, max=y2[i])
        w.resize_as_(xx2)
        h.resize_as_(yy2)
        w = xx2 - xx1
        h = yy2 - yy1
        # check sizes of xx1 and xx2.. after each iteration
        w = torch.clamp(w, min=0.0)  # clamp函数可以去查查，类似max、mini的操作
        h = torch.clamp(h, min=0.0)
        inter = w * h
        # IoU = i / (area(a) + area(b) - i)
        # 以下两步操作做了个优化，area已经计算好了，就可以直接根据idx读取结果了，area[i]同理，避免了不必要的冗余计算
        rem_areas = torch.index_select(area, 0, idx)  # load remaining areas)
        union = (rem_areas - inter) + area[i]  # 就是area(a) + area(b) - i
        IoU = inter / union  # store result in iou，# IoU来啦~~~
        # keep only elements with an IoU <= overlap
        idx = idx[IoU.le(overlap)]  # 这一轮NMS操作，IoU阈值小于overlap的idx，就是需要保留的bbox，其他的就直接忽略吧，并进行下一轮计算

        # if count == 2:
        #     break
    print(keep, count)
    return keep, count


# def nms(dets, thresh):
#     x1 = dets[:, 0]
#     y1 = dets[:, 1]
#     x2 = dets[:, 2]
#     y2 = dets[:, 3]
#     scores = dets[:, 4]
#
#     areas = (x2 - x1 + 1) * (y2 - y1 + 1)
#     order = scores.argsort()[::-1]
#
#     keep = []
#     while order.size > 0:
#         i = order[0]
#         keep.append(i)
#         xx1 = np.maximum(x1[i], x1[order[1:]])
#         yy1 = np.maximum(y1[i], y1[order[1:]])
#         xx2 = np.minimum(x2[i], x2[order[1:]])
#         yy2 = np.minimum(y2[i], y2[order[1:]])
#
#         w = np.maximum(0.0, xx2 - xx1 + 1)
#         h = np.maximum(0.0, yy2 - yy1 + 1)
#         inter = w * h
#         ovr = inter / (areas[i] + areas[order[1:]] - inter)
#
#         inds = np.where(ovr <= thresh)[0]
#         order = order[inds + 1]
#
#     return keep


if __name__ == '__main__':
    boxes = np.loadtxt('boxes.txt')
    scores = np.loadtxt('scores.txt')
    # to tensor
    boxes = torch.from_numpy(boxes)
    scores = torch.from_numpy(scores)
    # print(boxes, '\n', scores)

    nms(boxes, scores)
