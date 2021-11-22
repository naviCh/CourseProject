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

def sentiment_headline_with_comments(submissions):
	sia = SentimentIntensityAnalyzer()
	results = []

	for row in submissions.itertuples():
		headline = row.TITLE
		comments = str(row.COMMENTS)

		# Setting weights for headline sentiment and comments sentiment
		comments_weight = 0.1 if comments else 0.0
		headline_weight = 1.0 - comments_weight

		pol_score_headline_dict = sia.polarity_scores(headline)
		pol_score_comments_dict = sia.polarity_scores(comments)
		pol_score_dict = {
			'neg': pol_score_headline_dict['neg']*headline_weight + pol_score_comments_dict['neg']*comments_weight,
			'neu': pol_score_headline_dict['neu']*headline_weight + pol_score_comments_dict['neu']*comments_weight,
			'pos': pol_score_headline_dict['pos']*headline_weight + pol_score_comments_dict['pos']*comments_weight,
			'compound': pol_score_headline_dict['compound']*headline_weight + pol_score_comments_dict['compound']*comments_weight,
			'headline': headline,
			'comments': comments,
		}
		results.append(pol_score_dict)

	return pd.DataFrame.from_records(results)

if __name__ == "__main__":
	submissions = pd.read_excel("crawler/redditCrawlerData.xls")

	# TODO: choose sentiment method based on command line argument
	sentiments = sentiment_headline_with_comments(submissions)
	sentiments.to_csv('baseline_sentiment_results_headline_comments.csv', index=False)