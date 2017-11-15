# -*- coding: utf-8 -*-
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from selenium import webdriver

cap = webdriver.DesiredCapabilities.PHANTOMJS
cap["phantomjs.page.settings.javascriptEnabled"] = True
cap["phantomjs.page.settings.loadImages"] = True
cap["phantomjs.page.settings.userAgent"] = 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'

class ArticleSpider(CrawlSpider):
    name = "article"

    start_urls = ["http://www.sciencedirect.com/science/journal/17511577"]

    rules = (
        Rule(LinkExtractor(allow=(), restrict_xpaths=('//div[@id="volumeIssueData"]/ol/li',), ), callback="parse_item", follow= True,),
        Rule(LinkExtractor(allow=(), restrict_css=('.artTitle',),), callback="parse_item_2", follow=True,), 
    )

    count = 0
    def parse_item_2(self, response):
        print('Processing..' + response.url)
        driver = webdriver.PhantomJS(desired_capabilities=cap)
        # driver = webdriver.Firefox()
        driver.set_window_size(1400, 1000)
        driver.get(response.url)
        html = driver.page_source
        self.count = self.count + 1
        with open("G:\\journals\\informetrics\\" + str(self.count) + ".html", 'w', encoding='utf-8') as file:
            file.write(html)

    def parse_item(self, response):
        print('Processing ..' + response.url)


