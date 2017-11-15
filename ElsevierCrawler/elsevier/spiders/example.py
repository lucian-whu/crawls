# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import re
import pprint as pp
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
    
    def parse_item_2(self, response):
        print('Processing..' + response.url)
        driver = webdriver.PhantomJS(desired_capabilities=cap)
        # driver = webdriver.Firefox()
        driver.set_window_size(1400, 1000)
        driver.get(response.url)
        print(driver.page_source)

    def parse_item(self, response):
        print('Processing ..' + response.url)


