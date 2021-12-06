import os
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
		comments_weight = 0.2 if comments else 0.0
		headline_weight = 1.0 - comments_weight

		pol_score_headline_dict = sia.polarity_scores(headline)
		pol_score_comments_dict = sia.polarity_scores(comments)
		compound_score = pol_score_headline_dict['compound']*headline_weight + pol_score_comments_dict['compound']*comments_weight

		if compound_score < -0.2:
			baseline_sentiment = -1
		elif -0.2 <= compound_score <= 0.2:
			baseline_sentiment = 0
		else:
			baseline_sentiment = 1

		pol_score_dict = {
			'BASELINE_SENTIMENT': baseline_sentiment,
			'SENTIMENT_IVAN': row.SENTIMENT_IVAN,
			'SENTIMENT_JEFF': row.SENTIMENT_JEFF,
			'SENTIMENT_AUSTIN': row.SENTIMENT_AUSTIN,
			'TITLE': headline,
			'URL': row.URL,
			'DATE': row.DATE,
			'UPVOTE': row.UPVOTE,
			'DOWNVOTE': row.DOWNVOTE,
			'COMMENTS': comments,
		}

		results.append(pol_score_dict)

	return pd.DataFrame.from_records(results)

if __name__ == "__main__":
	submissions = pd.read_csv(os.path.dirname(os.getcwd()) + "/crawler/redditCrawlerData.csv")
	submissions.columns = submissions.columns.str.replace(' ', '_')

	# TODO: choose sentiment method based on command line argument
	sentiments = sentiment_headline_with_comments(submissions)
	sentiments.to_csv(os.path.dirname(os.getcwd()) + '/crawler/redditCrawlerData.csv', index=False)