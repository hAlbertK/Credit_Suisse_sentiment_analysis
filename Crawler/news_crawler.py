#!/usr/bin/env python
# encoding=utf-8

import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import datetime
import re
import time
from random import randint
from newspaper import Article

news_list = []

def get_content(stock_url):
    try:
        news = Article(stock_url, language='en')
        news.download()
        news.parse()
    except Exception: # Some urls cannot be resolved 
        return ''
    return news.text

class Content:

    ## base class for all articles
    def __init__(self, keyword, url, title, pubDate, name, content):
        self.keyword = keyword
        self.url = url
        self.title = title
        self.pubDate = pubDate
        self.name = name
        self.content = content
        

    ## function to control output 
    ## Can be tailored to output the desired content
    def appendList(self):
        news_item = {
            'SYMBOL': self.keyword,
            'URL': self.url,
            'TITLE': self.title,
            'PUBLISH_TIME': self.pubDate,
            'SITE_NAME': self.name,
            'CONTENT': self.content
        }
        news_list.append(news_item)


## Website structure class
## Not really necessary in crawling google news 
class Website:
    def __init__(self, name):
        self.name = name


## Crawler class 
class Crawler:

    def getPage(self, url):
        try:
            req = requests.get(url)
        except requests.exceptions.RequestException:
            return None
        return BeautifulSoup(req.text, 'html.parser')

    def safeGet(self, pageObj, selector):
        childObj = pageObj.select(selector)
        if childObj is not None:
            return childObj[0].get_text()
        return ''

    ##  Main search function that searches for a given keyword and records all pages returned 
    def search(self, query_keyword, query_site, site):
        # https://news.google.com/search?q=site%3Astreetinsider.com%20"ADOM"%20when%3A1y&hl=en-US&gl=US&ceid=US%3Aen

        time.sleep(randint(0, 3)) ## specify a throttle to avoid hitting servers too hard since we have more requests; a randomly generated int

        bs = self.getPage('https://news.google.com/search?q=site%3A'+query_site+'%20%22'+query_keyword+'%22%20when%3A1y&hl=en-US&gl=US&ceid=US%3Aen')
        contents = bs.find("main", attrs = {"class" : "HKt8rc CGNRMc"})
        articles = contents.find_all("div", attrs = {"class": "xrnccd"})
 #      tlist = []
        for e in articles[0:5]: # select top-k docs as relevant 
            title = e.find("h3").get_text()
            try:
                pubDate = e.time['datetime']
            except Exception: ## Some articles do not have pub date. Ignore these for now 
                pass
            url = e.find('a').get('href')
            ab_url = 'https://news.google.com'+ url
            siteName = e.find('a', attrs = {"class": "wEwyrc AVN2gc uQIVzc Sksgp"}).get_text()
            content = get_content(ab_url)
            returned = Content(query_keyword, ab_url, title, pubDate, siteName, content)
            returned.appendList()




## Not necessarily needed in crawling Google News 
## I just preserved the previous structure for later use
sitesParam = [
  #  ['Reuters', 'http://reuters.com', 'http://www.reuters.com/search/news?blob=',
  #  'div.search-result-content', 'h3.search-result-title a', False, 'h1',
  #  'div.StandardArticleBody_body', 'div.ArticleHeader_date', 'div.ArticleHeader_date'], 
    ['GoogleNews']
]

target_site = []
for row in sitesParam:
    target_site = Website(row[0])

# Instantiate a crawler 
crawler = Crawler()

# All tickers to search 
suspended = pd.read_csv('/Users/Frank.peng/Desktop/VS_workspace/Python_in_VS/CS_Project/Crawler/suspended_2019-10-03-11-39.csv')
query_keywords = np.asarray(suspended['Symbol'])


# All websites to search
# The sec does not return results though, need to figure that out 
query_sites = ['scmp.com', 'streetinsider.com', 'theguardian.com', 'forbes.com', 'bloomberg.com', 'reuters.com', 'cnbc.com', 'nasdaq.com', 'stockmarketwire.com', 
'prnewswire.com', 'globenewswire.com', 'sec.gov', 'channelnewsasia.com', 'straitstimes.com', 'finance.yahoo.com']

# Iterate each site and each keyword 
for s in query_sites:
    for k in query_keywords:
        print('working on ticker:' + k + '    |   on the website: ' + s + '    now')
        crawler.search(k, s, target_site)
        


output_file = datetime.datetime.now().strftime("news_output_%Y-%m-%d-%H-%M.csv")
df_news_output = pd.DataFrame(news_list)
for e in news_list:
    df_news_output.loc[len(df_news_output)] = e

# Add scraped time, reindex df
df_news_output['SCRAPED_TIME']=datetime.datetime.now().strftime("%Y-%m-%d-%H-%M")
df_news_output = df_news_output.reindex(columns=['SYMBOL','SITE_NAME', 'URL','PUBLISH_TIME', 'SCRAPED_TIME', 'TITLE', 'CONTENT'])
df_news_output.to_csv(output_file, encoding='utf-8', index=False)

    