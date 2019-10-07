### Aggregated_Result
Contains news articles from the following websites:

- www.reuters.com 
- www.cnbc.com 
- https://www.nasdaq.com/
- https://www.prnewswire.com/
- https://globenewswire.com/
- finance.yahoo.com

I tried to narrow down the query terms and retrieve more related articles. 
However there are still duplicates in this file and need to be dealt with later. 


### Other CSVs
The rest csv files are scraping results of other websites. 
I also noted that the following websites are problematic because:
- www.scmp.com
(few relevant results)
- https://www.theguardian.com/ 
(no relevant results)
- http://www.stockmarketwire.com/
(Cannot get results via google news; few relevant news articles)
- https://www.sec.gov/edgar/searchedgar/companysearch.html
(SEC site provides filings and reports of each company, and these are included in the scraping results of other sites)
- https://www.channelnewsasia.com
 (few relevant results; mostly from Reuters) 
- https://www.straitstimes.com
 (few relevant results; mostly from Reuters)

### Working on:
- https://www.forbes.com/
- https://www.streetinsider.com/
I can retrieve title and url of the articles, but kept getting HTTP 416 error.

- Bloomberg
"Please make sure your browser supports JavaScript and cookies and that you are not blocking them from loading"
