# -*- coding: utf-8 -*-
"""
Created on Fri Jul 14 09:53:41 2017

@author: Administrator
"""
from PIL import Image,ImageFilter,ImageEnhance  
import pytesseract
import string  
import re  

def initTable(threshold=140):           # 二值化函数
    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)

    return table

im =Image.open("3.jpg")  

im_grey=im.convert('L')#灰度化
#binaryImage = im_grey.point(initTable(), '1')  
#im_peak=im_grey.convert('1')#二值化

im_filter=im_grey.filter(ImageFilter.MedianFilter)

sharpness =ImageEnhance.Contrast(im_filter)#对比度增强
sharp_img = sharpness.enhance(1.0)
sharp_img.show()
vcode=pytesseract.image_to_string(sharp_img)
print(vcode)
vcode=str(vcode.encode("utf8"))
identify = string.maketrans('', '')   
  
delEStr = string.punctuation + ' '  #ASCII 标点符号和空格
delCStr = '《》（）&%￥#@！{}【】'   
  
s = vcode.translate(identify, delEStr) #去掉ASCII 标点符号和空格   
if re.findall('[\x80-\xff].', s):    #s为中文   
   s = s.translate(identify, delCStr)   
   print(s)
else: #s为英文   
    print(s)

