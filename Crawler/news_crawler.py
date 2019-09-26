#!/usr/bin/env python
# encoding=utf-8

import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import datetime

news_list = []

## Article content class
class Content:

    ## base class for all articles
    def __init__(self, keyword, url, title, body):
        self.keyword = keyword
        self.url = url
        self.title = title
        self.body = body
        

    ## function to control output 
    ## Can be tailored to output the desired content
    def appendList(self):
        news_item = {
            'symbol': self.keyword,
            'title': self.title,
            'text': self.body
            #'url': self.url
        }
        news_list.append(news_item)


## Website structure class
## Parameters to be speficied by us in "sites" 
class Website:
    def __init__(self, name, url, searchUrl, resultListing, resultUrl, absoluteUrl, titleTag, bodyTag):
        self.name = name
        self.url = url
        self.searchUrl = searchUrl
        self.resultListing = resultListing
        self.resultUrl = resultUrl
        self.absoluteUrl = absoluteUrl
        self.titleTag = titleTag
        self.bodyTag = bodyTag


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
        if childObj is not None and len(childObj) > 0:
            return childObj[0].get_text()
        return ''

    ##  Main search function that searches for a given keyword and records all pages returned 
    def search(self, keyword, site):
        bs = self.getPage(site.searchUrl + keyword) ## e.g. http://www.reuters.com/search/news?blob=MSFT
        searchResults = bs.select(site.resultListing)
        for result in searchResults:
            url = result.select(site.resultUrl)[0].attrs['href'] ## Select the article urls 
           
            if(site.absoluteUrl):  # Check whether it's a relative or an absolute URL
                bs = self.getPage(url)
            else:
                bs = self.getPage(site.url + url)
            if bs is None:
                print('Error with the URL or the page. ') 
                return
            title = self.safeGet(bs, site.titleTag) ## grab title 
            body = self.safeGet(bs, site.bodyTag) ## grab body 
            if title != '' and body != '':
                content = Content(keyword, url, title, body) ## Structure the article content for output 
                content.appendList()





## Here to specify a list of websites along with relevant information for scraping 
## Double check each parameter before running 
## name, url, searchUrl, resultListing, resultUrl, absoluteUrl, titleTag, bodyTag
sitesParam = [
    ['Reuters', 'http://reuters.com', 'http://www.reuters.com/search/news?blob=',
    'div.search-result-content', 'h3.search-result-title a', False, 'h1',
    'div.StandardArticleBody_body']

#    ['SCMP', 'https://www.scmp.com', 'https://www.scmp.com/content/search/',
#    'li.search-results__item item', 'div.wrapper__content content a', False, 'h1',
#    'div.details__body body', 'div.wrapper__published-date']
# The SCMP one is not working though
    
]
sites = []
for row in sitesParam:
    sites.append(Website(row[0], row[1], row[2],row[3], row[4], row[5], row[6], row[7]))


crawler = Crawler()

## Here to specify keywords(should be tickers)
## e.g. ['ADOM', 'ASV', 'AESEW', 'EMMA']
suspended = pd.read_csv('"Enter_Your_Path_Here"')
keywords = np.asarray(suspended['Symbol'])
## keywords =['ADOM', 'ASV', 'AESEW', 'GOOGL', 'MSFT']

for k in keywords:
    print('Working on: ' + k + ' now')
    for s in sites:
        crawler.search(k, s)


output_file = datetime.datetime.now().strftime("news_output_%Y-%m-%d-%H-%M.csv")
df_news_output = pd.DataFrame(news_list)
for n in news_list:
    df_news_output.loc[len(df_news_output)] = n

df_news_output.to_csv(output_file, encoding='utf-8', index=False)

