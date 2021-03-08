#!/user/bin/env python3
# -*- coding: utf-8 -*-
import os
from xml.etree import ElementTree as ET

# 删除不需要的节点
# xmls_path = r'F:\1028\smoke_only_20201119'
# xmls_file = os.listdir(xmls_path)
# for xf in xmls_file:
#     xf_path = os.path.join(xmls_path, xf)
#     if xf_path.endswith('.xml'):
#         dom = ET.parse(xf_path)
#         root = dom.getroot()
#
#         for i in root.findall('object'):
#             if i.find('name').text == '99':
#                 # root.remove(i)
#                 pass
#             elif i.find('name').text == '98':
#                 # root.remove(i)
#                 pass
#             elif i.find('name').text == 'smoking':
#                 i.find('name').text = '100'
#
#         dom.write(xf_path, xml_declaration=True)

# 修改节点
xmls_path = r'E:\c_HISW_work_file\ICT\zgyd\0222'
xmls_file = os.listdir(xmls_path)
for xf in xmls_file:
    xf_path = os.path.join(xmls_path, xf)
    if xf_path.endswith('.xml'):
        dom = ET.parse(xf_path)
        root = dom.getroot()

        for i in root.findall('object'):
            if i.find('name').text == '98':
                i.find('name').text = 'helmet'
                print(xf_path)
            elif i.find('name').text == '99':
                i.find('name').text = 'uniform'
                print(xf_path)
            # elif i.find('name').text == 'smoking':
            #     # i.find('name').text = '100'
            #     print(xf_path)

        dom.write(xf_path, xml_declaration=True)
