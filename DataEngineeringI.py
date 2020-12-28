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

# Creates links list

BB_urls = []    

for yr in range(1996,2020):
    
        BB_urls.append('https://www.federalreserve.gov/monetarypolicy/beigebook' + str(yr) + '.htm')
        
BB_urls.append(BB_2020_url)   

links = []

for BB_url in BB_urls:

    print('Pulling ' + str(BB_url))

    driver.get(BB_url)

    print('Loading page')

    tm.sleep(rd.randint(2, 4))

    soup = BeautifulSoup(driver.page_source, 'lxml')

    foundlinks = [str(l['href']) for l in soup.find_all("a", href=re.compile(r"[/]monetarypolicy[/]beigebook.*.htm"))]

    links.append(foundlinks)    

links = [item for sublist in links for item in sublist]

updated_links = []

for link in links:
    
    if 'https://www.federalreserve.gov' not in link:
        
        updated_links.append('https://www.federalreserve.gov' + link)
    
    else:
    
        updated_links.append(link)

print('Collected Links')

def simple_clean_corpus(corpus: str): 

            corpus = re.sub('\n|<p>|</p>|<br/>|<strong>.*</strong>', '', corpus)

            return corpus
        
# Creating the dataframe

date = []
overallEconomicActivity = []
employmentPrices = []
        
for n, link in enumerate(updated_links):
    
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

        overallEconomicActivity.append(simple_clean_corpus(corpusOverallEconomicActivity))

        employmentPrices.append(simple_clean_corpus(corpusEmploymentPrices))

        print('Corpuses from link ' + str(n) + ' cleaned and collected')
        
#     else:
        
#         date.append(re.sub('Last update:|\n|\\s{2,}',
#                            '',
#                            soup.find('div', {'id':'lastUpdate'}).text))
        
        
        
beigeBookExtracts = pd.DataFrame({"Date":date,
                                  "OverallEconomicActivity":overallEconomicActivity,
                                  "EmploymentPrices":employmentPrices})

def str_to_datetime(date: str):

    date = re.sub('\\s', '', date)

    date = datetime.datetime.strptime(date, '%B%d,%Y')
    
    return date

beigeBookExtracts['Date'] = beigeBookExtracts['Date'].apply(lambda x: str_to_datetime(x)) 

print(beigeBookExtracts)