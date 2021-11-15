#!/user/bin/env python3
# -*- coding: utf-8 -*-
import os

import imutils
import pymysql
import cv2

# 打开数据库连接
import requests
from pandas import np

db = pymysql.connect(host='222.73.81.2', port=11306, user='root', passwd='mysql@Hisw321', db='cloud_admin', charset='utf8')

# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()

# 使用 execute()  方法执行 SQL 查询
cursor.execute("select remarks from t_alarm ORDER BY alarm_date desc LIMIT 5")

# 使用 fetchone() 方法获取单条数据.
db_result = cursor.fetchall()

for slagcar_url in db_result:
    slagcar_url = slagcar_url[0]
    out_img_path = os.path.join('slagcar_pics', os.path.basename(slagcar_url))
    print(slagcar_url)
    file = requests.get(slagcar_url)
    img = cv2.imdecode(np.fromstring(file.content, np.uint8), 1)
    img = imutils.resize(img, 1080)
    cv2.imshow('img', img)
    cv2.waitKey(3000)
    cv2.imwrite(out_img_path, img)

# 关闭数据库连接
db.close()
