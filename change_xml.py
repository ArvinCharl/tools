#!/user/bin/env python3
# -*- coding: utf-8 -*-
import os
import shutil
from xml.etree import ElementTree as ET

# 删除不需要的节点
# xmls_path = r'E:\c_data\excavator1'
# xmls_file = os.listdir(xmls_path)
# for xf in xmls_file:
#     xf_path = os.path.join(xmls_path, xf)
#     if xf_path.endswith('.xml'):
#         dom = ET.parse(xf_path)
#         root = dom.getroot()
#
#         for i in root.findall('object'):
#             if i.find('name').text == 'slagcar':
#                 print(xf_path)
#                 root.remove(i)
# #             #     pass
# #             # elif i.find('name').text == 'helmet':
# #             #     # root.remove(i)
# #             #     pass
# #             # elif i.find('name').text == 'smoking':
# #             #     root.remove(i)
# #             #     pass
# #
#         dom.write(xf_path, xml_declaration=True)

# 修改节点
# xmls_path = r'E:\c_data\jg\Safety Helmet Wearing Dataset\Images'
# xmls_file = os.listdir(xmls_path)
# for xf in xmls_file:
#     xf_path = os.path.join(xmls_path, xf)
#     if xf_path.endswith('.xml'):
#         dom = ET.parse(xf_path)
#         root = dom.getroot()
#
#         for i in root.findall('object'):
#             # if i.find('name').text == '98':
#             if i.find('name').text == 'head_with_helmet':
#                 i.find('name').text = 'helmet'
#                 print(xf_path)
#             #     pass
#             # elif i.find('name').text == 'head':
#             #     i.find('name').text = 'no_helmet'
#             #     print(xf_path)
#                 # pass
#             # elif i.find('name').text == '100':
#             #     i.find('name').text = 'smoking'
#             #     # root.remove(i)
#             #     print(xf_path)
#
#         dom.write(xf_path, xml_declaration=True)


# 删除没有标注内容的xml
# xmls_path = r'E:\c_data\excavator1'
# xmls_file = os.listdir(xmls_path)
# for xf in xmls_file:
#     xf_path = os.path.join(xmls_path, xf)
#     if xf_path.endswith('.xml'):
#         dom = ET.parse(xf_path)
#         root = dom.getroot()
#         for i in root.findall('object'):
#             if i.find('name').text == 'slagcar':
#                 shutil.copy(xf_path, r'E:\c_data\ex_slagcar')
#                 shutil.copy(xf_path.split('.')[0] + '.jpg', r'E:\c_data\ex_slagcar')
#                 print(xf_path)

