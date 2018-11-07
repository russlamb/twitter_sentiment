import os
from Twitterclient import TwitterClient
from flask import Flask, jsonify, request, render_template

app = Flask(__name__)


@app.route('/')
def main():
    """twitter sentiment analysisinput  page"""
    app.logger.info('User accessed the main.html template')
    return render_template('main.html', title="Sentiment Analysis")


@app.route('/result')    
def result():
    """
    result page to result analysis
    """
    
    app.logger.info('User accessed the result template')
    query =  request.args.get("query")
    count =  request.args.get("count") 
    # output_format=request.args.get("format")
    
    if not query:
        query = "BX"
        
    api = TwitterClient()

    # calling function to get tweets
    tweets = api.get_tweets(query=query, count=count)
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
            "polarity":tweet["polarity"]
        })
    
    detail_negative = []
    for tweet in ntweets[:10]:
        detail_negative.append({
            "text": tweet["text"],
            "polarity":tweet["polarity"]
        })
    return render_template('result.html', title="Analysis Result", 
        summary=summary, detail_positive=detail_positive, 
        detail_negative=detail_negative)
        
        


app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)))