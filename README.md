# CourseProject

Please fork this repository and paste the github link of your fork on Microsoft CMT. Detailed instructions are on Coursera under Week 1: Course Project Overview/Week 9 Activities.

## Installation
From project root directory, run: 
```bash
pip install -r requirements.txt
```

## Setup 
### Secrets
Go to https://www.reddit.com/prefs/apps/ to get a `client_id`,`client_secret`, and `user_agent`.
The file `secrets` should contain key-value pairs of the format `key=value` and should be placed in the project root directory. The secrets needed are:

* `client_id` - Client ID for personal script use 
* `client_secret` - Secret
* `user_agent` - Reddit Username

## Running the baseline code
In order to run our baseline model on the redditCrawlerData that lives in the crawler directory, run:
```bash
cd baseline
python baseline_sentiment.py
```

The results of the baseline sentiment analysis are written back into the input redditCrawlerData file in the very first column so they can be compared against human sentiment ratings.  This baseline uses the nltk package, specifically the SentimentIntensityAnalyzer class within nltk.sentiment.  An instance of the SentimentIntensityAnalyzer class has the polarity_scores method which takes a string as input and returns various metrics relating to whether the sentiment was deemed negative, neutral, or positive.  The metric we pay most attention to was the "compound" value, which is a float value between -1 and 1 inclusive, where -1 is the most negative and 1 is the most positive.  In order to come up with a compound value for one particular Reddit link, we ran the polarity_scores method on both the title and the comments on the links separately and took a weighted average.  This weighted average was then translated into -1, 0, or 1 in order to make them more directly comparable to the human sentiment ratings, which only took those discrete values.

Currently, baseline_sentiment.py expects the input data to be in the redditCrawlerData file and won't work with any other name or path.  Future improvements of this code include being able to specify an input path, specify the weights in the weighted average baseline sentiment calculation, and specify the compound cutoffs for determining negative, neutral, and positive sentiment.