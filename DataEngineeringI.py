# https://code.visualstudio.com/docs/python
# Modules

## Tidying
import numpy as np
import pandas as pd
import re
import datetime

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

# Configure Chrome Options for webdriver

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome('/Users/Cookie/node_modules/chromedriver/lib/chromedriver/chromedriver', 
                          chrome_options = chrome_options)

# Create Class

class data_engineering_1:
    
    def __init__(self):
        
        '''
        
        '''

    def year_link_create(self, yr:int):

        link = ('https://www.federalreserve.gov/monetarypolicy/beigebook' + str(yr) + '.htm')

        return link

    def find_links(self, BB_url:str):

        print('Pulling ' + str(BB_url))

        driver.get(BB_url)

        print('Loading page')

        tm.sleep(rd.randint(2, 4))

        soup = BeautifulSoup(driver.page_source, 'lxml')

        foundlinks = [str(l['href']) for l in soup.find_all("a", href=re.compile(r"[/]monetarypolicy[/]beigebook.*.htm"))]

        return foundlinks

    def format_links(self, link: str):

        if 'https://www.federalreserve.gov' not in link:

            return ('https://www.federalreserve.gov' + link)

        else:

            return link

    def simple_clean_corpus(self, corpus: str): 

                corpus = re.sub('\n|<p>|</p>|<br/>|<strong>.*</strong>', '', corpus)

                return corpus

    def pull_corpora_17_20(self, links:list, date = [], overallEconomicActivity = [], employmentPrices = []):    

        for n, link in enumerate(links):

            driver.get(link)

            print('Loading link ' + str(n))

            tm.sleep(rd.randint(1, 3))

            reportSoup = BeautifulSoup(driver.page_source, 'lxml')

            if any(ext in link for ext in ['2017', '2018', '2019','2020']):

                date.append(re.sub('Last Update:|\n|\\s{2,}',
                                   '',
                                   reportSoup.find('div', {'class':'lastUpdate'}).text)) # Pulling date for the dataframe

                textSoup = [str(t) for t in reportSoup.find_all('p')]

                positionOEA = [i for i, s in enumerate(textSoup) if 'Overall Economic Activity' in s][0]
                positionEW = [i for i, s in enumerate(textSoup) if 'Employment and Wages' in s][0]
                positionP = [i for i, s in enumerate(textSoup) if 'Prices' in s][0]

                corpusOverallEconomicActivity = ''.join(textSoup[positionOEA:positionEW])
                corpusEmploymentPrices = ''.join(textSoup[positionEW:(positionP+1)])   

                overallEconomicActivity.append(self.simple_clean_corpus(corpusOverallEconomicActivity))

                employmentPrices.append(self.simple_clean_corpus(corpusEmploymentPrices))

                print('Corpora from link ' + str(n) + ' cleaned and collected')

        return date, overallEconomicActivity, employmentPrices        

    def str_to_datetime(self, date: str):

        date = re.sub('\\s', '', date)

        date = datetime.datetime.strptime(date, '%B%d,%Y')

        return date

dataEngineering1 = data_engineering_1()    
    
years = range(1996,2020)

BB_urls = list(map(dataEngineering1.year_link_create, years)) 

links = list(map(dataEngineering1.find_links, BB_urls))   

links = [item for sublist in links for item in sublist] # unnests lists
    
updated_lists = list(map(dataEngineering1.format_links, links))

print('Collected Links')

date, overallEconomicActivity, employmentPrices = dataEngineering1.pull_corpora_17_20(updated_lists)

beigeBookExtracts= pd.DataFrame({"Date":date,
                                 "OverallEconomicActivity":overallEconomicActivity,
                                 "EmploymentPrices":employmentPrices})

beigeBookExtracts['Date'] = beigeBookExtracts['Date'].apply(lambda x: dataEngineering1.str_to_datetime(x))