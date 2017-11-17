# -*- coding: utf-8 -*-
"""
Created on Mon Jul 17 14:30:33 2017

@author: Administrator
"""

import string  
import re  
  
identify = string.maketrans('', '')   
  
delEStr = string.punctuation + ' '  #ASCII 标点符号和空格
delCStr = '《》（）&%￥#@！{}【】'   
  
s = 'XV6_HD《'   
print type(s)
s = s.translate(identify, delEStr) #去掉ASCII 标点符号和空格   
if re.findall('[\x80-\xff].', s):    #s为中文   
   s = s.translate(identify, delCStr)   
   print s   
else: #s为英文   
    print s  