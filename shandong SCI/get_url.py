# -*- coding: utf-8 -*-
"""
Created on Thu Aug 03 10:10:06 2017

@author: Administrator
"""



from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
import time,re,string
from bs4 import BeautifulSoup
from PIL import Image,ImageFilter,ImageEnhance  
import pytesseract
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import xlwt

 
#f = open("html.txt",'wb')

def initTable(threshold=140):           # 二值化函数
    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)

    return table

def cnki_ocr(image):
    im=image
    im_grey=im.convert('L')#灰度化
    #binaryImage = im_grey.point(initTable(), '1')  
    #im_peak=im_grey.convert('1')#二值化

    im_filter=im_grey.filter(ImageFilter.MedianFilter)

    sharpness =ImageEnhance.Contrast(im_filter)#对比度增强
    sharp_img = sharpness.enhance(1.0)
    #sharp_img.show()
    vcode=pytesseract.image_to_string(sharp_img,lang="fontyp")
    #print vcode
    vcode=str(vcode.encode("utf8"))
    identify = string.maketrans('', '')   
  
    delEStr = string.punctuation + ' '  #ASCII 标点符号和空格
    delCStr = '《》（）&%￥#@！{}【】'   
    s = vcode.translate(identify, delEStr) #去掉ASCII 标点符号和空格   
    ocr_text = s.translate(identify, delCStr) 
    
    return ocr_text
def cnki_ocr_error():
    driver.save_screenshot('F://aa1.png')  #截取当前网页，该网页有我们需要的验证码
    box_error = (890,78,953,100)
        
    im_screen_error=Image.open("F://aa1.png") #打开截图
    frame4_error = im_screen_error.crop(box_error)
        #frame4=i.crop(rangle)  #使用Image的crop函数，从截图中再次截取我们需要的区域
        #frame4.show()
    cap_text_error=cnki_ocr(frame4_error)
    return cap_text_error
                       
data={}
file = xlwt.Workbook(encoding = 'utf-8')     
#指定file以utf-8的格式打开
table = file.add_sheet('aaa')           
#指定打开的文件名

driver = webdriver.Chrome()
driver.get("http://kns.cnki.net/kns/brief/result.aspx?dbprefix=CJFQ")
driver.maximize_window()

driver.find_element_by_id("1_2").click()
WebDriverWait(driver, 5).until(
    EC.presence_of_element_located((By.ID, "expertvalue"))
)  # Wait until the `text_to_score` element appear (up to 5 seconds)
driver.find_element_by_id("expertvalue").clear()
driver.find_element_by_id('expertvalue').send_keys(u"AF%江苏省农科院 AND HX=Y")
#elem=driver.find_element_by_id("au_1_value2").send_keys(u"江苏省农业科学院")

#elem = driver.find_element_by_xpath("//textarea[@id='expertvalue']/form/div/div[3]/div[1]/dl/dd").clear()
#elem = driver.find_element_by_class_name("textarea1 ac_input").clear()
#设置年份
Select(driver.find_element_by_xpath("//select[@id='year_from']")).select_by_value('1994')
Select(driver.find_element_by_xpath("//select[@id='year_to']")).select_by_value('2016')
#选择核心期刊
#driver.find_element_by_xpath('//input[@id="AllmediaBox"]').click() #点击全部期刊 
#driver.find_element_by_xpath('//input[@id="mediaBox3"]').click()  #点击核心期刊

driver.find_element_by_id("btnSearch").click()
#elem.send_keys(Keys.RETURN)

driver.switch_to_frame("iframeResult")

time.sleep(5)
driver.find_element_by_link_text("50").click()
page_num_text=driver.find_element_by_class_name("countPageMark").text
page_list=page_num_text.split('/')
page_num=int(page_list[1])
article_num=0
if page_num==120:
    driver.find_element_by_link_text("发表时间").click()
    #driver.find_element_by_link_text("发表时间").click()
for i in range(page_num):
    time.sleep(3)
    content=driver.page_source  
    soup = BeautifulSoup(content,"lxml")
    while BeautifulSoup(driver.page_source,"lxml").find(id="CheckCode"):
    #if soup.find(id="CheckCode"):
        driver.save_screenshot('F://aa.png')
        location = driver.find_element_by_id('CheckCodeImg').location
        size=driver.find_element_by_id('CheckCodeImg').size
        left=location['x'] + 411
        top=location['y']
        right=location['x'] + size['width'] + 411
        bottom = location['y'] + size['height']
        im_screen=Image.open("F://aa.png")
        frame4 = im_screen.crop((left,top,right,bottom))
        '''
        imgelement = driver.find_element_by_xpath('//img[@src="/kns/checkcode.aspx?t=\'+Math.random()"]')  #定位验证码
        driver.save_screenshot('F://aa.png')  #截取当前网页，该网页有我们需要的验证码
        #location = imgelement.location  #获取验证码x,y轴坐标
        box = (890,39,953,61)
        
        size=imgelement.size  #获取验证码的长宽
        #rangle=(int(location['x']),int(location['y']),int(location['x']+size['width']),int(location['y']+size['height'])) #写成我们需要截取的位置坐标
        im_screen=Image.open("F://aa.png") #打开截图
        frame4 = im_screen.crop(box)
        #frame4=i.crop(rangle)  #使用Image的crop函数，从截图中再次截取我们需要的区域
        #frame4.show()
        '''
        cap_text=cnki_ocr(frame4)
        print cap_text
        driver.find_element_by_id("CheckCode").send_keys(cap_text)
        time.sleep(3)
        driver.find_element_by_xpath('//input[@value="提交"]').click()
        '''
        while BeautifulSoup(driver.page_source,"lxml").find(id="CheckCode"):
            print u"验证码错误，请重新输入验证码！"
            new_cap=cnki_ocr_error()
            driver.find_element_by_id("CheckCode").send_keys(new_cap)
            time.sleep(3)
            driver.find_element_by_xpath('//input[@value="提交"]').click()
        '''
        content1=driver.page_source  
        soup1 = BeautifulSoup(content1,"lxml")
            
            
                    
        for article1 in soup1.findAll("tr", attrs={"bgcolor":re.compile(r"#ffffff|#f6f7fb")}):
            
            data_list=[]
            
            title = article1.find(class_="fz14").get_text()
            print title
            data_list.append(title)
            author=article1.find(class_="author_flag").get_text()
            print author
            data_list.append(author)
            journal=article1.find(class_="cjfdyxyz").get_text()
            print journal
            data_list.append(journal)
            #year=article.find().get_text()
            cited_num=article1.find(class_="KnowledgeNetcont").get_text()
            print(u"被引频次为%s" % cited_num.encode("utf8"))
            data_list.append(cited_num)
            article_href=article1.find(class_="fz14").get("href")
            #print article_href
            article_href_list = article_href.split("&")
            article_url="http://kns.cnki.net/KCMS/detail/detail.aspx?"+article_href_list[2]+"&"+article_href_list[3]+"&"+article_href_list[4]
            print article_url
            data_list.append(article_url)
            article_num=article_num+1
            data[str(article_num)]=data_list    

    else:
        for article in soup.findAll("tr", attrs={"bgcolor":re.compile(r"#ffffff|#f6f7fb")}):
            
            data_list=[]
            
            article_title = article.find(class_="fz14").get_text()
            print article_title
            data_list.append(article_title)
            author=article.find(class_="author_flag").get_text()
            print author
            data_list.append(author)
            journal=article.find(class_="cjfdyxyz").get_text()
            print journal
            data_list.append(journal)
            #year=article.find().get_text()
            cited_num=article.find(class_="KnowledgeNetcont").get_text()
            print(u"被引频次为%s" % cited_num.encode("utf8"))
            
            data_list.append(cited_num)
            
            article_href=article.find(class_="fz14").get("href")
            #print article_href
            article_href_list = article_href.split("&")
            article_url="http://kns.cnki.net/KCMS/detail/detail.aspx?"+article_href_list[2]+"&"+article_href_list[3]+"&"+article_href_list[4]
            print article_url
            data_list.append(article_url)
            article_num=article_num+1
            data[str(article_num)]=data_list        
        

           
            '''
            driver.get(article_url)
            
            content2=driver.page_source
            soup2 = BeautifulSoup(content2,"lxml")
            catalog_tag=soup2.find("label",attrs={"id":"catalog_ZTCLS"})
            catalog=catalog_tag.parent.string
            print catalog
            time.sleep(2)
            driver.back() 
            
            
            
            actions = ActionChains(driver)
            about = driver.find_element_by_link_text(article_title)
            actions.key_down(Keys.CONTROL).click(about).key_up(Keys.CONTROL).perform()

            driver.switch_to.window(driver.window_handles[-1])
            driver.get(article_url)
            
            time.sleep(5)
            js = "window.open(article_url)" #可以看到是打开新的标签页 不是窗口
            driver.execute_script(js)
            time.sleep(5)
            driver.close() 
            
            #打开文章页面
            #driver.find_element_by_link_text(title.encode("utf8")).click()
            #element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME,"fz14")))
            wait = WebDriverWait(driver, 20)
            element = wait.until(EC.presence_of_element_located((By.LINK_TEXT,article_title.encode("utf8"))))
            #element = driver.find_element_by_link_text(title.encode("utf8"))
            element.click()
            time.sleep(5)
            print driver.current_window_handle # 输出当前窗口句柄
            handles = driver.window_handles # 获取当前窗口句柄集合（列表类型）
            print handles # 输出句柄集合
            for handle in handles:# 切换窗口（切换到搜狗）
               if handle!=driver.current_window_handle:
                   print 'switch to ',handle
                   driver.switch_to_window(handle)
                   print driver.current_window_handle # 输出当前窗口句柄（搜狗）
                   content2=driver.page_source
                   soup2 = BeautifulSoup(content2,"lxml")
                   catalog_tag=soup2.find("label",attrs={"id":"catalog_ZTCLS"})
                   catalog=catalog_tag.parent.string
                   #catalog=catalog_tag.string
                   print catalog
            driver.close()
            #driver.close() #关闭当前窗口（搜狗）
            driver.switch_to_window(handles[0]) #切换回原窗口
            '''
        
        
    print i    
    if i < page_num-1:
        print page_num
        driver.find_element_by_link_text("下一页").click()
    
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
file.save('aaa.xls') 
 
print("work is done！")
'''
f.write(content.encode('utf8'))
f.close()
driver.quit()
'''