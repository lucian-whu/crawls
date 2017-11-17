# -*- coding: utf-8 -*-
"""
Created on Tue Jul 25 15:23:18 2017

@author: Administrator
"""

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome()
driver.get("https://www.google.com")

# open a link in a new window
actions = ActionChains(driver)
about = driver.find_element_by_link_text('Google 大全')
actions.key_down(Keys.CONTROL).click(about).key_up(Keys.CONTROL).perform()

driver.switch_to.window(driver.window_handles[-1])
driver.get("https://stackoverflow.com")