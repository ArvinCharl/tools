import os
import xml.dom.minidom

"""修改文件名, 在原文件名后面加标识"""
# path = r'E:\code\tools\f_rename\gaussian_noise'
# dir_list = os.listdir(path)
# n = 0
# for i in dir_list:
#     old_name = path + os.sep + i
#     print('old_name: %s' % old_name)
#     new_name = path + os.sep + i[0:-4] + 'gn' + i[-4:]
#     n += 1
#     print('new_name: %s' % new_name)
#     os.rename(old_name, new_name)

"""修改xml文档的 filename 标签的值"""
# path = r'E:\code\tools\f_rename\轰6K'
# file_list = os.listdir(path)
# for i in file_list:
#     # xml 文件的名称
#     if i[-4:] == '.xml':
#         xml_path = os.path.join(path, i)
#         print(xml_path)
#
#         # 打开xml文档
#         dom = xml.dom.minidom.parse(xml_path)
#
#         # 得到文档元素对象
#         root = dom.documentElement
#         filename = root.getElementsByTagName("filename")
#         a = filename[0]
#         # old_name = a.firstChild.data
#         # new_name = old_name[:-4] + 'g' + old_name[-4:]
#         new_name = i[:-4] + '.jpg'
#         a.firstChild.data = new_name
#         print(a.firstChild.data)
#
#         with open(xml_path, 'w', encoding='utf8') as f:
#             dom.writexml(f)


"""修改xml文档的 object/name 标签的值"""
path = r'E:\code\tools\f_rename\jh7xml'
dir_list = os.listdir(path)
for i in dir_list:
    xml_path = os.path.join(path, i)
    print(xml_path)

    # 打开xml文档
    dom = xml.dom.minidom.parse(xml_path)

    # 得到文档元素对象
    root = dom.documentElement
    filename = root.getElementsByTagName("name")
    # 定位文本
    a = filename[0]
    # 获取原本的文本名
    # old_name = a.firstChild.data
    # print(old_name)
    # 修改新文本名
    # new_name = old_name[:3]
    new_name = 'jh7'
    a.firstChild.data = new_name
    print(a.firstChild.data)
    # 写入源文件
    with open(xml_path, 'w', encoding='utf8') as f:
        dom.writexml(f)
