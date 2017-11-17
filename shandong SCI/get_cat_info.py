# -*- coding: utf-8 -*-
"""
Created on Mon Jul 31 12:23:43 2017

@author: Administrator
"""

from selenium import webdriver
import time,re,string
from bs4 import BeautifulSoup
import xlrd,xlwt

workbook = xlrd.open_workbook(r'aaa.xls')
sheet1_name = workbook.sheet_names()[0]
  # 根据sheet索引或者名称获取sheet内容
#sheet1 = workbook.sheet_by_index(0) # sheet索引从0开始
sheet1 = workbook.sheet_by_name('aaa')
 
  # sheet的名称，行数，列数
print sheet1.name,sheet1.nrows,sheet1.ncols
driver = webdriver.Chrome()
data={}
file = xlwt.Workbook(encoding = 'utf-8')     
#指定file以utf-8的格式打开
table = file.add_sheet('detail')  
for i in range(sheet1.nrows):
    data_list=[]
    
    url=sheet1.cell(i,5).value.encode('utf-8')
    driver.get(url)
    driver.maximize_window()
    content=driver.page_source  
    soup = BeautifulSoup(content,"lxml")
    
    title=driver.find_element_by_class_name("title").text
    print title.encode('utf-8')
    data_list.append(title)
    
    organic=driver.find_element_by_class_name("orgn").text
    print organic.encode('utf-8')
    data_list.append(organic)
    
    baseinfo=soup.find_all('div',{'class':'wxBaseinfo'})[0].find_all('p')
    if len(baseinfo)>=5:
        baseinfo_num=5
    else:
        baseinfo_num=len(baseinfo)
    for ii in range(baseinfo_num):
        abs=baseinfo[ii].get_text()
        print abs.encode('utf-8')  
        data_list.append(abs)
    
    date=soup.find_all('div',{'class':'sourinfo'})[0].find_all('p')[2].get_text()
    print date.encode('utf-8')
    data_list.append(date)    
        
    '''    
    abs=soup.find_all('div',{'class':'wxBaseinfo'})[0].find_all('p')[0].get_text()
    print abs.encode('utf-8')  
    data_list.append(abs)
    fond=soup.find_all('div',{'class':'wxBaseinfo'})[0].find_all('p')[1].get_text()
    print fond.encode('utf-8')
    data_list.append(fond)
    keyword=soup.find_all('div',{'class':'wxBaseinfo'})[0].find_all('p')[2].get_text()
    print keyword.encode('utf-8')
    data_list.append(keyword)
    catalog=soup.find_all('div',{'class':'wxBaseinfo'})[0].find_all('p')[3].get_text()
    print catalog.encode('utf-8')
    data_list.append(catalog)
    '''
    
    
    data[str(i)]=data_list 
         
ldata = []
num = [a for a in data]             
#for循环指定取出key值存入num中
num.sort()                          
#字典数据取出后无需，需要先排序

for x in num:                       
#for循环将data字典中的键和值分批的保存在ldata中
    t = [int(x)]
    for a in data[x]:
        t.append(a)
    ldata.append(t)

for i,p in enumerate(ldata):        
#将数据写入文件,i是enumerate()函数返回的序号数
    for j,q in enumerate(p):
        print i,j,q
        table.write(i,j,q)
file.save('detail.xls') 
 
print("work is done！")         