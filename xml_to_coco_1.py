# coding=utf-8
import xml.etree.ElementTree as ET
import os
import json

voc_clses = ['open', 'short', 'mousebite', 'spur', 'copper', 'pin-hole']
categories = []

# 根据voc_clses，得到完整的列表categories
# [
# {'supercategory': 'open', 'name': 'open', 'id': 0}, 
# {'supercategory': 'short', 'name': 'short', 'id': 1}, 
# {'supercategory': 'mousebite', 'name': 'mousebite', 'id': 2}, 
# {'supercategory': 'spur', 'name': 'spur', 'id': 3}, 
# {'supercategory': 'copper', 'name': 'copper', 'id': 4}, 
# {'supercategory': 'pin-hole', 'name': 'pin-hole', 'id': 5}
# ]
for iind, cat in enumerate(voc_clses):
    cate = {}
    cate['supercategory'] = cat
    cate['name'] = cat
    cate['id'] = iind
    categories.append(cate)

def getimages(xmlname, id):
    # sig_xml_box列表存放当前xml文件对应图像的所有的bbox信息
    sig_xml_box = []
    tree = ET.parse(xmlname)
    root = tree.getroot()
    # images以键值对的形式存放当前xml文件对应图像的'file_name', 'width', 'height', 'id'
    images = {}
    for i in root:  # 遍历一级节点
        if i.tag == 'filename':
            file_name = i.text  # 0001.jpg
            # print('image name: ', file_name)
            images['file_name'] = file_name
        if i.tag == 'size':
            # 遍历一级节点'size'的所有二级节点
            for j in i:
                if j.tag == 'width':
                    width = j.text
                    images['width'] = width
                if j.tag == 'height':
                    height = j.text
                    images['height'] = height
        if i.tag == 'object':
            # 遍历一级节点'object'的所有二级节点
            for j in i:
                if j.tag == 'name':
                    cls_name = j.text
                # cat_id是当前object类别对应的id，
                # 'open': 1, 'short': 2, 'mousebite': 3, 'spur': 4, 'copper': 5, 'pin-hole': 6
                cat_id = voc_clses.index(cls_name) + 1
                if j.tag == 'bndbox':
                    bbox = []
                    xmin = 0
                    ymin = 0
                    xmax = 0
                    ymax = 0
                    # 遍历二级节点'bndbox'的所有三级节点
                    for r in j:
                        if r.tag == 'xmin':
                            xmin = eval(r.text)
                        if r.tag == 'ymin':
                            ymin = eval(r.text)
                        if r.tag == 'xmax':
                            xmax = eval(r.text)
                        if r.tag == 'ymax':
                            ymax = eval(r.text)
                    # 列表bbox中存放了当前bndbox的xmin, ymin, 长, 宽, 对应的图片代号, 对应的类别代号, 面积
                    bbox.append(xmin)
                    bbox.append(ymin)
                    bbox.append(xmax - xmin)
                    bbox.append(ymax - ymin)
                    bbox.append(id)   # 保存当前box对应的image_id
                    bbox.append(cat_id)
                    # anno area
                    bbox.append((xmax - xmin) * (ymax - ymin) - 10.0)   # bbox的areas
                    # coco中的ares数值是 < w*h 的, 因为它其实是按segmentation的面积算的,所以我-10.0一下...
                    sig_xml_box.append(bbox)
                    # print('bbox', xmin, ymin, xmax - xmin, ymax - ymin, 'id', id, 'cls_id', cat_id)
    images['id'] = id
    # print ('sig_img_box', sig_xml_box)
    return images, sig_xml_box



def txt2list(txtfile):
    f = open(txtfile, "r")
    l = []
    for line in f:
        # print(line, type(line))
        l.append(line.replace('\n', '').replace('\r', ''))
    return l


if __name__ == '__main__':
    # xml文件所在文件夹
    xml_prefix = '/home/user/xiongdengrui/pcb/DeepPCB/PCBData_collected/anno_xml_trainval'
    # pcb/DeepPCB/PCBData下的test.txt包含了很多冗余信息，pcb/DeepPCB/PCBData_collected/trainval_test_split下的test.txt是处理后的不包含冗余信息的
    txt_path = '/home/user/xiongdengrui/pcb/DeepPCB/PCBData_collected/trainval_test_split/trainval.txt'
    # 将txt文件中每一行作为一个元素，创建一个列表xml_names
    # ['20085291.xml', '20085292.xml', ..., '12000593.xml']
    xml_names = txt2list(txt_path)

    xmls = []
    bboxes = []
    ann_js = {}
    # xmls列表里存放所有xml标注文件的路径
    for ind, xml_name in enumerate(xml_names):
        xmls.append(os.path.join(xml_prefix, xml_name))
    # 目标json文件路径
    json_name = '/home/user/xiongdengrui/pcb/DeepPCB/PCBData_collected/anno_json/trainval.json'
    images = []

    for i_index, xml_file in enumerate(xmls):
    # getimages()返回值中：
    # image是字典，以键值对的形式存放当前xml文件对应图像的'file_name', 'width', 'height', 'id'
    # sig_xml_bbox是列表，存放当前xml文件对应图像的所有的bbox信息
        image, sig_xml_bbox = getimages(xml_file, i_index)
        # 将所有xml文件(所有图像)对应的image字典汇总到列表images中
        images.append(image)
        # 将所有xml文件(所有图像)对应的sig_xml_bbox列表(由该图像中多个bbox的列表组成)拆分成一个个bbox的列表汇总到列表bboxes中
        bboxes.extend(sig_xml_bbox)
    # ann_js是整个json文件里包含所有信息的大字典，包含'images', 'categories', 'annotations'
    ann_js['images'] = images
    ann_js['categories'] = categories
    annotations = []
    for box_ind, box in enumerate(bboxes):
        anno = {}
        anno['image_id'] =  box[-3]
        anno['category_id'] = box[-2]
        anno['bbox'] = box[:-3]
        anno['id'] = box_ind
        anno['area'] = box[-1]
        anno['iscrowd'] = 0
        annotations.append(anno)
    ann_js['annotations'] = annotations
    json.dump(ann_js, open(json_name, 'w'), indent=4)  # indent=4 更加美观显示