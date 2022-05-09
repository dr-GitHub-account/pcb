txt_path = '/home/user/xiongdengrui/pcb/DeepPCB/PCBData_collected/trainval_test_split/test.txt'

with open(txt_path, 'r', encoding="utf-8") as f_txt, open("%s.bak" % txt_path, "w", encoding="utf-8") as f2:
    for line in f_txt.readlines():
        print(line, type(line))
        # line.replace('txt', 'xml')
        # line = 
        
# import os

# def alter(file,old_str,new_str):

# :param file: 文件路径

# :param old_str: 需要替换的字符串

# :param new_str: 替换的字符串

# with open(file, "r", encoding="utf-8") as f1,open("%s.bak" % file, "w", encoding="utf-8") as f2:

# for lin in f1:

# print(lin)

# if old_str in lin:

# lin = lin.replace(old_str, new_str)

# f2.write(lin)

# os.remove(file)

# os.rename("%s.bak" % file, file)

# alter(r"E:\abc\1.txt", "a", "b")#将"E:\abc"路径的1.txt文件把所有的a改为b