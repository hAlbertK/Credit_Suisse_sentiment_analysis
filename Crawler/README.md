
#### The Scraper
The new scraper is built on top of the previous one and is tailored to utilize Google News search function. The class structure is preserved. 

#### To run the crawler
Simply open a commandline tool, cd to the directory and run:
```bash 
$ python suspended_crawler.py
```
and 
```bash 
$ python google_news_crawler.py
```
<p> The output should be two csv files. However, the news article output is ridiculously large. Expect a lot of duplicates and irrelevant articles. I will keep working on tweaking the code to cut down the size and to find the most relevant ones. </p>


#### TODO 
1. Examine the relevance of output documents 
2. Reduce the size of output 
3. 
