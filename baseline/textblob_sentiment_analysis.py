from textblob import TextBlob
import pandas as pd
import os

from baseline_sentiment import input_into_csv

def textblob_sentiment_headline_with_comments(submissions):
    results = []
    for row in submissions.itertuples():
        headline = row.TITLE
        comments = str(row.COMMENTS)

        # Setting weights for headline sentiment and comments sentiment
        comments_weight = 0.1 if comments else 0.0
        headline_weight = 1.0 - comments_weight

        pol_score_headline = TextBlob(headline).sentiment
        pol_score_comments = TextBlob(comments).sentiment

        compound_score = pol_score_headline.polarity * headline_weight + pol_score_comments.polarity * comments_weight

        results.append(input_into_csv(row, headline, comments, compound_score, -0.1, 0.1))
    return pd.DataFrame.from_records(results)


if __name__ == "__main__":
    submissions = pd.read_csv(os.path.dirname(os.getcwd()) + "/crawler/redditCrawlerData.csv")
    submissions.columns = submissions.columns.str.replace(' ', '_')

    # TODO: choose sentiment method based on command line argument
    sentiments = textblob_sentiment_headline_with_comments(submissions)
    sentiments.to_csv(os.path.dirname(os.getcwd()) + '/baseline/textBlobCrawlerData.csv', index=False)
