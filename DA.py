
# Modules

## Tidying
import numpy as np
import pandas as pd
import re

## Scraping
from bs4 import BeautifulSoup
from selenium import webdriver # This will probably need to be installed via terminal
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

driver.get(BB_2020_url)

tm.sleep(rd.randint(2, 4)/1)

BeautifulSoup(driver.page_source, 'lxml') # all this will give us is a page of links where we aim to take the top one using driver.find_elements_by...