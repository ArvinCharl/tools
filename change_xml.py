#!/user/bin/env python3
# -*- coding: utf-8 -*-
import os
from xml.etree import ElementTree as ET

xmls_path = r'F:\1028\smoke_only_20201119'
xmls_file = os.listdir(xmls_path)
for xf in xmls_file:
    xf_path = os.path.join(xmls_path, xf)
    if xf_path.endswith('.xml'):
        dom = ET.parse(xf_path)
        root = dom.getroot()

        for i in root.findall('object'):
            if i.find('name').text == '99':
                root.remove(i)
            elif i.find('name').text == '98':
                root.remove(i)
            # elif i.find('name').text == 'smoking':
            #     i.find('name').text = '100'

        dom.write(xf_path, xml_declaration=True)


# xmls_path = r'F:\1028\smoke_only_20201119'
# xmls_file = os.listdir(xmls_path)
# for xf in xmls_file:
#     xf_path = os.path.join(xmls_path, xf)
#     if xf_path.endswith('.xml'):
#         dom = ET.parse(xf_path)
#         root = dom.getroot()
#
#         for i in root.findall('object'):
#             if i.find('name').text == 'uniform':
#                 i.find('name').text = '99'
#             elif i.find('name').text == 'helmet':
#                 i.find('name').text = '98'
#             elif i.find('name').text == 'smoking':
#                 i.find('name').text = '100'
#
#         dom.write(xf_path, xml_declaration=True)
