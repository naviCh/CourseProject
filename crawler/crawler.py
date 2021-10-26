import praw 
from pathlib import Path


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
        
    
    def crawl(self, sub, start, end):
        """
        Crawls subreddit and finds headlines between two dates 

        Parameters
        ----------
        sub: str 
            Subreddit
        start: str 
            Start date 
        End: str 
            End date

        Returns
        -------
        List of headlines and links
        """
        headlines = set() 
        subreddit = self.reddit.subreddit(sub)
        for submission in subreddit.new(limit=None): 
            headlines.add(submission.title)
        print(len(headlines))
