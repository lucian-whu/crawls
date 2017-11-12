# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from scrapy.spiders import CrawlSpider

from plosjournal.items import PlosjournalItem


class PlosSpider(CrawlSpider):
    name = 'plos'
    start_urls = ['http://journals.plos.org/plosone/browse/']

    def parse_start_url(self, response):
        # call parse_page for start url
        print(response.url + "这是response.url的内容")
        yield Request(response.url, callback=self.parse_page)

    def parse_page(self, response):
        # grab article url
        urls = response.xpath('//div[@class="article-block"]//a[@class="article-url"]/@href').extract()

        # add domain to url and call parse_item on each article url
        for url in urls:
            url = 'http://journals.plos.org' + url
            yield Request(url, callback=self.parse_item)

            # grab link for the next page
            next_page = response.xpath('//nav[@class="nav-pagination"]//a[@id="nextPageLink"]/@href').extract()

            # if there is a next page, follow the link and call parse_page on it
            if len(next_page) is not 0:
                next_page_url = 'http://journals.plos.org' + next_page[0].strip()
                yield Request(next_page_url, callback=self.parse_page)

    def parse_item(self,response):
        print(response.url)
        name = response.url.split('.')[-1]
        name = name + '.' + 'html'
        # print(name)
        html = response.text
        with open("result\\" + name, 'w', encoding='utf-8')as file:
            file.write(html)



