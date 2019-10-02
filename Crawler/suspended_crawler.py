#!/usr/bin/env python
# encoding=utf-8

import re
import urllib
import requests 

from bs4 import BeautifulSoup
import csv
import pandas as pd 
import datetime

DOWNLOAD_URL = 'https://listingcenter.nasdaq.com/IssuersPendingSuspensionDelisting.aspx'


def download_page(url):
    return requests.get(url, headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'
    }).text


soup = BeautifulSoup(download_page(DOWNLOAD_URL),'lxml')
stock_list_section = soup.find('body').find('form').find('div', attrs={'align': 'center'})

output_file = datetime.datetime.now().strftime("suspended_%Y-%m-%d-%H-%M.csv")


stock_master_wrapper = stock_list_section.find('div', attrs={'class': 'masterwrapper'})
stock_main_container = stock_master_wrapper.find('div', attrs={'id': 'maincontainer'})
tbl_master = stock_main_container.find("div", attrs={'id': 'ctl00_tblMaster'})
stock_list = tbl_master.find('div', attrs={'id': 'grdView'})
table = stock_list.find('table', attrs={'class':'rgMasterTable'})

headers = ['Issuer Name','Symbol','Reason','Status','Effective Date','Form 25 Date']
df = pd.DataFrame(columns=headers)

stocks = []
for row in table.find_all("tr", attrs = {"class" : "rgRow"}):
    stocklist = []
    for cell in row.find_all("td"):
        stocklist.append(cell.text)
    stocklist = [element.replace('\xa0', 'None') for element in stocklist]
    stocks.append(stocklist)
##  print(stocklist)

## Stupid me. There is another rgaltrow class 
for row in table.find_all("tr", attrs = {"class" : "rgAltRow"}):
    stocklist = []
    for cell in row.find_all("td"):
        stocklist.append(cell.text)
    stocklist = [element.replace('\xa0', 'None') for element in stocklist]
    stocks.append(stocklist)

 
for e in stocks:
    df.loc[len(df)] = e

df = df.loc[df['Status'] == 'Suspended']
df.to_csv(output_file, encoding='utf-8', index=False)
