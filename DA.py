
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
BB_2019_1996_urls = 'https://www.federalreserve.gov/monetarypolicy/beige-book-archive.htm' # 2017-2020 has the same format

# Creating the dataframe

date = []
overallEconomicActivity = []
employmentPrices = []

# Configure Chrome Options for webdriver

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome('/Users/Cookie/node_modules/chromedriver/lib/chromedriver/chromedriver', 
                          chrome_options = chrome_options)

# Pulling most recent BB entry

print('Pulling ' + BB_2020_url)

driver.get(BB_2020_url)

print('Loading page')

tm.sleep(rd.randint(2, 4))

soup = BeautifulSoup(driver.page_source, 'lxml')

links = [str(l['href']) for l in soup.find_all("a", href=re.compile("/monetarypolicy/beigebook"))]

links = ['https://www.federalreserve.gov' + sub for sub in links]

print('Collected Links')

for n, link in enumerate(links):

    driver.get(link)

    print('Loading link ' + str(n))

    tm.sleep(rd.randint(1, 3))

    reportSoup = BeautifulSoup(driver.page_source, 'lxml')

    date.append(re.sub('Last Update:|\n|\\s{2,}',
                       '',
                       reportSoup.find('div', {'class':'lastUpdate'}).text)) # Pulling date for the dataframe

    tm.sleep(rd.randint(1, 3))

    textSoup = [str(t) for t in reportSoup.find_all('p')]

    positionOEA = [i for i, s in enumerate(textSoup) if 'Overall Economic Activity' in s][0]
    positionEP = [i for i, s in enumerate(textSoup) if 'Employment and Wages' in s][0]
    positionEnd = [i for i, s in enumerate(textSoup) if 'Highlights by Federal Reserve District' in s][0]

    corpusOverallEconomicActivity = ''.join(textSoup[positionOEA:positionEP])
    corpusEmploymentPrices = ''.join(textSoup[positionEP:positionEnd])

    def simpleCleanCorpus(corpus: str): 

        corpus = re.sub('<p>|</p>|<br/>|<strong>.*</strong>', '', corpus)

        return corpus

    overallEconomicActivity.append(simpleCleanCorpus(corpusOverallEconomicActivity))

    employmentPrices.append(simpleCleanCorpus(corpusEmploymentPrices))

    print('Corpuses from link ' + str(n) + 'cleaned and collected')
    
beigeBookExtracts2020 = pd.DataFrame({"Date":date,
                                      "OverallEconomicActivity":overallEconomicActivity,
                                      "EmploymentPrices":employmentPrices})

print(beigeBookExtracts2020)