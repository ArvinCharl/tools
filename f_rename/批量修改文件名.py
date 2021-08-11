import os
import time

path = r'E:\c_data\jg\no_helmet-helmet\ori-ciga\2'

# 获取该目录下所有文件，存入列表中
fileList = os.listdir(path)

n = 1403
for i in fileList:
    # if i.endswith('JPG'):

    # 获取旧文件名（就是路径+文件名）
    oldname = path + os.sep + i  # os.sep添加系统分隔符
    # old_xml_name = path + os.sep + i.split('.')[0] + '.xml'
    # print(f'oldname: {oldname}')
    # print(f'old_xml_name: {old_xml_name}')
    # if i.split('_')[0] == '徐汇南部医疗施工区2':
    newname = path + os.sep + 'hel-nohel_' + str(n) + '_' + str(time.time()).replace('.', '_') + '.' + i.split('.')[-1]
    # new_xml_name = path + os.sep + 'web_' + i.split('.')[0] + '.xml'
    # newname = path + os.sep + 'negative_' + '_'.join(i.split('_')[1:])
    # print(f'newname: {newname}')
    # print(f'new_xml_name: {new_xml_name}')
    os.rename(oldname, newname)  # 用os模块中的rename方法对文件改名
    # os.rename(old_xml_name, new_xml_name)
    print(oldname, '======>', newname)
    # print(old_xml_name, '======>', new_xml_name)

    # 过滤要修改的文件
    # if i[-4:] == '.xml':

    # 设置新文件名
    # newname = path + os.sep + '%03d' % n + i[-4:]
    # newname = path + os.sep + '%03d' % n + i[-4:]

    # os.rename(oldname, newname)  # 用os模块中的rename方法对文件改名
    # print(oldname, '======>', newname)

    n += 1
