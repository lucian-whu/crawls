# -*- coding: utf-8 -*-
"""
Created on Mon Jul 24 15:57:56 2017

@author: Administrator
# 训练验证码
"""

from PIL import Image,ImageFilter,ImageEnhance  
import os,pytesseract
import os.path
rootdir="D:\\shandong SCI\\train data"
i=0
for parent,dirnames,filenames in os.walk(rootdir):
    
    for filename in filenames:
        print filename
        im=Image.open(os.path.join(parent,filename))  
        im_grey=im.convert('L')#灰度化
        #binaryImage = im_grey.point(initTable(), '1')
        #im_peak=im_grey.convert('1')#二值化

        im_filter=im_grey.filter(ImageFilter.MedianFilter)

        sharpness =ImageEnhance.Contrast(im_filter)#对比度增强
        sharp_img = sharpness.enhance(1.0)
        sharp_img.show()
        vcode=pytesseract.image_to_string(sharp_img,lang="fontyp")
        vcode=str(vcode.encode("utf8"))
        print vcode
        i=i+1
        save_name=str(i)+".tif"
        sharp_img.save(save_name)
       
    