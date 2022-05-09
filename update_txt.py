import os

txt_file = '/home/user/xiongdengrui/pcb/DeepPCB/PCBData_collected/trainval_test_split/trainval.txt'
old_ext = 'txt'
new_ext = 'xml'

def alter(txt_file, old_ext, new_ext):
    """
    将替换的字符串写到一个新的文件中，然后将原文件删除，新文件改为原来文件的名字
    :param txt_file: 文件路径
    :param old_ext: 需要替换的字符串
    :param new_ext: 替换的字符串
    :return: None
    """
    with open(txt_file, "r", encoding="utf-8") as f1, open("%s.bak" % txt_file, "w", encoding="utf-8") as f2:
        for line in f1:
            line = line.split(' ')[1]
            line = line.split('/')[2]
            if old_ext in line:
                line = line.replace(old_ext, new_ext)
            f2.write(line)
    os.remove(txt_file)
    os.rename("%s.bak" % txt_file, txt_file)

alter(txt_file, old_ext, new_ext)