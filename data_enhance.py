#!/user/bin/env python3
# -*- coding: utf-8 -*-
import multiprocessing
import os
import random
import time
from PIL import Image, ImageDraw
import cv2
import imutils
import numpy
import xml.dom.minidom as xdm


def make_xml(xml_data):
    doc = xdm.Document()
    root = doc.createElement('annotation')

    root.setAttribute('verified', 'yes')
    doc.appendChild(root)

    folder = doc.createElement('folder')
    filename = doc.createElement('filename')
    path = doc.createElement('path')
    folder.appendChild(doc.createTextNode('Desktop'))
    filename.appendChild(doc.createTextNode('{}'.format(xml_data.get('img_name'))))
    path.appendChild(doc.createTextNode('C:/Users/Desktop/{}'.format(xml_data.get('img_name'))))
    root.appendChild(folder)
    root.appendChild(filename)
    root.appendChild(path)

    source = doc.createElement('source')
    root.appendChild(source)
    database = doc.createElement('database')
    database.appendChild(doc.createTextNode('Unknown'))
    source.appendChild(database)

    size = doc.createElement('size')
    root.appendChild(size)
    width = doc.createElement('width')
    width.appendChild(doc.createTextNode('{}'.format(xml_data.get('bg_w'))))
    height = doc.createElement('height')
    height.appendChild(doc.createTextNode('{}'.format(xml_data.get('bg_h'))))
    depth = doc.createElement('depth')
    depth.appendChild(doc.createTextNode('3'))
    size.appendChild(width)
    size.appendChild(height)
    size.appendChild(depth)

    segmented = doc.createElement('segmented')
    segmented.appendChild(doc.createTextNode('0'))
    root.appendChild(segmented)

    object = doc.createElement('object')
    root.appendChild(object)
    name = doc.createElement('name')
    name.appendChild(doc.createTextNode('{}'.format(xml_data.get('xml_cls_name'))))
    pose = doc.createElement('human_pose')
    pose.appendChild(doc.createTextNode('Unspecified'))
    truncated = doc.createElement('truncated')
    truncated.appendChild(doc.createTextNode('0'))
    difficult = doc.createElement('difficult')
    difficult.appendChild(doc.createTextNode('0'))
    object.appendChild(name)
    object.appendChild(pose)
    object.appendChild(truncated)
    object.appendChild(difficult)
    bndbox = doc.createElement('bndbox')
    object.appendChild(bndbox)
    xmin = doc.createElement('xmin')
    xmin.appendChild(doc.createTextNode('{}'.format(xml_data.get('xml_xmin'))))
    ymin = doc.createElement('ymin')
    ymin.appendChild(doc.createTextNode('{}'.format(xml_data.get('xml_ymin'))))
    xmax = doc.createElement('xmax')
    xmax.appendChild(doc.createTextNode('{}'.format(xml_data.get('xml_xmax'))))
    ymax = doc.createElement('ymax')
    ymax.appendChild(doc.createTextNode('{}'.format(xml_data.get('xml_ymax'))))
    bndbox.appendChild(xmin)
    bndbox.appendChild(ymin)
    bndbox.appendChild(xmax)
    bndbox.appendChild(ymax)

    with open(os.path.join(xml_data.get('out_img_xml_path'), xml_data.get('out_xml_name')), 'w') as f:
        doc.writexml(f, indent='', addindent='\t', newl='\n', encoding='utf-8')


def overlay_images(base_img_path, pasted_img, num, out_img_xml_path):
    start_time = time.time()
    bg_pic = Image.open(base_img_path).convert("RGBA")

    bg_w, bg_h = bg_pic.size

    around_pic = Image.open(pasted_img).convert("RGBA")

    ap_w, ap_h = around_pic.size

    bg_x = random.randint(0, bg_w - ap_w)
    bg_y = random.randint(0, bg_h - ap_h)

    bg_pic.paste(around_pic, (bg_x, bg_y), around_pic)

    # 生成 xml 文件
    xml_xmin = bg_x
    xml_ymin = bg_y
    xml_xmax = bg_x + ap_w
    xml_ymax = bg_y + ap_h

    xml_filename = os.path.split(pasted_img)[1]
    xml_cls_name = xml_filename.split('_')[0]

    # print('11111', xml_cls_name + '_' + str(num) + \
    #                '_{}'.format(os.path.splitext(base_img_path)[0].split(os.sep)[1]))
    out_img_name = xml_cls_name + '_' + str(num) + \
                   '_{}'.format(os.path.splitext(base_img_path)[0].split(os.sep)[1]) + \
                   '_' + xml_filename.split('_')[3] + '_' + str(time.time()).split('.')[0] + \
                   os.path.splitext(pasted_img)[1]

    out_xml_name = os.path.splitext(out_img_name)[0] + '.xml'

    xml_data = {
        'img_name': out_img_name,
        'bg_w': bg_w,
        'bg_h': bg_h,
        'xml_cls_name': xml_cls_name,
        'xml_xmin': xml_xmin,
        'xml_ymin': xml_ymin,
        'xml_xmax': xml_xmax,
        'xml_ymax': xml_ymax,
        'out_xml_name': out_xml_name,
        'out_img_xml_path': out_img_xml_path
    }

    make_xml(xml_data)

    # draw = ImageDraw.Draw(bg_pic)
    # draw.rectangle((xml_xmin, xml_ymin, xml_xmax, xml_ymax), outline='red')

    save_path = os.path.join(out_img_xml_path, out_img_name)

    print(out_xml_name)

    bg_pic.save(save_path)
    print('cost time: ', time.time() - start_time)
    # bg_pic.show()


def crop_ori_img(input_img_path, out_pic_width, out_img_path, plane_kind):
    """
    从原始图中获取飞机部分的图片
    :param input_img_path:
    :param out_pic_width: 输出图片的宽度
    :param out_img_path:
    :param plane_kind: 机型种类如 j10 j11
    :return:
    """
    start_time = time.time()
    # 带alpha通道
    img1 = cv2.imread(input_img_path, cv2.IMREAD_UNCHANGED)

    img2 = cv2.imread(input_img_path)

    gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    canny = cv2.Canny(gray, 30, 300)

    a_point = numpy.argwhere(canny > 0)

    a_list = []
    b_list = []
    for i in a_point:
        a_list.append(i[1])
        b_list.append(i[0])

    x_min = min(a_list)
    x_max = max(a_list)
    y_min = min(b_list)
    y_max = max(b_list)

    # cv2.rectangle(img, (x_min, y_min), (x_max, y_max), (0, 0, 255), 1)    # BGR

    cropped = img1[y_min:y_max, x_min:x_max]
    cropped = imutils.resize(cropped, out_pic_width)

    out_path = os.path.join(out_img_path, str(out_pic_width))
    print('out_path: ', out_path)

    if not os.path.exists(out_path):
        os.makedirs(out_path)

    cv2.imwrite(os.path.join(
        out_path,
        '{}_pasted_width{}_{}.{}'.format(plane_kind,
                                         str(out_pic_width),
                                         str(time.time()).split('.')[0],
                                         input_img_path.split('.')[-1])),
        cropped
    )

    print('cost time: ', time.time() - start_time, '\n')

    # show_cropped = img2[y_min:y_max, x_min:x_max]
    # show_cropped = imutils.resize(show_cropped, out_pic_width)
    # cv2.imshow('img', show_cropped)
    # cv2.waitKey(0)


def make_xml_pic(bg_imgs_path, ard_imgs_path, output_path, processes_num=8):
    start_time = time.time()
    pool = multiprocessing.Pool(processes=processes_num)
    n = 0
    for bg_img in os.listdir(bg_imgs_path):
        for root, dir_list, file_list in os.walk(ard_imgs_path):
            for file_name in file_list:
                input_bg_img = os.path.join(bg_imgs_path, bg_img)
                input_ard_img = os.path.join(root, file_name)
                n += 1
                out_cls_path = file_name.split('_')[0]
                out_file_path = os.path.join(output_path, out_cls_path)

                if not os.path.exists(out_file_path):
                    os.makedirs(out_file_path)

                pool.apply_async(overlay_images, (input_bg_img, input_ard_img, n, out_file_path))
    pool.close()
    pool.join()
    print('totol time: ', (time.time() - start_time))


def make_pasted_imgs(imgs_path, out_pic_width, out_img_path, plane_kind, processes_num=8):
    start_time = time.time()
    pool = multiprocessing.Pool(processes=processes_num)
    n = 0
    for img in os.listdir(imgs_path):
        input_img = os.path.join(imgs_path, img)
        n += 1
        pool.apply_async(crop_ori_img, (input_img, out_pic_width, out_img_path, '{}_{}'.format(plane_kind, str(n))))
    pool.close()
    pool.join()
    print('totol time: ', (time.time() - start_time))


if __name__ == '__main__':
    # make_pasted_imgs('j20_20201105', 400, 'j20_pasted', 'j20')
    # crop_ori_img('10200.png', 500, 'j20_pasted', 'j20')
    #
    # overlay_images('bg_imgs/bg1.jpg', 'j20_pasted/500/j20_pasted_width500_1604558799.png', '1', 'train_bged_pics_xmls')
    make_xml_pic('bg_imgs', 'j20_pasted', 'train_bged_pics_xmls')
