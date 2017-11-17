# -*- coding: utf-8 -*-
"""
Created on Thu Jul 06 09:44:11 2017

@author: Administrator
"""
import sys
import urllib2
import cookielib  
import string
import re
import time


f = open('test.csv', 'r')
i = 1
for line in f:
    print line
    try:
        cj = cookielib.CookieJar()  
        cookie_support = urllib2.HTTPCookieProcessor(cj)  
        opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)  
        urllib2.install_opener(opener)
        url = line
        refer = 'http://epub.cnki.net/kns/brief/brief.aspx?pagename=ASP.brief_default_result_aspx&dbPrefix=SCDB&dbCatalog=%e4%b8%ad%e5%9b%bd%e5%ad%a6%e6%9c%af%e6%96%87%e7%8c%ae%e7%bd%91%e7%bb%9c%e5%87%ba%e7%89%88%e6%80%bb%e5%ba%93&ConfigFile=SCDBINDEX.xml&research=off&t=1431252221059&keyValue=python&S=1'


        h = {
             'Referer' : refer,
             'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0'
        }
        r = urllib2.urlopen(urllib2.Request(url,headers = h))


        r = urllib2.urlopen(urllib2.Request(r.geturl(),headers = h))
        r = urllib2.urlopen(urllib2.Request(r.geturl(),headers = h))
        r = urllib2.urlopen(urllib2.Request(r.geturl(),headers = h))


        data = r.read()
        
        if data[:8] == '[TARGET]':
            with open(str(i)+".caa", "wb") as up:     
                up.write(data)
            up.close
        else:
            with open(str(i)+".caj", "wb") as up:     
                up.write(data)
            up.close
        print str(i)+' '+'succeed'
        time.sleep(2)
    except:
        print str(i)+' '+'failed'
    i = i + 1

