import praw 
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
    
    def crawl(self, sub, start, upperlimit):
        """
        Crawls subreddit and finds headlines between two dates 

        Parameters
        ----------
        sub: string
            Subreddit to crawl
        start: datetime
            Start date 
        upperlimit: int
            Limit of submissions
        Returns
        -------
        List of submissions
        """
        headlines = [] 
        start_epoch = int(start.timestamp())
        submissions = list(self.api.search_submissions(after=start_epoch,
                                                       subreddit=sub,
                                                       limit=upperlimit))

        # submission follows https://praw.readthedocs.io/en/stable/code_overview/models/submission.html
        return submissions
