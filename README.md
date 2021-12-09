# CS410 Course Project Documentation

Please fork this repository and paste the github link of your fork on Microsoft CMT. Detailed instructions are on Coursera under Week 1: Course Project Overview/Week 9 Activities.

## Presentation link
Please access the final project presentation at https://mediaspace.illinois.edu/media/t/1_40y3fxbn

## Contributions
* `Ivan Cheung` - Parser, Textblob analysis and manual annotations
* `Jeff Zhan` - Reddit crawler and manual annotations
* `Austin Wang` - Baseline NLTK sentiment analysis and manual annotations

## Installation
From project root directory, run: 
```bash
pip install -r requirements.txt
```

Running the baseline model also requires a one-time installation of the vader_lexicon.  After installing nltk via requirements.txt, open a terminal window in Python and run:
```bash
  >>> import nltk
  >>> nltk.download('vader_lexicon')
```

## Setup 
### Secrets
Go to https://www.reddit.com/prefs/apps/ to get a `client_id`,`client_secret`, and `user_agent`.
The file `secrets` should contain key-value pairs of the format `key=value` and should be placed in the project root directory. The secrets needed are:

* `client_id` - Client ID for personal script use 
* `client_secret` - Secret
* `user_agent` - Reddit Username

## Running the crawler 
Inside the `crawler` folder, `crawler.py` is a class object that represents the crawler for the Reddit API. In order to instantiate a crawler, the user must have completed the `setup` steps above. Examples of how to run `crawler` can be found in `parser` and below: 

```bash
from crawler import Crawler 
import datetime as dt

#grabbing 100 submissions from 2017/1/1 to 2018/1/1
start = dt.datetime(2020, 1, 1)
end = dt.datetime(2021, 7, 7)

crawler = Crawler() 
submissions = crawler.crawl("worldnews", start, end, 100) 
filtered_submissions = crawler.filter_submissions(submissions, lower=5, upper=1000)
for sub in filtered_submissions: 
    print(sub.score)
```
Having called `crawler.crawl()` the user can take these submission objects and perform the relevant functions necessary to `filter_submissions()` based on upvotes, `get_comments()` based on upvotes, and `sort_format_submissions()`. Please reference `crawler.py` for additional parameter information. 


## Running the parser
In order to run the parser, run:
```bash
python crawler/parser.py
```

The parser connects to the crawler class. The crawler class will first use the Reddit API psaw, as well as parameters such as SubReddit name, start date, end date, and number of submissions, to fetch the data into an object. Afterwards, to filter out low quality submissions, we use upvote count to filter out submissions below 10 upvotes. Finally, the parser would create an Excel file and write into multiple columns. We take the title, URL, Date of submissions, upvote/downvote count, as well as top 10 popular comments into our excel file for the sentiment analysis. We also include several empty columns for manual annotations as well as an empty column for the sentiment analysis results.

The columns for manual annotation were then populated by the team.

## Running the baseline NLTK Sentiment analysis code
In order to run our baseline model on the redditCrawlerData that lives in the crawler directory, run:
```bash
cd baseline
python baseline_sentiment.py
```

The results of the baseline sentiment analysis are written back into the input redditCrawlerData file in the very first column so they can be compared against human sentiment ratings.  This baseline uses the nltk package, specifically the SentimentIntensityAnalyzer class within nltk.sentiment.  An instance of the SentimentIntensityAnalyzer class has the polarity_scores method which takes a string as input and returns various metrics relating to whether the sentiment was deemed negative, neutral, or positive.  The metric we pay most attention to was the "compound" value, which is a float value between -1 and 1 inclusive, where -1 is the most negative and 1 is the most positive.  In order to come up with a compound value for one particular Reddit link, we ran the polarity_scores method on both the title and the comments on the links separately and took a weighted average.  This weighted average was then translated into -1, 0, or 1 in order to make them more directly comparable to the human sentiment ratings, which only took those discrete values.

Currently, baseline_sentiment.py expects the input data to be in the redditCrawlerData file and won't work with any other name or path.  Future improvements of this code include being able to specify an input path, specify the weights in the weighted average baseline sentiment calculation, and specify the compound cutoffs for determining negative, neutral, and positive sentiment.

## Running the TextBlob Sentiment analysis code
In order to run our textBlob model on the redditCrawlerData that lives in the crawler directory, run:
```bash
cd baseline
python textblob_sentiment_analysis.py
```

The textBlob model uses the same utility functions to write and read from CSV files as the NLTK analysis. The only part that is different is the weights of the comments and headlines on the final scoring, as well as using TextBlob sentiment function to calculate polarity. The result is stored in output file textBlobCrawlerData.csv.
