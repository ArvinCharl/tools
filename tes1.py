#!/user/bin/env python3
# -*- coding: utf-8 -*-
import os
import shutil

n = 0
for root, dirs, files in os.walk(r'F:\excel'):
    for file in files:
        each_file = os.path.join(root, file)
        shutil.copy(each_file, r'F:\excel\out')
        n += 1
        print('正在移动第{}个文件: {}'.format(str(n), each_file), '\n')
