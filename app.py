import os
from Twitterclient import TwitterClient
from flask import Flask, jsonify, request, render_template, session, g
# from flask_paginate import Pagination, get_page_parameter

app = Flask(__name__)


def parse_int(number):
    try:
        return int(number)
    except ValueError as e:
        print("there was an error parsing {}".format(number))
        return None

@app.route('/')
def main():
    """twitter sentiment analysisinput  page"""
    app.logger.info('User accessed the main.html template')
    return render_template('main.html', title="Sentiment Analysis")

@app.route('/p')
def main_p():
    """Search twitter for positive tweets"""
    app.logger.info('User access main_p.html template')
    

    return render_template('main_p.html')

@app.route('/result')    
def result():
    """
    result page to result analysis
    """
    
    app.logger.info('User accessed the result template')
    query =  request.args.get("query")
    count =  request.args.get("count") 
    # output_format=request.args.get("format")
    count = parse_int(count) if parse_int(count) else 200
    
    if count>1000:      # set a maximum tweet count of 1000 to prevent overloading
        count = 1000
    
    if not query:
        query = "BX"
        
    api = TwitterClient()

    # calling function to get tweets
    tweets_with_dupes = api.get_tweets(query=query, count=count)
    unique_tweets = set([tweet['text'] for tweet in tweets_with_dupes])
    tweets = []
    for tweet in tweets_with_dupes:
        if tweet['text'] in unique_tweets:
            tweets.append(tweet)
            unique_tweets.remove(tweet['text'])


    ptweets = sorted([tweet for tweet in tweets if tweet['sentiment'] == 'positive'],key= lambda kv: kv['polarity'], reverse=True)
    ntweets = sorted([tweet for tweet in tweets if tweet['sentiment'] == 'negative'],key= lambda kv: kv['polarity'])
    summary = [
        { 
            "sentiment": "positive", 
            "count": len(ptweets), 
            "percentage": 100*len(ptweets) / len(tweets) if len(tweets)>0 else 0
        },
        { 
            "sentiment": "negative", 
            "count": len(ntweets), 
            "percentage": 100*len(ntweets) / len(tweets) if len(tweets)>0 else 0
        },
        { 
            "sentiment": "neutral", 
            "count": len(tweets) - len(ntweets) - len(ptweets), 
            "percentage": 100* (len(tweets) - len(ntweets) - len(ptweets)) / len(tweets) if len(tweets)>0 else 0
        }
    
    ]
    
    detail_positive = []
    for tweet in ptweets[:10]:
        detail_positive.append({
            "text": tweet["text"],
            "polarity":tweet["polarity"],
            "url":tweet["url"]
        })
    
    detail_negative = []
    for tweet in ntweets[:10]:
        detail_negative.append({
            "text": tweet["text"],
            "polarity":tweet["polarity"],
            "url":tweet["url"]
        })

    # add retweeted and favorited tweets to the list
    f_tweets = sorted(tweets, key=lambda kv: kv['favorites'], reverse=True)
    r_tweets = sorted(tweets, key=lambda kv: kv['retweets'], reverse=True)

    
    return render_template('result.html', title="Analysis Result", 
        summary=summary, detail_positive=detail_positive, 
        detail_negative=detail_negative, detail_retweeted=r_tweets[:10],
        detail_favorited=f_tweets[:10])
    


@app.route('/positive')
def positive():


    # parse the request arguments
    query =  request.args.get("query")
    count =  request.args.get("count") 
    
    # parse the count argument to make sure it's an integer (not a string)
    count = parse_int(count) if parse_int(count) else 200

    # get pagination page argument
    # page = request.args.get(get_page_parameter(), type=int, default=1)

    # check if we should enable search in pagination.  q is the arg for search query (i think)
    search = False
    q = request.args.get('q')
    if q:
        search=True

    # if we don't have any tweets stored for the session, get them now.
    api = TwitterClient()
    tweets = api.get_tweets(query=query, count=count)
    ptweets = sorted([tweet for tweet in tweets if tweet['sentiment'] == 'positive'],key= lambda kv: kv['polarity'], reverse=True)


    # render
    return render_template("positive.html",ptweets=ptweets)

# app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)))

