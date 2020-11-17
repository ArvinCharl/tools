# coding:utf-8


# pip install lxml


import os
import glob
import json
import shutil
import numpy as np
import xml.etree.ElementTree as ET



START_BOUNDING_BOX_ID = 1


def get(root, name):
    return root.findall(name)


def get_and_check(root, name, length):
    vars = root.findall(name)

    if len(vars) == 0:
        raise NotImplementedError('Can not find %s in %s.' % (name, root.tag))

    if length > 0 and len(vars) != length:
        raise NotImplementedError('The size of %s is supposed to be %d, but is %d.' % (name, length, len(vars)))

    if length == 1:
        vars = vars[0]

    return vars


def convert(xml_list, json_file, pre_define_categories, only_care_pre_define_categories):
    json_dict = {"images": [], "type": "instances", "annotations": [], "categories": []}

    categories = pre_define_categories.copy()

    bnd_id = START_BOUNDING_BOX_ID

    all_categories = {}

    for index, line in enumerate(xml_list):

        try:
            # print("Processing %s"%(line))

            xml_f = line

            tree = ET.parse(xml_f)

            root = tree.getroot()

            filename = os.path.basename(xml_f)[:-4] + ".jpg"

            # image_id = 20190000001 + index
            image_id = index

            size = get_and_check(root, 'size', 1)

            width = int(get_and_check(size, 'width', 1).text)

            height = int(get_and_check(size, 'height', 1).text)

            image = {'file_name': filename, 'height': height, 'width': width, 'id': image_id}

            json_dict['images'].append(image)

            ## Cruuently we do not support segmentation

            #  segmented = get_and_check(root, 'segmented', 1).text

            #  assert segmented == '0'

            for obj in get(root, 'object'):

                category = get_and_check(obj, 'name', 1).text

                if category in all_categories:

                    all_categories[category] += 1

                else:

                    all_categories[category] = 1

                if category not in categories:

                    if only_care_pre_define_categories:
                        continue

                    new_id = len(categories) + 1

                    print(
                        "[warning] category '{}' not in 'pre_define_categories'({}), create new id: {} automatically".format(
                            category, pre_define_categories, new_id))

                    categories[category] = new_id

                category_id = categories[category]

                bndbox = get_and_check(obj, 'bndbox', 1)

                xmin = int(float(get_and_check(bndbox, 'xmin', 1).text))

                ymin = int(float(get_and_check(bndbox, 'ymin', 1).text))

                xmax = int(float(get_and_check(bndbox, 'xmax', 1).text))

                ymax = int(float(get_and_check(bndbox, 'ymax', 1).text))

                assert (xmax > xmin), "xmax <= xmin, {}".format(line)

                assert (ymax > ymin), "ymax <= ymin, {}".format(line)

                o_width = abs(xmax - xmin)

                o_height = abs(ymax - ymin)

                ann = {'area': o_width * o_height, 'iscrowd': 0, 'image_id':

                    image_id, 'bbox': [xmin, ymin, o_width, o_height],

                       'category_id': category_id, 'id': bnd_id, 'ignore': 0,

                       'segmentation': []}

                json_dict['annotations'].append(ann)

                bnd_id = bnd_id + 1


        except Exception as e:
            print(line,str(e))
            continue
    for cate, cid in categories.items():
        cat = {'supercategory': 'none', 'id': cid, 'name': cate}

        json_dict['categories'].append(cat)
    json_fp = open(json_file, 'w')

    json_str = json.dumps(json_dict)

    json_fp.write(json_str)

    json_fp.close()

    print("------------create {} done--------------".format(json_file))

    print("find {} categories: {} -->>> your pre_define_categories {}: {}".format(len(all_categories), all_categories.keys(), len(pre_define_categories), pre_define_categories.keys()))

    print("category: id --> {}".format(categories))

    print(categories.keys())

    print(categories.values())

def tcoco(xml, classes, train_ratio=0.8):
    xml_dir = os.path.join("voc", xml)

    path2 = os.path.join('coco', xml)

    save_json_train = os.path.join(path2, 'instances_train2014.json')
    save_json_val = os.path.join(path2, 'instances_val2014.json')

    pre_define_categories = {}

    for i, cls in enumerate(classes):
        pre_define_categories[cls] = i + 1

    # pre_define_categories = {'a1': 1, 'a3': 2, 'a6': 3, 'a9': 4, "a10": 5}

    only_care_pre_define_categories = True

    # only_care_pre_define_categories = False

    # train_ratio = train_ratio

    xml_list = glob.glob(xml_dir + "/*.xml")

    xml_list = np.sort(xml_list)

    np.random.seed(100)

    np.random.shuffle(xml_list)

    train_num = int(len(xml_list) * train_ratio)

    xml_list_train = xml_list[:train_num]

    xml_list_val = xml_list[train_num:]

    if os.path.exists(path2 + "/annotations"):
        shutil.rmtree(path2 + "/annotations")

    os.makedirs(path2 + "/annotations")

    if os.path.exists(path2 + "/images/train2014"):
        shutil.rmtree(path2 + "/images/train2014")

    os.makedirs(path2 + "/images/train2014")

    if os.path.exists(path2 + "/images/val2014"):
        shutil.rmtree(path2 + "/images/val2014")

    os.makedirs(path2 + "/images/val2014")

    convert(xml_list_train, save_json_train, pre_define_categories, only_care_pre_define_categories)

    convert(xml_list_val, save_json_val, pre_define_categories, only_care_pre_define_categories)

    f1 = open(os.path.join(path2, "train.txt"), "w")

    for xml in xml_list_train:
        try:
            img = xml[:-4].strip() + ".jpg"

            f1.write(os.path.basename(xml)[:-4] + "\n")
            basename = os.path.basename(img)

            shutil.copyfile(img, path2 + r"/images/train2014/" + basename)
        except:
            img = xml[:-4] + ".jpeg"

            f1.write(os.path.basename(xml)[:-4] + "\n")
            basename = os.path.basename(img)

            shutil.copyfile(img, path2 + r"/images/train2014/" + basename)

    f2 = open(os.path.join(path2, "test.txt"), "w")

    for xml in xml_list_val:
        img = xml[:-4] + ".jpg"

        f2.write(os.path.basename(xml)[:-4] + "\n")

        shutil.copyfile(img, path2 + r"/images/val2014/" + os.path.basename(img))

    f1.close()

    f2.close()

    print("-------------------------------")

    print("train number:", len(xml_list_train))

    print("val number:", len(xml_list_val))


if __name__ == '__main__':

    # classes = ['complete_form', 'img', 'incomplete_form', 'statistical_charts', 'formula', 'paragraph']
    # classes = ['paragraph', 'img', 'incomplete_form', 'complete_form', 'statistical_charts', 'formula']
    # classes = ['chef_cloth', 'chefcap','head_cover']
    classes = ['helmet', 'smoking', 'uniform']

    xml = 'jg4'
    train_ratio = 1
    tcoco(xml, classes, train_ratio)
