import tweepy
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import API
from tweepy import Cursor
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from textblob import TextBlob
import re

access_token = "1135482028185407488-xpgmOpyKZ5Q5L8E1V0gOqAI1J0gHYh"
access_token_secret = "HooWx6eQO5O8RHndD8gbR8srykE1bOmCYyegDKrL2PnNi"
consumer_key = "FAtAcDRvXko6m0YJ7eGJOiqon"
consumer_secret = "kPMwCoXuLcK08WW1Faiplce6TBou2FMWhhNW58OP4DX4qRSpom"


##twitter client
class TwitterClient():
    def __init__(self,twitter_user=None):
        self.auth=TwitterAuthenticator().authenticate_twitter_app()
        self.twitter_client=API(self.auth)     ##,parser=tweepy.parsers.JSONParser()
        self.twitter_user=twitter_user

    def get_twitter_client_api(self):
        return self.twitter_client

    def get_user_timeline_tweets(self,num_tweets):
        tweets=[]
        ##user_timeline=user_timeline
        for tweet in Cursor(self.twitter_client.user_timeline,id=self.twitter_user).items(num_tweets):
            tweets.append(tweet)
        return tweets

    def get_friend_list(self,num_friends):
        friend_list=[]
        for friend in Cursor(self.twitter_client.friends,id=self.twitter_user).items(num_friends):
            friend_list.append(friend)
        return friend_list

    def get_home_timeline_tweets(self,num_tweets):
        home_timeline_tweets=[]
        for tweet in Cursor(self.twitter_client.home_timeline,id=self.twitter_user).items(num_tweets):
            home_timeline_tweets.append(tweet)
        return home_timeline_tweets



class TwitterAuthenticator():
    def authenticate_twitter_app(self):
        auth=OAuthHandler(consumer_key,consumer_secret)
        auth.set_access_token(access_token,access_token_secret)
        return auth

class Twitter_Streamer():
    def __init__(self):
        self.twitter_authenticator=TwitterAuthenticator()
    #Class for streaming and processing live tweets
    def stream_tweets(self,fetched_tweets_filename,hash_tag_list):
        #this handles twitter authentication and the connection to the twiter streaming api
        listener=TwitterListener(fetched_tweets_filename)
        auth=self.twitter_authenticator.authenticate_twitter_app()
        stream=Stream(auth,listener,ctweet_mode='extended')
        stream.filter(track=hash_tag_list)

class TwitterListener(StreamListener):
    #this is a basic listener class that just prints received tweets to stdout
    def __init__(self,fetched_tweets_filename):
        self.fetched_tweets_filename=fetched_tweets_filename

    def on_data(self,data):
        try:
            print(data)
            with open(self.fetched_tweets_filename,'a') as tf:
                tf.write(data)
            return True
        except BaseException as e:
            print('error on data:%s' % str(e))
        return True

    def on_error(self,status):
        if status==420:
            ##returning false on data method in case rate limit occurs
            return False
        print(status)

## functionality for analysing and categorising content from tweets
class TweetAnalyser():
    ##def clean_tweet(self, tweet):
        ##return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet.split())
        

    def analyze_sentiment(self, tweet):
        analysis = TextBlob(tweet)
        
        if analysis.sentiment.polarity > 0:
            return 1
        elif analysis.sentiment.polarity == 0:
            return 0
        else:
            return -1

        
    
    def tweets_to_data_frame(self, tweets):
       
        df = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['Tweets'])
        
        df['id']=np.array([tweet.id for tweet in tweets])
        df['len'] = np.array([len(tweet.text) for tweet in tweets])
        df['date'] = np.array([tweet.created_at for tweet in tweets])
        df['source'] = np.array([tweet.source for tweet in tweets])
        df['likes'] = np.array([tweet.favorite_count for tweet in tweets])
        df['retweets'] = np.array([tweet.retweet_count for tweet in tweets])
        df['sentiment'] = np.array([self.analyze_sentiment(tweet.text) for tweet in tweets])
        ##df['sentiment']= list(map(lambda tweet: analyze_sentiment(tweet), tweets))

        return df
   