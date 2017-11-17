# -*- coding: utf-8 -*-
"""
Created on Wed Aug 02 16:09:45 2017

@author: Administrator
"""

import random
s = int(random.uniform(1,10))
print(s)
m = int(input('输入整数:'))
while m != s:
	if m > s:
		print('大了')
		m = int(input('输入整数:'))
	if m < s:
		print('小了')
		m = int(input('输入整数:'))
	if m == s:
		print('OK')
		break;