import pandas as pd
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

def sentiment_headline_only(submissions):
	sia = SentimentIntensityAnalyzer()
	results = []

	for row in submissions.itertuples():
		headline = row.TITLE
		pol_score_dict = sia.polarity_scores(headline)
		pol_score_dict['headline'] = headline
		results.append(pol_score_dict)

	return pd.DataFrame.from_records(results)

def sentiment_headline_comments(submissions):
	pass

if __name__ == "__main__":
	submissions = pd.read_excel("crawler/redditCrawlerData.xls")

	# TODO: choose sentiment method based on command line argument
	sentiments = sentiment_headline_only(submissions)
	sentiments.to_csv('baseline_sentiment_results.csv', index=False)