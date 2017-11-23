# -*- coding: utf-8 -*-
from selenium import webdriver
from scrapy import Selector

chrome_opt = webdriver.ChromeOptions()
prefs = {"profile.managed_default_content_settings.images": 2, "profile.default_content_settings.popups": 0,
         "download.default_directory": "F:\\journal\\qbxb\\"}
chrome_opt.add_experimental_option("prefs", prefs)
browser = webdriver.Chrome(executable_path="C:\\Users\\lx201\\Desktop\\GithubProject\\crawls\\cnkiCrawler"
                                           "\\chromedriver.exe", chrome_options=chrome_opt)


# 将文章的URL写入文件detail_links
def write_urls(urls):
    with open("detail_links", 'a', encoding='utf-8') as f:
        for url in urls:
            f.write(url + '\n')


start = "http://c.wanfangdata.com.cn/periodical/qbxb/2017-8.aspx"
for i in range(0, 158):
    browser.get(start)
    t_selector = Selector(text=browser.page_source)
    urls = t_selector.xpath('//a[@class="qkcontent_name"]/@href').extract()

    # 找到下一页的链接
    next_url = t_selector.xpath('//div[@class="Content_div_detail"]/p/a/@href').extract()
    # 将链接写入文件
    write_urls(urls)

    # 休息8秒钟从下一页继续爬取
    if len(next_url) is not 0:
        import time
        time.sleep(3)
        start = "http://c.wanfangdata.com.cn" + str(next_url[0])
    else:
        browser.quit()
        print("work done!")
