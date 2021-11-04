import praw 
from praw.models import MoreComments
from psaw import PushshiftAPI
from pathlib import Path
import datetime as dt

class Crawler: 
    def __init__(self, secrets_file=Path("./secrets")): 
        """
        Intialize Crawler

        Parameters
        ----------
        secrets_file: str 
            Path to secrets file  
        """
        self.secrets = dict([x.split("=") for x in secrets_file.read_text().strip("\n").split("\n")])
        self.reddit = praw.Reddit(client_id=self.secrets['client_id'],
                                  client_secret=self.secrets['client_secret'],
                                  user_agent=self.secrets['user_agent']
                                )
        self.api = PushshiftAPI(self.reddit)
   
    def crawl(self, sub, start, end, upperlimit):
        """
        Crawls subreddit and finds headlines between two dates 

        Parameters
        ----------
        sub: string
            Subreddit to crawl
        start: datetime
            Start date 
        end: datetime 
            End date 
        upperlimit: int
            Limit of submissions
        Returns
        -------
        List of submission objects
        """
        start_epoch = int(start.timestamp())
        end_epoch = int(end.timestamp())
        submissions = list(self.api.search_submissions(after=start_epoch,
                                                       before=end_epoch,
                                                       subreddit=sub,
                                                       limit=upperlimit))
        # submission follows https://praw.readthedocs.io/en/stable/code_overview/models/submission.html
        return submissions

    def filter_submissions(self, submissions, lower=2, upper=5000): 
        """
        Filters submissions based on number of upvotes 

        Parameters
        ----------
        submissions: list
            list of submission objects from praw
        lower: int default 2
            lower bound of upvotes 
        upper: int default 5000
            higher bound of upvotes

        Returns
        -------
        List of Submissions 
        """
        filtered = [] 
        for submission in submissions: 
            if submission.score >= lower and submission.score <= upper: 
                filtered.append(submission)
        return filtered
    
    def get_comments(self, submission, threshold=10):
        """
        Gets Comments from a praw submission above a threshold

        Parameters
        ----------
        submission: submission
            praw submission object
        threshold: int 
            top n comments to return 

        Returns
        -------
        List of Comments in Markdown
        """
        submission.comment_sort = "top"
        submission.comments.replace_more(limit=None)
        comments = submission.comments
        return comments[0:threshold] if threshold < len(comments) else comments

    def sort_format_submissions(self, submissions):
        """
        Sorts submissions objects based on number of upvotes
        Mostly for testing purposes 

        Parameters
        ---------
        submissions: submission 
            list of praw submission objects
        
        Returns
        -------
        Returns a list of formatted submission dictionaries 
        """
        reformated = [] 
        for submission in submissions: 
            entry = {} 
            entry['title'] = submission.title
            entry['url'] = submission.url
            post_date = dt.datetime.utcfromtimestamp(submission.created_utc)
            post_date_str = post_date.strftime("%m/%d/%Y")
            entry['postdate'] = post_date_str
            entry['upvotes'] = submission.score 
            downvotes = submission.score / submission.upvote_ratio - submission.score
            entry['downvotes'] = int(downvotes)
            reformated.append(entry)
        sorted_submissions = sorted(reformated, key=lambda x: x['upvotes'], reverse=True)
        return sorted_submissions