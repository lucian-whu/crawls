# coding="utf-8"
__author__ = "Xin Li"
__Date__ = "20171120"

import selenium.webdriver
import time
import random

for i in range(1, 11):
    name = "gaoji_links." + str(i)
    print(name)
    with open(name, 'r', encoding='utf-8') as f:
        links = f.readlines()
        count = 0
        for line in links:
            n = random.randint(1, 3)
            time.sleep(3 * n)
            chrome_opt = selenium.webdriver.ChromeOptions()
            prefs = {"profile.default_content_settings.popups": 0,
                     "download.default_directory": "F:\\journal\\qbxb\\cnki1\\"}
            chrome_opt.add_experimental_option("prefs", prefs)
            browser = selenium.webdriver.Chrome(
                executable_path="C:\\Users\\lx201\\Desktop\\GithubProject\\crawls\\cnkiCrawler"
                                "\\chromedriver.exe", chrome_options=chrome_opt)
            browser.get(line)

            count = count + 1  # 文章编号
            print(count)
            url = line  # 文章链接
            title = browser.find_element_by_class_name("title").text  # 文章标题

            # 获取文章的摘要，判断“更多”是否显示，显示则点击，再提取摘要文本；不显示，则直接提取摘要文本
            flag = True
            try:
                if browser.find_element_by_id("ChDivSummaryMore").is_displayed():
                    flag = True
                else:
                    flag = False
            except:
                flag = False
            if flag:
                browser.find_element_by_id("ChDivSummaryMore").click()
            abs = browser.find_element_by_id("ChDivSummary").text

            # 获取关键词，判断是否有关键词
            flag_kw = True
            try:
                if browser.find_element_by_id("catalog_KEYWORD").is_displayed():
                    flag_kw = True
                else:
                    flag_kw = False
            except:
                flag_kw = False
            keywords = ""
            if flag_kw:
                kws = browser.find_elements_by_xpath('//label[@id="catalog_KEYWORD"]/following-sibling::a')
                for kw in kws:
                    keywords = keywords + kw.text
            else:
                keywords = "这篇文献没有关键词"

            # 将文章的详细内容和关键词分别写入两个文件
            infoFileName = "results\\info." + str(i)
            kwFileName = "results\\kw." + str(i)
            with open(infoFileName, 'a', encoding='utf-8') as info:
                info.write('\n' + str(count) + '\n')
                info.write(url)
                info.write("标题：" + title + '\n')
                info.write("摘要：" + abs + '\n')
                info.write("关键词：" + keywords)
                info.write('\n')
            with open(kwFileName, 'a', encoding='utf-8') as kwf:
                kwf.write(str(count) + '|' + keywords + '\n')
            # 完成一篇文章，就退出浏览器
            browser.quit()
