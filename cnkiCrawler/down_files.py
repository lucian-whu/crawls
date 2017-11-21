# -*- coding: utf-8 -*-
from selenium import webdriver
from scrapy import Selector

chrome_opt = webdriver.ChromeOptions()
prefs = {"profile.managed_default_content_settings.images": 2, "profile.default_content_settings.popups": 0,
         "download.default_directory": "F:\\journal\\qbxb\\"}
chrome_opt.add_experimental_option("prefs", prefs)
browser = webdriver.Chrome(executable_path="C:\\Users\\lx201\\Desktop\\GithubProject\\crawls\\cnkiCrawler"
                                           "\\chromedriver.exe", chrome_options=chrome_opt)
with open("links",'r', encoding='utf-8') as f:
    links = f.readlines()
    for line in links:
        browser.get(line)
        import time
        time.sleep(8)



