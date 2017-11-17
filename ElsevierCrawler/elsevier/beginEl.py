# coding=utf-8
from scrapy import cmdline

#cmdline.execute("scrapy crawl article".split())
cmdline.execute("scrapy crawl article -a deltafetch_reset=1".split())
