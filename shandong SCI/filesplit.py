# -*- coding: utf-8 -*-
"""
Created on Thu Jun 01 11:04:48 2017

@author: Administrator
"""
import os



#定义目录：目录下有多个文件需要处理

path = 'D:\\shandong SCI\\origin data\\'
os.chdir(path)
f1=file("savedrecs3.txt")
#定义输出文件

ss="\nER\n"
sr=f1.read().split(ss)
f1.close()
for i in range(len(sr)):
    f = file("z%d.txt" % i,"w")
    f.write(sr[i] if i==0 else ss+sr[i])
    f.close()
