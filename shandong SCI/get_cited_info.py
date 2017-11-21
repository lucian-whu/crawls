# -*- coding: utf-8 -*-
"""
Created on Tue Jul 25 16:07:53 2017

@author: Administrator
"""

import re
import string
import time


import pandas as pd
import pytesseract
from PIL import Image, ImageFilter, ImageEnhance
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.select import Select


# f = open("html.txt",'wb')

def cnki_ocr(image):
    im = image
    im_grey = im.convert('L')  # 灰度化
    # binaryImage = im_grey.point(initTable(), '1')
    # im_peak=im_grey.convert('1')#二值化

    im_filter = im_grey.filter(ImageFilter.MedianFilter)

    sharpness = ImageEnhance.Contrast(im_filter)  # 对比度增强
    sharp_img = sharpness.enhance(1.0)
    # sharp_img.show()
    vcode = pytesseract.image_to_string(sharp_img, lang="fontyp")
    # print vcode
    vcode = str(vcode.encode("utf8"))
    identify = string.maketrans('', '')
    delEStr = string.punctuation + ' '  # ASCII 标点符号和空格
    delCStr = '《》（）&%￥#@！{}【】'
    s = vcode.translate(identify, delEStr)  # 去掉ASCII 标点符号和空格
    ocr_text = s.translate(identify, delCStr)
    return ocr_text


df = pd.DataFrame()
data = {'title': '', 'author': '', 'journal': '', 'cited_num': '', 'url': ''}

driver = webdriver.Chrome()
driver.get("http://kns.cnki.net/kns/brief/result.aspx?dbprefix=CJFQ")
driver.maximize_window()

driver.find_element_by_id("1_1").click()
elem = driver.find_element_by_id("au_1_value2").send_keys(u"江苏省农业科学院")

# elem = driver.find_element_by_xpath("//textarea[@id='expertvalue']/form/div/div[3]/div[1]/dl/dd").clear()
# elem = driver.find_element_by_class_name("textarea1 ac_input").clear()
# 设置年份
Select(driver.find_element_by_xpath("//select[@id='year_from']")).select_by_value('1994')
Select(driver.find_element_by_xpath("//select[@id='year_to']")).select_by_value('2016')
# 选择核心期刊
driver.find_element_by_xpath('//input[@id="AllmediaBox"]').click()  # 点击全部期刊
driver.find_element_by_xpath('//input[@id="mediaBox3"]').click()  # 点击核心期刊

driver.find_element_by_id("btnSearch").click()
# elem.send_keys(Keys.RETURN)

driver.switch_to_frame("iframeResult")

time.sleep(5)
driver.find_element_by_link_text("50").click()
page_num_text = driver.find_element_by_class_name("countPageMark").text
page_list = page_num_text.split('/')
page_num = int(page_list[1])

for i in range(page_num):
    time.sleep(3)
    content = driver.page_source
    soup = BeautifulSoup(content, "lxml")
    code = Selector
    if soup.find(id="CheckCode"):
        imgelement = driver.find_element_by_xpath('//img[@src="/kns/checkcode.aspx?t=\'+Math.random()"]')  # 定位验证码
        driver.save_screenshot('F://aa.png')  # 截取当前网页，该网页有我们需要的验证码
        # location = imgelement.location  #获取验证码x,y轴坐标
        box = (890, 39, 953, 61)

        size = imgelement.size  # 获取验证码的长宽
        # rangle=(int(location['x']),int(location['y']),int(location['x']+size['width']),int(location['y']+size['height'])) #写成我们需要截取的位置坐标
        im_screen = Image.open("F://aa.png")  # 打开截图
        frame4 = im_screen.crop(box)
        # frame4=i.crop(rangle)  #使用Image的crop函数，从截图中再次截取我们需要的区域
        # frame4.show()
        cap_text = cnki_ocr(frame4)
        print cap_text
        driver.find_element_by_id("CheckCode").send_keys(cap_text)
        time.sleep(3)
        driver.find_element_by_xpath('//input[@value="提交"]').click()

        content1 = driver.page_source
        soup1 = BeautifulSoup(content1, "lxml")
        for article1 in soup1.findAll("tr", attrs={"bgcolor": re.compile(r"#ffffff|#f6f7fb")}):
            title = article1.find(class_="fz14").get_text()
            print title
            author = article1.find(class_="author_flag").get_text()
            print author
            journal = article1.find(class_="cjfdyxyz").get_text()
            print journal
            # year=article.find().get_text()
            cited_num = article1.find(class_="KnowledgeNetcont").get_text()
            print(u"被引频次为%s" % cited_num.encode("utf8"))
            article_href1 = article1.find(class_="fz14").get("href")
            # print article_href
            article_href_list1 = article_href1.split("&")
            article_url1 = "http://kns.cnki.net/KCMS/detail/detail.aspx?" + article_href_list1[2] + "&" + \
                           article_href_list1[3] + "&" + article_href_list1[4]
            print article_url1

    else:
        for article in soup.findAll("tr", attrs={"bgcolor": re.compile(r"#ffffff|#f6f7fb")}):
            article_title = article.find(class_="fz14").get_text()
            print article_title
            author = article.find(class_="author_flag").get_text()
            print author
            # journal = article.find(class_="cjfdyxyz").get_text()
            # print journal
            # year=article.find().get_text()
            cited_num = article.find(class_="KnowledgeNetcont").get_text()
            print(u"被引频次为%s" % cited_num.encode("utf8"))
            article_href = article.find(class_="fz14").get("href")
            # print article_href
            article_href_list = article_href.split("&")
            article_url = "http://kns.cnki.net/KCMS/detail/detail.aspx?" + article_href_list[2] + "&" + \
                          article_href_list[3] + "&" + article_href_list[4]
            print article_url

    print i
    if i < page_num:
        driver.find_element_by_link_text("下一页").click()

print("work is done！")
