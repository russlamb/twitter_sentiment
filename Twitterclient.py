import re

import tweepy
from textblob import TextBlob
from tweepy import OAuthHandler
import os
import errno

class TwitterClient(object):
    '''
    Generic Twitter Class for sentiment analysis.
    '''

    def __init__(self):
        '''
        Class constructor or initialization method.
        '''
        # keys and tokens from the Twitter Dev Console
        
        #consumer_key = keyring.get_password("Twitter", "consumer_key")
        #consumer_secret = keyring.get_password("Twitter", "consumer_secret")
        #access_token = keyring.get_password("Twitter", "access_token")
        #access_token_secret = keyring.get_password("Twitter", "access_token_secret")
        
        # use environment instead of keyring
        
        consumer_key = os.environ.get("consumer_key")
        consumer_secret = os.environ.get("consumer_secret")
        access_token = os.environ.get("access_token")
        access_token_secret = os.environ.get("access_token_secret")
        
        # If enrivonment variables missing, raise an error
        if (not consumer_key or 
                not consumer_secret or
                not access_token or
                not access_token_secret):
            raise OSError(errno.ENODATA, "Environment variables not set for Twitter API")

        # attempt authentication
        try:
            # create OAuthHandler object
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            # set access token and secret
            self.auth.set_access_token(access_token, access_token_secret)
            # create tweepy API object to fetch tweets
            self.api = tweepy.API(self.auth)
        except:
            print("Error: Authentication Failed")

    def clean_tweet(self, tweet):
        '''
        Utility function to clean tweet text by removing links, special characters
        using simple regex statements.
        '''
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

    def get_tweet_sentiment(self, tweet):
        '''
        Utility function to classify sentiment of passed tweet
        using textblob's sentiment method
        '''
        # create TextBlob object of passed tweet text
        analysis = TextBlob(self.clean_tweet(tweet))
        # set sentiment
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'
            
    def get_tweet_polarity(self, tweet):
        '''
        RL added 11/6/18
        
        Utility function to get polarity of passed tweet
        using textblob's sentiment method
        '''
        # create TextBlob object of passed tweet text
        analysis = TextBlob(self.clean_tweet(tweet))
        # set sentiment
        return analysis.sentiment.polarity


    def tweepy_search(self, query, count):
        searched_tweets = []
        last_id = -1
        
        max_tweets = int( count )
        while len(searched_tweets) < max_tweets:
            count = max_tweets - len(searched_tweets)
            try:
                new_tweets = self.api.search(q=query, count=count, max_id=str(last_id - 1))
                if not new_tweets:
                    print("no new tweets")
                    break
                searched_tweets.extend(new_tweets)
                last_id = new_tweets[-1].id
            except tweepy.TweepError as e:
                
                # depending on TweepError.code, one may want to retry or wait
                # to keep things simple, we will give up on an error
                print("error fetching tweets: {}".format(e))
                break
        return searched_tweets

    def get_tweets(self, query, count=10):
        '''
        Main function to fetch tweets and parse them.
        '''
        # empty list to store parsed tweets
        tweets = []

        try:
            # call twitter api to fetch tweets
            #fetched_tweets = self.api.search(q=query, count=count)
            fetched_tweets = self.tweepy_search(query, count)

            # for debugging / finding tweet properties
            #if len(fetched_tweets)>0:
            #    print(fetched_tweets[0]._json)

            # parsing tweets one by one
            for tweet in fetched_tweets:
                # empty dictionary to store required params of a tweet
                parsed_tweet = {}

                # saving text of tweet
                parsed_tweet['text'] = tweet.text
                # saving sentiment of tweet
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)
                parsed_tweet['polarity'] = self.get_tweet_polarity(tweet.text)
                parsed_tweet['url'] = "https://twitter.com/statuses/{}".format(tweet.id_str)  # add url back to tweet
                parsed_tweet['retweets'] = tweet.retweet_count
                parsed_tweet['favorites'] = tweet.favorite_count
                parsed_tweet['language'] = tweet.lang

                # appending parsed tweet to tweets list
                if tweet.retweet_count > 0:
                    # if tweet has retweets, ensure that it is appended only once
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)

                # return parsed tweets
            return tweets

        except tweepy.TweepError as e:
            # print error (if any)
            print("Error : " + str(e))
