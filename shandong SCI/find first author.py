# -*- coding: utf-8 -*-
"""
Created on Thu Jun 01 10:16:47 2017

@author: Administrator
"""

import os
import sys
import pandas as pd
import matplotlib.pyplot as plt

#定义目录：目录下有多个文件需要处理
path = 'D:\\shandong SCI\\origin data\\'
#定义输出文件
#fout = open("normal.txt","w")
x=[
   'PT',
   'AU',
   'AF',
   'CA',
   'TI',
   'SO',
   'LA',
   'DT',
   'ID',
   'AB',
   'C1',
   'RP',
   'EM',
   'RI',
   'OI',
   'FU',
   'FX',
   'CA',
   'CR',
   'NR',
   'TC',
   'Z9',
   'U1',
   'U2',
   'PU',
   'PI',
   'PA',
   'SN',
   'J9',
   'JI',
   'PD',
   'PY',
   'VL',
   'IS',
   'BP',
   'EP',
   'DI',
   'PG',
   'WC',
   'SC',
   'GA',
   'UT',
   ]
y=['C1','RP']
#改变路径
os.chdir(path)
print os.getcwd()
#遍历目录下的所有文件
i=0
empty_df = pd.DataFrame.from_dict({"file_name":"","PT":"","AU":"","AF":"","CA":"","TI":"","SO":"","LA":"","DT":"","ID":"","AB":"","C1":"","RP":"","EM":"","RI":"","OI":"","FU":"","FX":"","CA":"","CR":"","NR":"","TC":"","Z9":"","U1":"","U2":"","PU":"","PI":"","PA":"","SN":"","J9":"","JI":"","PD":"","PY":"","VL":"","IS":"","BP":"","EP":"","DI":"","PG":"","WC":"","SC":"","GA":"","UT":""},orient='index').T
for filename in os.listdir(path):
    print filename
    fs = open(filename,'r+')
    #处理文件中的每一行数据
    i=i+1
    ii=str(i)
    dict1={}
    dict1['file_name']=filename
    for line in fs.readlines():
        a = line.split()
        print a
                
        if a != [] and a[0] in x:
            dict1[a[0]]=''.join(list(line)[3:])
        
        
    if 'Shandong Acad Agr Sci' in dict1['C1'] or 'Shandong Acad Agr Sci' in dict1['RP']:
        new=pd.DataFrame(dict1,index=[ii])
        empty_df = empty_df.append(new,ignore_index=True)  
    if 'Shanmdong Acad Agr Sci' in dict1['C1'] or 'Shanmdong Acad Agr Sci' in dict1['RP']:
        new=pd.DataFrame(dict1,index=[ii])    
        empty_df = empty_df.append(new,ignore_index=True)  
    if 'SHANDONG ACAD AGR SCI' in dict1['C1'] or 'SHANDONG ACAD AGR SCI' in dict1['RP']:
        new=pd.DataFrame(dict1,index=[ii])
        #if a[0] in y and 'Shandong Acad Agr Sci' in line:            
        empty_df = empty_df.append(new,ignore_index=True)   
year=empty_df['PY'][1:467]
institution = empty_df['C1'][1:467]
print year.value_counts()
print institution.value_counts()
'''
fig = plt.figure()
ax=fig.add_subplot(1,1,1)
ax.hist(empty_df['PY'])
plt.xlabel('year')
plt.ylabel('num')
plt.show()
'''

writer=pd.ExcelWriter('D:\\shandong SCI\\2.csv')
empty_df.to_excel(writer)
#writer.save()
              
#fout.write('\n')    
#fout.close()  