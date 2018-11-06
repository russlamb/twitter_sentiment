import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob
import os
from Twitterclient import TwitterClient


def main():
    # creating object of TwitterClient Class
    api = TwitterClient()
    
    # calling function to get tweets
    tweets = api.get_tweets(query='Donald Trump', count=200)
    print(tweets)
    # picking positive tweets from tweets
    ptweets = sorted([tweet for tweet in tweets if tweet['sentiment'] == 'positive'],key= lambda kv: kv['polarity'], reverse=True)
    # percentage of positive tweets
    print("Positive tweets percentage: {} %".format(100 * len(ptweets) / len(tweets)))
    # picking negative tweets from tweets
    ntweets = sorted([tweet for tweet in tweets if tweet['sentiment'] == 'negative'],key= lambda kv: kv['polarity'])
    # percentage of negative tweets
    print("Negative tweets percentage: {} %".format(100 * len(ntweets) / len(tweets)))
    # percentage of neutral tweets
    print("Neutral tweets percentage: {} % ".format(100 * (len(tweets) - len(ntweets) - len(ptweets)) / len(tweets)))

    
    # printing first 5 positive tweets
    print("\n\nPositive tweets:")
    for tweet in ptweets[:10]:
        print(tweet['text'])
        print(tweet['polarity'])

    # printing first 5 negative tweets
    print("\n\nNegative tweets:")
    for tweet in ntweets[:10]:
        print(tweet['text'])
        print(tweet['polarity'])

def test_tweepy():
    consumer_key = os.environ.get("consumer_key")
    consumer_secret = os.environ.get("consumer_secret")
    access_token = os.environ.get("access_token")
    access_token_secret = os.environ.get("access_token_secret")

    # attempt authentication
    # create OAuthHandler object
    auth = OAuthHandler(consumer_key, consumer_secret)
    # set access token and secret
    auth.set_access_token(access_token, access_token_secret)
    # create tweepy API object to fetch tweets
    api = tweepy.API(auth)

    #tweets = api.search("Trump", count=100)
    tweets = api.home_timeline()
    print(tweets)

if __name__ == "__main__":
    # calling main function
    # print("test")
    main()
    #test_tweepy()
