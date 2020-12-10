
# https://code.visualstudio.com/docs/python
# Modules

## Tidying
import numpy as np
import pandas as pd
import re

## Scraping
from bs4 import BeautifulSoup # https://www.crummy.com/software/BeautifulSoup/bs4/doc/
from selenium import webdriver # https://selenium-python.readthedocs.io/locating-elements.html
from selenium.webdriver.chrome.options import Options

## Sleeping
import time as tm
import random as rd

# Beige Book URLs
BB_2020_url = 'https://www.federalreserve.gov/monetarypolicy/beige-book-default.htm'
BB_2019_1996_urls = 'https://www.federalreserve.gov/monetarypolicy/beige-book-archive.htm'

# Configure Chrome Options for webdriver

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome('/Users/Cookie/node_modules/chromedriver/lib/chromedriver/chromedriver', chrome_options = chrome_options)  # You will need to install chromedriver this a pain for macs..

# Pulling most recent BB entry

print('Pulling ' + BB_2020_url)

driver.get(BB_2020_url)

print('Loading page')

tm.sleep(rd.randint(2, 4))

print(BeautifulSoup(driver.page_source, 'lxml')) # all this will give us is a page of links where we aim to take the most recent one using driver.find_elements_by...