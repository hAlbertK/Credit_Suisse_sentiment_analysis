#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  3 17:43:08 2019

@author: peilin
"""

import re
import csv
import time
from bs4 import BeautifulSoup
import urllib
import pandas as pd
import requests
import json
import string
from newspaper import Article

url = 'https://listingcenter.nasdaq.com/IssuersPendingSuspensionDelisting.aspx'
response = urllib.request.urlopen(url)
soup = BeautifulSoup(response, 'html.parser')
table = soup.find('table', {'class': 'rgMasterTable'})

stock_list = []
for tr in table.tbody.findAll('tr'):
    row = []
    for td in tr.findAll('td'):
        text = td.getText()
        if text == '\xa0':
            text = 'None'
        row.append(text)
    stock_list.append(row)

df = pd.DataFrame(stock_list)
df.columns = ['Issuer Name','Symbol','Reason','Status','Effective Date','Form 25 Date']
ticker = df.to_dict('index')

# Build query structure for google news
# Found that the Issuer name query style is better for google news
def build_query_list():
    query_list = []
    for i in ticker:
        comp = re.sub(r'[,\.]', ' ', ticker[i]['Issuer Name']).split()
        str_comp = ' '.join(comp)
        query_list.append(str_comp)
    return query_list

# Request the query list
query_list_google_news = build_query_list()

def parseSingleNews(query):
    # Create a list to storage relevant information of the news 
    news_list = []
    # Use the ticker_index to obtain stock name and stock ID within the ticker dictionary
    ticker_index = 0
    
    for q in query:
        
        # Parse the specific URL for each different stock
        # Using the google news RSS
        q1 = q.replace(' ','+')
        url = 'https://news.google.com/rss/search?q=' + q1 + '+stock+suspend&hl=en-US&gl=US&ceid=US:en'
        response = urllib.request.urlopen(url)
        soup = BeautifulSoup(response, 'html.parser')
        channel = soup.find('channel')
        
        # Grab the first three news for each company
        for item in soup.findAll('item')[0:3]:
            single_stock = {}
            single_stock['STOCK ID'] = ticker[ticker_index]['Symbol']
            url = ''
            abst = ''
            description = item.find('description').get_text()
            match = re.search(r'(href=")(.*)(" target)', description)
            if (match):
                url = match.group(2)
                single_stock['URL'] = url
            single_stock['PUBDATE'] = item.find('pubdate').get_text()
            single_stock['EDITED_DATE'] = item.find('pubdate').get_text()
            single_stock['SCRAPED_DATE'] = time.strftime("%Y-%m-%d-%H-%M")
            single_stock['TITLE'] = item.find('title').get_text()
            
            # Put the stock information in the list: news_list
            news_list.append(single_stock)
            
        # Move on to the next company
        ticker_index += 1
    
    return(news_list)
    
news_list = parseSingleNews(query_list_google_news)

# Get the news content for each article we have got using the newspaper library
def get_content(single_stock):
    single_stock['content'] = ''
    url = single_stock['URL']
    try:
        news = Article(url, language='en')
        news.download()
        news.parse()
        single_stock['content'] = news.text
        return(single_stock)
    except Exception as e:
        single_stock['content'] = 'Error'
        return(single_stock)

for single_stock in news_list:
    get_content(single_stock)

# write nested list of dict to csv
with open("suspended_news.csv", 'w') as f:
    w = csv.writer(f)
    fieldnames=news_list[0].keys()  # solve the problem to automatically write the header
    w.writerow(fieldnames)
    for row in news_list:
        w.writerow(row.values())