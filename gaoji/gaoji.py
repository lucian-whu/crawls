import re
import string

import location
from PIL import Image, ImageEnhance, ImageFilter
from bs4 import BeautifulSoup
from pytesseract import pytesseract
from scrapy import Selector
from selenium import webdriver


# 验证码识别函数
def cnki_ocr(image):
    im = image
    im_grey = im.convert('L')  # 灰度化
    im_filter = im_grey.filter(ImageFilter.MedianFilter)
    sharpness = ImageEnhance.Contrast(im_filter)  # 对比度增强
    sharp_img = sharpness.enhance(1.0)
    vcode = pytesseract.image_to_string(sharp_img, lang="fontyp")
    ocr_text = vcode.replace(' ', '')
    # print(ocr_text)
    return ocr_text


# 对浏览器进行设置
chrome_opt = webdriver.ChromeOptions()
prefs = {"profile.default_content_settings.popups": 0,  # 下载文件时不出现选择框
         "download.default_directory": "F:\\journal\\qbxb\\"}  # 设置下载文件时的默认文件夹
chrome_opt.add_experimental_option("prefs", prefs)

# 实例化一个浏览器
browser = webdriver.Chrome(executable_path="C:\\Users\\lx201\\Desktop\\GithubProject\\crawls\\cnkiCrawler"
                                           "\\chromedriver.exe", chrome_options=chrome_opt)
browser.maximize_window()  # 最大化浏览器


# 将文章的URL写入文件links
def write_urls(urls):
    with open("gaoji_links", 'a', encoding='utf-8') as f:
        for url in urls:
            f.write(url + '\n')


# 一次写一个url
def write_url(url):
    with open("gaoji_links", 'a', encoding='utf-8') as f:
        f.write(url + '\n')


# 进入高级检索页面输入检索式，进行检索：
start = "http://kns.cnki.net/kns/brief/result.aspx?dbprefix=scdb"
browser.get(start)
browser.find_element_by_xpath('//dd[@id="joursource_1"]/input[@id="magazine_value1"]').send_keys("情报学报")
browser.find_element_by_xpath('//dd[@id="joursource_1"]/input[@id="magazine_value1"]').click()  # 点击去掉下拉框
browser.find_element_by_xpath('//input[@id="publishdate_from"]').send_keys("1994-01-01")  # 起始日期
browser.find_element_by_xpath('//input[@id="publishdate_to"]').send_keys("2000-12-31")  # 截止日期
js = browser.find_element_by_xpath('//input[@id="btnSearch"]').get_attribute("onclick")  # 找到检索按钮
browser.execute_script(js)  # 执行检索按钮下的js代码

# 切入结果列表的iframe
browser.switch_to_frame("iframeResult")
# 加载15秒
import time

time.sleep(15)

browser.find_element_by_link_text("50").click()  # 每页显示50条结果
# 得到总的页数page_num
page_num_text = browser.find_element_by_class_name("countPageMark").text
page_list = page_num_text.split('/')
page_num = int(page_list[1])
print(page_num)

for i in range(page_num):  # 对每一页进行浏览
    t_selector = Selector(text=browser.page_source)

    code = t_selector.xpath('//input[@id="CheckCode"]').extract()  # 找验证码的图片

    if len(code) is not 0:  # 如果验证码存在的话，对验证码进行识别，并进行相应的处理
        while BeautifulSoup(browser.page_source, "lxml").find(id="CheckCode"):  # 识别验证码，识别错误的话，继续识别
            browser.save_screenshot('F://aa.png')
            location = browser.find_element_by_id('CheckCodeImg').location
            size = browser.find_element_by_id('CheckCodeImg').size
            left = location['x'] + 411
            top = location['y']
            right = location['x'] + size['width'] + 411
            bottom = location['y'] + size['height']
            im_screen = Image.open("F://aa.png")
            frame4 = im_screen.crop((left, top, right, bottom))  # 最终得到验证码的截图frame4

            cap_text = cnki_ocr(frame4)  # 进行识别
            browser.find_element_by_id("CheckCode").send_keys(cap_text)  # 填入验证码
            browser.find_element_by_xpath('//input[@value="提交"]').click()
            time.sleep(3)  # 等待加载

            content1 = browser.page_source
            soup1 = BeautifulSoup(content1, "lxml")

            # 对结果列表的文章进行处理
            for article1 in soup1.findAll("tr", attrs={"bgcolor": re.compile(r"#ffffff|#f6f7fb")}):
                title = article1.find(class_="fz14").get_text()  # 标题
                print(title)
                author = article1.find(class_="author_flag").get_text()  # 作者
                journal = article1.find(class_="Mark").get_text()  # 期刊
                year = article1.find().get_text()  # 年份
                # if (article.find(class_="KnowledgeNetcont")) is not None:
                #     cited_num = article.find(class_="KnowledgeNetcont").get_text()
                #     print(cited_num)
                # else:
                #     print('0')                 # 被引次数
                article_href1 = article1.find(class_="fz14").get("href")  # 链接
                article_href_list1 = article_href1.split("&")
                article_url1 = "http://kns.cnki.net/KCMS/detail/detail.aspx?" + article_href_list1[2] + "&" + \
                               article_href_list1[3] + "&" + article_href_list1[4]
                write_url(article_url1)

    else:
        soup = BeautifulSoup(browser.page_source, "lxml")
        for article in soup.findAll("tr", attrs={"bgcolor": re.compile(r"#ffffff|#f6f7fb")}):
            article_title = article.find(class_="fz14").get_text()
            print(article_title)
            author = article.find(class_="author_flag").get_text()
            journal = article.find(class_="Mark").get_text()
            year = article.find().get_text()
            # if(article.find(class_="KnowledgeNetcont")) is not None:
            #     cited_num = article.find(class_="KnowledgeNetcont").get_text()
            #     print(cited_num)
            # else:
            #     print('0')
            article_href = article.find(class_="fz14").get("href")
            article_href_list = article_href.split("&")
            article_url = "http://kns.cnki.net/KCMS/detail/detail.aspx?" + article_href_list[2] + "&" + \
                          article_href_list[3] + "&" + article_href_list[4]
            write_url(article_url)

    print(i)
    if i < (page_num-1):
            browser.find_element_by_link_text("下一页").click()
    else:
        print("work is done！")
