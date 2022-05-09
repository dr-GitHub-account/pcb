import cv2
import os

# labels = ['A', 'B', 'C']  # 数据集类别名
xml_head = '''<annotation>
    <folder>VOC2007</folder>
    <!--文件名-->
    <filename>{}</filename>.
    <source>
        <database>The VOC2007 Database</database>
        <annotation>PASCAL VOC2007</annotation>
        <image>flickr</image>
        <flickrid>325991873</flickrid>
    </source>
    <owner>
        <flickrid>null</flickrid>
        <name>null</name>
    </owner>    
    <size>
        <width>{}</width>
        <height>{}</height>
        <depth>{}</depth>
    </size>
    <segmented>0</segmented>
    '''
xml_obj = '''
    <object>        
        <name>{}</name>
        <pose>Rear</pose>
        <!--是否被裁减，0表示完整，1表示不完整-->
        <truncated>0</truncated>
        <!--是否容易识别，0表示容易，1表示困难-->
        <difficult>0</difficult>
        <!--bounding box的四个坐标-->
        <bndbox>
            <xmin>{}</xmin>
            <ymin>{}</ymin>
            <xmax>{}</xmax>
            <ymax>{}</ymax>
        </bndbox>
    </object>
    '''

xml_end = '''
</annotation>'''


cnt = 0
i = 0
name_list = ['background', 'open', 'short', 'mousebite', 'spur', 'copper', 'pin-hole']

with open('/home/user/xiongdengrui/pcb/DeepPCB/PCBData/trainval.txt', 'r') as trainval_or_test_list: # 训练数据train.txt或test.txt，其中包含图片路径
    # 读取txt文件的每行，lst为str类型
    for lst in trainval_or_test_list.readlines():
        
        # # simplification
        # if i == 1:
        #     break
        # i = i + 1
        
        jpg_file = lst.split(" ")[0]
        # jpg file
        jpg_file = jpg_file.strip()
        jpg_path = os.path.join('/home/user/xiongdengrui/pcb/DeepPCB/PCBData_collected/images_defect', jpg_file.split('/')[2])
        # print('jpg_path:', jpg_path)
        
        txt_file = lst.split(" ")[1]
        # txt file
        txt_file = txt_file.strip()
        txt_path = os.path.join('/home/user/xiongdengrui/pcb/DeepPCB/PCBData_collected/anno_txt', txt_file.split('/')[2])
        # print('txt_path:', txt_path)
        
        # xml file 
        xml_file = jpg_file.replace('.jpg', '.xml')
        xml_path = os.path.join('/home/user/xiongdengrui/pcb/DeepPCB/PCBData_collected/anno_xml_trainval', xml_file.split('/')[2])        
        # print('xml_path:', xml_path)
        
        obj = ''

        # get head information
        img = cv2.imread(jpg_path)
        img_h, img_w = img.shape[0], img.shape[1]
        head = xml_head.format(str(jpg_path.split('/')[-1]), str(img_w), str(img_h), '3')
        # print(head, type(head))
        
        # process txt annotation and rewrite it in xml format
        with open(txt_path, 'r') as f_txt:
            # every for loop reads a line in txt file, i.e. a single instance
            for line in f_txt.readlines():
                pcb_raw_datas = line.strip().split(' ')
                print(pcb_raw_datas, type(pcb_raw_datas))
                label_id = pcb_raw_datas[4].strip()
                label = name_list[int(label_id)]
                xmin = pcb_raw_datas[0].strip()
                ymin = pcb_raw_datas[1].strip()
                xmax = pcb_raw_datas[2].strip()
                ymax = pcb_raw_datas[3].strip()
                print(label_id, type(label_id))
                print(label, type(label))
                print(xmin, type(xmin))
                print(ymin, type(ymin))
                print(xmax, type(xmax))
                print(ymax, type(ymax))
                obj += xml_obj.format(label, xmin, ymin, xmax, ymax)
                
        with open(xml_path, 'w') as f_xml:
            f_xml.write(head + obj + xml_end)
        cnt += 1
        print(cnt)
        
        
           
