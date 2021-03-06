import tweepy
import json
from apis.filter import Filter
from apis.db import DBHelper

'''
Author: Ankit Kumar
Tweet Filter Module
Get Tweets from DB and Filter Them
Push Tweets that satisfy the Constraint to Filter DB
'''

class TweetFilter:
    '''
    Tweet Filter Class
    '''

    def __init__(self, args):
        self.logger = args.logger

        config = json.load(open(args.config))

        self.filter = Filter(dict(logger=args.logger, filter_path=config['filter_path']))
        self.db = DBHelper(dict(logger=args.logger))

    def run(self):
        self.logger.debug("Starting to Filter Tweets!")

        # Initialize Pagination Data
        page_items_count = 1000
        page = 1

        while True:
            # Get 1000 Tweets
            tweets = self.db.get_tweets(page, page_items_count)

            # Filter Tweets
            for tweet in tweets:
                filtered_tags = self.filter.check(tweet)
                if filtered_tags is not None:
                    filtered_tweet = dict(tweetid=tweet['tweetid'], tags=filtered_tags, lrscore=0)
                    self.db.add_filtered_tweet(filtered_tweet)

            # Stopping Condition
            if len(tweets) < page_items_count:
                break
            else:
                page += 1



def filter_tweets(args):
    '''
    Function called by the CommandLine Parser
    '''
    tweetFilter = TweetFilter(args)
    tweetFilter.run()