# coding = "utf-8"
import selenium
from selenium import webdriver

with open("detail_links", 'r', encoding='utf-8') as f:
    links =  f.readlines()
    for line in links:
        chrome_opt = selenium.webdriver.ChromeOptions()
        prefs = {"profile.default_content_settings.popups": 0,
                 "download.default_directory": "F:\\journal\\qbxb\\cnki1\\"}
        chrome_opt.add_experimental_option("prefs", prefs)
        browser = selenium.webdriver.Chrome(
            executable_path="C:\\Users\\lx201\\Desktop\\GithubProject\\crawls\\cnkiCrawler"
                            "\\chromedriver.exe", chrome_options=chrome_opt)
        browser.get(line)

        title = browser.find_element_by_id()
