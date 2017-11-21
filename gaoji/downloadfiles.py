# -*- coding: utf-8 -*-
import time

from selenium import webdriver

for i in range(1, 11):
    name = "gaoji_links." + str(i)
    print(name)
    with open(name, 'r', encoding='utf-8') as f:
        links = f.readlines()
        count = 0
        for line in links:
            chrome_opt = webdriver.ChromeOptions()
            prefs = {"profile.default_content_settings.popups": 0,
                     "download.default_directory": "F:\\journal\\qbxb\\cnki1\\"}
            chrome_opt.add_experimental_option("prefs", prefs)
            browser = webdriver.Chrome(executable_path="C:\\Users\\lx201\\Desktop\\GithubProject\\crawls\\cnkiCrawler"
                                                       "\\chromedriver.exe", chrome_options=chrome_opt)
            browser.get(line)
            time.sleep(5)
            browser.find_element_by_link_text("PDF下载").click()
            time.sleep(20)
            with open("guo", 'a', encoding='utf-8') as f1:
                f1.write(line)  # 将已经下载的链接放到guo
            count = count + 1
            print(count)
            browser.quit()
time.sleep(120)


