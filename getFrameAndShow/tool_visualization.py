# -*- coding: utf-8 -*-
import time

import PIL.ImageColor as ImageColor
import PIL.ImageDraw as ImageDraw
import PIL.ImageFont as ImageFont
import PIL.Image as Image
import numpy as np
import cv2


# from pic_mask import mask_pic


def draw_bounding_box_on_image_array(image,
                                     ymin,
                                     xmin,
                                     ymax,
                                     xmax,
                                     color=(144, 222, 150),
                                     thickness=2,
                                     display_str_list=(),
                                     use_normalized_coordinates=False):
    """Adds a bounding box to an image (numpy array).

    Args:
      image: a numpy array with shape [height, width, 3].
      ymin: ymin of bounding box in normalized coordinates (same below).
      xmin: xmin of bounding box.
      ymax: ymax of bounding box.
      xmax: xmax of bounding box.
      color: color to draw bounding box. Default is red.
      thickness: line thickness. Default value is 4.
      display_str_list: list of strings to display in box
                        (each to be shown on its own line).
      use_normalized_coordinates: If True (default), treat coordinates
        ymin, xmin, ymax, xmax as relative to the image.  Otherwise treat
        coordinates as absolute.
    """
    image_pil = Image.fromarray(np.uint8(image)).convert('RGB')
    draw_bounding_box_on_image(image_pil, ymin, xmin, ymax, xmax, color,
                               thickness, display_str_list,
                               use_normalized_coordinates)
    np.copyto(image, np.array(image_pil))


def draw_bounding_box_on_image(image,
                               ymin,
                               xmin,
                               ymax,
                               xmax,
                               color='green',
                               thickness=2,
                               display_str_list=(),
                               use_normalized_coordinates=False):
    """Adds a bounding box to an image.

    Each string in display_str_list is displayed on a separate line above the
    bounding box in black text on a rectangle filled with the input 'color'.

    Args:
      image: a PIL.Image object.
      ymin: ymin of bounding box.
      xmin: xmin of bounding box.
      ymax: ymax of bounding box.
      xmax: xmax of bounding box.
      color: color to draw bounding box. Default is red.
      thickness: line thickness. Default value is 4.
      display_str_list: list of strings to display in box
                        (each to be shown on its own line).
      use_normalized_coordinates: If True (default), treat coordinates
        ymin, xmin, ymax, xmax as relative to the image.  Otherwise treat
        coordinates as absolute.
    """
    # print(xmin, xmax, ymin, ymax)
    draw = ImageDraw.Draw(image)
    im_width, im_height = image.size
    if use_normalized_coordinates:
        (left, right, top, bottom) = (xmin * im_width, xmax * im_width,
                                      ymin * im_height, ymax * im_height)
    else:
        (left, right, top, bottom) = (xmin, xmax, ymin, ymax)
    # print(left,right,top,bottom)
    draw.line([(left, top), (left, bottom), (right, bottom),
               (right, top), (left, top)], width=thickness, fill=color)
    try:
        # font = ImageFont.truetype('arial.ttf', 18)
        # font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 20)
        font = ImageFont.truetype('simsun.ttc', 30)
    except IOError:
        font = ImageFont.load_default()

    text_bottom = top
    # Reverse list and print from bottom to top.
    for display_str in display_str_list[::-1]:
        text_width, text_height = font.getsize(display_str)
        margin = np.ceil(0.05 * text_height)
        draw.rectangle(
            [(left, text_bottom - text_height - 2 * margin), (left + text_width,
                                                              text_bottom)],
            fill=color)
        draw.text(
            (left + margin, text_bottom - text_height - margin),
            display_str,
            fill='black',
            font=font)
        # text_bottom -= text_height - 2 * margin
        text_bottom = text_bottom - text_height if text_bottom - text_height > 10 else text_bottom + text_height


def draw_text_on_image_array(image,
                             color=(144, 222, 150),
                             thickness=2,
                             display_str_list=(),
                             use_normalized_coordinates=False):
    image_pil = Image.fromarray(np.uint8(image)).convert('RGB')
    draw_text_on_image(image_pil,
                       color,
                       thickness,
                       display_str_list,
                       use_normalized_coordinates)
    np.copyto(image, np.array(image_pil))


def draw_text_on_image(image,
                       color='green',
                       thickness=2,
                       display_str_list=(),
                       use_normalized_coordinates=False):
    draw = ImageDraw.Draw(image)
    try:
        # font = ImageFont.truetype('arial.ttf', 18)
        # font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 20)
        font = ImageFont.truetype(r'c:\windows\fonts\msyhl.ttc', 30)
    except IOError:
        font = ImageFont.load_default()
    for display_str in display_str_list[::-1]:
        # text_width, text_height = font.getsize(display_str)
        # draw.rectangle(
        #     [(50, 150)],
        #     fill=color)
        draw.text(
            (10, 80),
            display_str,
            fill='green',
            font=font)

# if __name__ == '__main__':
# start_time = time.time()
# img = cv2.imread('../img_test/032.jpg')
# mask = mask_pic_pic(img)
# mask, boxes_list = mask_pic(img)
# for box in boxes_list:
#     draw_bounding_box_on_image_array(mask, box[1], box[0], box[3], box[2],
#                                      display_str_list=['rec_model: J31', 'rec_number: 31001', 'Corresponding pilot ID: 1', 'Corresponding aircraft ID: 1'])
#
#     # lt = (box[0], box[1])
#     # rb = (box[2], box[3])
#     # cv2.rectangle(mask, lt, rb, (0, 255, 0), 2)
#
# cv2.imwrite("../TO_see/visualed.jpg", mask)
# # cv2.imwrite('TO_see/rec_array.jpg', mask)
# print('Totol cost time: ', time.time() - start_time)
