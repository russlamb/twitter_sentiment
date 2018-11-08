# Twitter Sentiment Analysis

Simple flask app accepts a user input and returns an analysis of the results.

Sentiment is based on TextBlob library.  

The analysis provides the number of positive, negative, and neutral tweets obtained from the search query.  It also includes the top 10 most positive and most negative tweets from the analysis, along with links to the twitter status.  

inspired by this post https://www.geeksforgeeks.org/twitter-sentiment-analysis-using-python/

## Files

main.py is a command line harness around the TwitterClient class used for testing the API works.  

app.py is the Flask app.  

## Configuration
The app expects environment variables with the Twitter API authentication keys (consumer_key, consumer_secret, auth_token, auth_token_secret).

# Current deployment
This code is currently deployed here.  You can submit your own queries to view the results.
https://twitter-sentiment-rl.herokuapp.com/

