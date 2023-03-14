## Standard Imports
import pandas as pd
from datetime import datetime
import tweepy as tweepy
import json
import time

while True:
    try:
        # import twitter api
        with open('/Users/Zach/Documents/.secret/twitter_api.json') as f:
            login = json.load(f)
            
        auth = tweepy.OAuthHandler(login['consumer_key'], login['consumer_secret'])
        auth.set_access_token(login['access_token'], login['access_secret'])
        
        twitter_api = tweepy.API(auth)

        # Query built by the health team

        cold_flu_query = 'cold OR flu OR cough OR (runny nose) OR (stuffy nose) OR (sore throat) OR (muscle aches) OR headaches OR (body aches) OR (itchy throat) -police -POLICE -filter:retweets'
        pneu_bronc_query = 'pneumonia OR bronchitis OR sweating OR chills OR (shortness of breath) OR (difficulty breathing) OR (out of breath) OR (coughing blood) -police -POLICE -filter:retweets'
        location = "39.8,-95.583068847656,2500km"  # Geographical center of the US with 2500km radius
        language = "en"
        result_type = "recent"

        # two queries, for low risk and one for high risk infections

        cold_flu_tweets = tweepy.Cursor(twitter_api.search_tweets, 
                                                    q=cold_flu_query, 
                                                    geocode=location,
                                                    since_id='2022-01-01',
                                                    lang=language).items(1000)

        pneu_bronc_tweets = tweepy.Cursor(twitter_api.search_tweets, 
                                                    q=pneu_bronc_query, 
                                                    geocode=location,
                                                    since_id='2022-01-01',
                                                    lang=language).items(1000)

        # filter tweets and import into data frame

        cf_file = pd.read_csv('cold_flu.csv')
        pb_file = pd.read_csv('pneu_bronc.csv')

        filtered_cold_flu_tweets = []

        for tweet in cold_flu_tweets:
            if cf_file['tweet_id'].isin([tweet.id]).any():
                continue
            if tweet.place is not None:
                filtered_cold_flu_tweets.append({
                    'tweet_id': tweet.id,
                    'text': tweet.text,
                    'location': tweet.place.full_name,
                    'date': tweet.created_at.date()
                })

        filtered_pneu_bronc_tweets = []

        for tweet in pneu_bronc_tweets:
            if pb_file['tweet_id'].isin([tweet.id]).any():
                continue
            if tweet.place is not None:
                filtered_pneu_bronc_tweets.append({
                    'tweet_id': tweet.id,
                    'text': tweet.text,
                    'location': tweet.place.full_name,
                    'date': tweet.created_at.date()
                })

        # figuring out how to not have duplicates in the file
        # i'm reading in the file, inserting the 'new' tweets into the the file, then dropping the duplicates, then writing the file again
        # it doesn't sound optimal, i should be verifying the tweet is new from the for loops up top but i feel like it requires to use a for loop in a for loop which doesn't sound good

        low_risk_tweets = pd.DataFrame(filtered_cold_flu_tweets)
        high_risk_tweets = pd.DataFrame(filtered_pneu_bronc_tweets)

        new_cf_file = pd.concat([cf_file, low_risk_tweets], ignore_index=True)
        new_pb_file = pd.concat([pb_file, high_risk_tweets], ignore_index=True)

        new_cf_file.drop_duplicates(inplace=True)
        new_pb_file.drop_duplicates(inplace=True)


        # put data frame into a csv

        new_cf_file.to_csv('cold_flu.csv', index=False)
        new_pb_file.to_csv('pneu_bronc.csv', index=False)

        print("Successfully Added Tweets to CSV Files!")
        print("I will now sleep for 15 minutes!")

        time.sleep(900)
    except tweepy.TooManyRequests as e:
        print("Error: ", e.response)
        time.sleep(900)