from flask import Flask,render_template,url_for,request,session
from textblob import TextBlob
from flask_bootstrap import Bootstrap
from tweepy import API 
from tweepy import Cursor
import matplotlib.pyplot as plt
import re
from tweepy import OAuthHandler
from tweepy import Stream
import numpy as np
import pandas as pd
from sentiment import TwitterListener
from sentiment import Twitter_Streamer
from sentiment import TwitterClient
from sentiment import TweetAnalyser
import pickle
import random
from itertools import zip_longest
import plotly



access_token = "1135482028185407488-xpgmOpyKZ5Q5L8E1V0gOqAI1J0gHYh"
access_token_secret = "HooWx6eQO5O8RHndD8gbR8srykE1bOmCYyegDKrL2PnNi"
consumer_key = "FAtAcDRvXko6m0YJ7eGJOiqon"
consumer_secret = "kPMwCoXuLcK08WW1Faiplce6TBou2FMWhhNW58OP4DX4qRSpom"

app=Flask(__name__)
app.secret_key="great"
Bootstrap(app)
tw=[]
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyse',methods=['GET','POST'])
def analyse():
   
    if request.method=='POST' and request.form["action"]=="Submit":
        rawtext=request.form['text1']
        #print(rawtext)
        #print(type(rawtext))
       
        twitter_client=TwitterClient()
        tweet_analyser=TweetAnalyser()
        api=twitter_client.get_twitter_client_api()
        tweets=api.user_timeline(screen_name=rawtext,count=10)
        df = tweet_analyser.tweets_to_data_frame(tweets)
       
       # print(dir(tweets[0]))
        #print(np.mean(df['len']))
        #print(np.max(df['likes']))
        #print(np.max(df['retweets']))
        pd.options.display.max_colwidth=200
        
      
        
        positive=0
        negative=0
        neutral=0
        ##session['tweetdata']=tweets
        pos=[]
        
        for x in tweets:
            analysis=TextBlob(x.text)
            profile_pic=x.user.profile_image_url
           # profile_banner=x.user.profile_banner
            if analysis.sentiment.polarity > 0:
                positive+=1
                pos.append(x.text)
                
            elif analysis.sentiment.polarity == 0: 
                neutral+=1
            else: 
                negative+=1

        
        filename="testfile"
        fileobject=open(filename,'wb')
        pickle.dump(tweets,fileobject)
        fileobject.close()
        filename="input_word"
        fileobject1=open(filename,'wb')
        pickle.dump(rawtext,fileobject1)
        fileobject1.close()

        url="https://twitter.com/"
        query='+'.join(rawtext.split())
        search_url=url+query
        print(search_url)

        return render_template('index.html',tables=[df.to_html(classes='data')], titles=df.columns.values,positive=positive,neutral=neutral,negative=negative,search_url=search_url,profile_pic=profile_pic)

    

@app.route('/positive',methods=['GET','POST'])
def positive():
   
    ##twe=session.get['posi']
    
    file=open('testfile','rb')
    b=pickle.load(file)
    file.close()
    pos=[]
    re_p=[]
    li_p=[]
    id_p=[]
    
    for x in b:
            analysis=TextBlob(x.text)
            
            if analysis.sentiment.polarity > 0:
                
                pos.append(x.text)
                re_p.append(x.retweet_count)
                li_p.append(x.favorite_count)
                id_p.append(x.id)
    
        
    file1=open('input_word','rb')
    t=pickle.load(file1)
    file1.close()

    url="https://twitter.com/"
    query='+'.join(t.split())
    search_url=url+query
    content=zip_longest(pos,re_p,li_p,id_p)

    return render_template('positive.html',content=content,search_url=search_url,id_p=id_p) 

@app.route('/negative',methods=['GET','POST'])    
def negative():
    file=open('testfile','rb')
    c=pickle.load(file)
    file.close()
    re_n=[]
    li_n=[]
    neg=[]
    id_n=[]
    for x in c:
        analysis=TextBlob(x.text)
        if analysis.sentiment.polarity < 0:
            neg.append(x.text)
            li_n.append(x.favorite_count)
            re_n.append(x.retweet_count)
            id_n.append(x.id)

    file1=open('input_word','rb')
    u=pickle.load(file1)
    file1.close()

    url="https://twitter.com/"
    query='+'.join(u.split())
    search_url=url+query

    neg_content=zip_longest(neg,li_n,re_n,id_n)
    return render_template('negative.html',neg_content=neg_content,search_url=search_url)

@app.route('/neutral',methods=['GET','POST'])    
def neutral():
    file=open('testfile','rb')
    d=pickle.load(file)
    file.close()
    re_neu=[]
    li_neu=[]
    neu=[]
    id_neu=[]
    for x in d:
        analysis=TextBlob(x.text)
        if analysis.sentiment.polarity == 0:
            neu.append(x.text)
            li_neu.append(x.favorite_count)
            re_neu.append(x.retweet_count)
            id_neu.append(x.id)

    file1=open('input_word','rb')
    u=pickle.load(file1)
    file1.close()

    url="https://twitter.com/"
    query='+'.join(u.split())
    search_url=url+query
    neu_content=zip_longest(neu,li_neu,re_neu,id_neu)
    return render_template('neutral.html',neu_content=neu_content,search_url=search_url)


if __name__ == "__main__":
    app.run(debug=False)