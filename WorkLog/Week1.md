# Worklog

### Week 1
### 9.19 - 9.26

#### Tasks
  1. Check crawling availability (robots.txt)

  2. Build scrapers for each site * 

  3. Integration with previous CS code 

#### The Scraper
A simple way to do this is to utilize the search bar of each website. Load the keywords to be searched to the search bar, identify the internal article links in each result: ` <span class="result">` or something like this. 
The returned URL could be relative or absolute. 
Then extract the required text from each article page.
The returned text data should be loaded into dataframe, with proper attribute names. (Then output a csv file?) 

<p> I used lots of previous code. </p> 


#### To run the crawler
Simply open a commandline tool, cd to the directory and run:
```bash 
$ python suspended_crawler.py
```
and 
```bash 

$ python news_crawler.py
```
<p> The output should be two csv files. Need to specify parameters and the suspended stock list path in the news_crawler.py. </p>
<p> The previous code is a better approach to this task I think. My implementation is kind of crappy and definitely needs to be replaced. </p>

## Note: Up to now(Sept 25), we don't have the suspended stock tickers. So I just used the suspension list on NASDAQ:  https://listingcenter.nasdaq.com/IssuersPendingSuspensionDelisting.aspx to test the code. 

#### TODO 
1. Work on the publish date of each article
2. Get more articles from various websites 
3. Examine the relevance of the returned articles 
4. Twerk the previous implementation code a little bit for a more desirable output 
5. 
6. 
