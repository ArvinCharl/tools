import os

path = r'E:\c_data\baoshan_kitchen\baoshan_traindata20210316'

# 获取该目录下所有文件，存入列表中
fileList = os.listdir(path)

n = 1
for i in fileList:
    # 获取旧文件名（就是路径+文件名）
    oldname = path + os.sep + i  # os.sep添加系统分隔符
    # print(oldname)
    if i.split('_')[0] == 'negative':
        newname = path + os.sep + 'positive_' + i.split('_')[1] + '_' + i.split('_')[2] + '_' + i.split('_')[3]
        os.rename(oldname, newname)  # 用os模块中的rename方法对文件改名
        print(oldname, '======>', newname)

    # 过滤要修改的文件
    # if i[-4:] == '.xml':

    # 设置新文件名
    # newname = path + os.sep + '%03d' % n + i[-4:]
    # newname = path + os.sep + '%03d' % n + i[-4:]

    # os.rename(oldname, newname)  # 用os模块中的rename方法对文件改名
    # print(oldname, '======>', newname)

    n += 1
