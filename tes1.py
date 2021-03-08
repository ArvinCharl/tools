#!/user/bin/env python3
# -*- coding: utf-8 -*-
import os
import time

file_path = r'E:\c_HISW_work_file\ICT\zgyd\fire_negative'
out_file_path = r'E:\c_HISW_work_file\ICT\zgyd\fire_negative_out'

files = os.listdir(file_path)
num = 0
for f in files:
    num += 1
    new_file_name = os.rename(
        os.path.join(file_path, f),
        os.path.join(out_file_path,
                     'negative_' + str(time.time()).replace('.', '') + '_' + str(num) + '.' + 'jpg')
    )
    print(os.path.join(file_path, f))
