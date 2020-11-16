import os
import random
from shutil import copyfile

img_path = 'j20'
ori_data = os.listdir(img_path)
train_img_data = random.sample([i for i in ori_data if i.split('.')[-1] == 'jpg'], 400)
print(train_img_data)

xml_data = [i for i in os.listdir(img_path) if i.split('.')[-1] == 'xml']
train_xml_data = []


for i in xml_data:
    pic_name = i.split('.')[0] + '.' + 'jpg'
    if pic_name in train_img_data:
        train_xml_data.append(i)

print(train_xml_data)

save_dir = 'train_data'

if not os.path.exists(save_dir):
    os.makedirs(save_dir)

for i in train_img_data:
    copyfile(os.path.join(img_path, i), os.path.join(save_dir, i))

for i in train_xml_data:
    copyfile(os.path.join(img_path, i), os.path.join(save_dir, i))
