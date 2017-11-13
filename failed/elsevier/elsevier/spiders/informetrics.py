# -*- coding: utf-8 -*-
# 得到elsevier期刊的文章页面
from scrapy import Request
from scrapy.spiders import CrawlSpider
from scrapy_splash import SplashRequest, SplashFormRequest


class InformetricsSpider(CrawlSpider):
    name = 'informetrics'
    start_urls = ['https://www.sciencedirect.com/science/journal/17511577/1/1']

    def parse_start_url(self, response):
        for url in self.start_urls:
            yield SplashRequest(url,
                                self.parse_page,
                                args={'wait':30}
                                )

    def parse_page(self,response):
        # 得到每篇文章的链接列表
        urls = response.xpath('//ol[@class="articleList results"]//ul[@class="article"]/li[@class="title"]/h4/a/@href').extract()
        # 把每一页的链接传到下一个处理函数
        for url in urls:
            print('!!!!!!!!!!' + url)
            url = 'https://www.sciencedirect.com' + url
            yield SplashRequest(url,
                                self.parse_item,
                                args={'wait':30})

        # 得到下一页的链接
        next_page = response.xpath('//a[@class="Next volume/issue"]/href').extrat()
        if len(next_page) is not 0:
            print(url+'!!!!!!!!!!!!!!')
            next_page_url = 'https://www.sciencedirect.com' + next_page[0].strip()
            yield SplashRequest(next_page_url,
                                self.parse_page,
                                args={'wait':30})

    def parse_item(self,response):
        print('response!!!!!!!!!'+response.url)

        html = response.text

        print(html)






