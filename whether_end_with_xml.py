import os

files = os.listdir(r'F:\1028\smoke_only_20201119')
# print(files)

xmls = [i for i in files if ' .xml' in i]
print(xmls)

