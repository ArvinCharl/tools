import os

files = os.listdir(r'E:\c_HISW_work_file\ICT\zgyd\fire')
# print(files)

xmls = [i for i in files if ' .xml' in i]
print(xmls)

