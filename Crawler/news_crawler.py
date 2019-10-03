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
    def __init__(self, keyword, url, title, body, pubDate, editDate, name):
        self.keyword = keyword
        self.url = url
        self.title = title
        self.body = body
        self.pubDate = pubDate
        self.editDate = editDate
        self.name = name
        

    ## function to control output 
    ## Can be tailored to output the desired content
    def appendList(self):
        news_item = {
            'SITE_NAME':self.name,
            'SYMBOL': self.keyword,
            'URL': self.url,
            'TITLE': self.title,
            'CONTENT': self.body,
            'PUBLISH_TIME': self.pubDate,
            'EDITED_TIME': self.editDate
        }
        news_list.append(news_item)


## Website structure class
## Parameters to be speficied by us in "sites" 
class Website:
    def __init__(self, name, url, searchUrl, resultListing, resultUrl, absoluteUrl, titleTag, bodyTag, pubDateTag, editDateTag):
        self.name = name
        self.url = url
        self.searchUrl = searchUrl
        self.resultListing = resultListing
        self.resultUrl = resultUrl
        self.absoluteUrl = absoluteUrl
        self.titleTag = titleTag
        self.bodyTag = bodyTag
        self.pubDateTag = pubDateTag
        self.editDateTag = editDateTag


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
            
            editDate = self.safeGet(bs, site.editDateTag) ## grab editDate
            pubDate = self.safeGet(bs, site.pubDateTag) ## grab pubDate
            body = self.safeGet(bs, site.bodyTag) ## grab body 
            title = self.safeGet(bs, site.titleTag) ## grab title 
            if title != '' and body != '':
                content = Content(keyword, site.url + url, title, body, pubDate, editDate, site.name) ## Structure the article content for output 
                content.appendList()





## Here to specify a list of websites along with relevant information for scraping 
## Feel free to add as many sites as you want, but double check each parameter before running 
## self, name, url, searchUrl, resultListing, resultUrl, absoluteUrl, titleTag, bodyTag, pubDateTag, editDateTag
sitesParam = [
    ['Reuters', 'http://reuters.com', 'http://www.reuters.com/search/news?blob=',
    'div.search-result-content', 'h3.search-result-title a', False, 'h1',
    'div.StandardArticleBody_body', 'div.ArticleHeader_date', 'div.ArticleHeader_date']
]
sites = []
for row in sitesParam:
    sites.append(Website(row[0], row[1], row[2],row[3], row[4], row[5], row[6], row[7], row[8], row[9]))


crawler = Crawler()

## Here to specify a query list (should be tickers) as keywords
## e.g. ['ADOM', 'ASV', 'AESEW', 'EMMA']
suspended = pd.read_csv('Enter_YOUR_PATH_HERE')
keywords = np.asarray(suspended['Symbol'])
## keywords =['ADOM', 'ASV', 'AESEW', 'GOOGL', 'MSFT']

for k in keywords:
    print('Working on: ' + k + ' now')
    for targetSite in sites:
        crawler.search(k, targetSite)


output_file = datetime.datetime.now().strftime("news_output_%Y-%m-%d-%H-%M.csv")
df_news_output = pd.DataFrame(news_list)
for e in news_list:
    df_news_output.loc[len(df_news_output)] = e

df_news_output['SCRAPED_TIME']=datetime.datetime.now().strftime("%Y-%m-%d-%H-%M")
df_news_output = df_news_output.reindex(columns=['SITE_NAME','SYMBOL','URL','PUBLISH_TIME','EDITED_TIME','SCRAPED_TIME', 'TITLE', 'CONTENT'])
df_news_output.to_csv(output_file, encoding='utf-8', index=False)

