import os
import shutil
import xml.dom.minidom
import cv2 as cv
import json

# raw data folder path
raw_data_folder = '/home/user/xiongdengrui/pcb/DeepPCB/PCBData'

i = 0

# group folder path
for group_folder in os.listdir(raw_data_folder):
    # only process the first group for simplification
    # if i == 1:
    #     break
    # i = i + 1
    # filter out test.txt and trainval.txt
    if group_folder.endswith('txt'):
        pass
    else:
        # list of child folders' names in group_folder, e.g. ['00041_not', '00041']
        # add .sort to make sure the first element is image folder's name (e.g. '00041'), the second element is txt annotation folder's name (e.g. '00041_not')
        group_folder_child_list = os.listdir(os.path.join(raw_data_folder, group_folder))
        group_folder_child_list.sort(key=lambda x:len(x))
        # image folder path, e.g. /home/user/xiongdengrui/pcb/DeepPCB/PCBData/group00041/00041
        image_folder = os.path.join(raw_data_folder, group_folder, group_folder_child_list[0])
        # txt anno folder path, e.g. /home/user/xiongdengrui/pcb/DeepPCB/PCBData/group00041/00041_not
        txt_anno_folder = os.path.join(raw_data_folder, group_folder, group_folder_child_list[1])
        print(image_folder, txt_anno_folder)
        # for every image in image_folder, save it to images_template if it is a template, otherwise save it to images_defect
        for image in os.listdir(image_folder):
            image_pre, image_ext = os.path.splitext(image)
            original_path = os.path.join(image_folder, image)
            if image_pre.endswith('temp'):
                destination_path = os.path.join('/home/user/xiongdengrui/pcb/DeepPCB/PCBData_collected/images_template', image.replace('_temp', ''))
            else:
                destination_path = os.path.join('/home/user/xiongdengrui/pcb/DeepPCB/PCBData_collected/images_defect', image.replace('_test', ''))
            shutil.copyfile(original_path, destination_path) 
        for annotation in os.listdir(txt_anno_folder):
            original_path = os.path.join(txt_anno_folder, annotation)
            destination_path = os.path.join('/home/user/xiongdengrui/pcb/DeepPCB/PCBData_collected/anno_txt', annotation)
            shutil.copyfile(original_path, destination_path) 