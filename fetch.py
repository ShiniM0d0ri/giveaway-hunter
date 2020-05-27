import tweepy
import re
import hidden #twitter keys
import string
import random

# Twitter credentials for the app
consumer_key = hidden.key[0]
consumer_secret = hidden.key[1]
access_key = hidden.key[2]
access_secret = hidden.key[3]

# pass twitter credentials to tweepy
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)


def listToString(s):  
    
    # initialize an empty string 
    str1 = " " 
    
    # return string   
    return (str1.join(s)) 


def get_tweets(queries,tweets_per_query):
    new_tweets = 0
    listfrens=["@Vipinuniyal15","@vipinuniyal11","@NaiWakan","@Vjaykumar10"]
    for query in queries:
        print ("Starting new query: " + query)
        for tweet in tweepy.Cursor(api.search, q=query, tweet_mode="extended").items(tweets_per_query ):
            user = tweet.user.screen_name
            id = tweet.id
            url = 'https://twitter.com/' + user +  '/status/' + str(id)
            print (url)
            try:
                text = tweet.retweeted_status.full_text.lower()
            except:
                text = tweet.full_text.lower()

            # Check if tweet is a retweet
            if text.startswith("retweeted"):
                print('Tweet appears to be a retweet [RETWEET]')
                continue
            
            # Check if tweet is a retweet
            if text.startswith("rt @"):
                print('Tweet appears to be a retweet [RETWEET]')
                continue
            # Check if tweet is a reply
            if text.startswith("@"):
                print('Tweet appears to be a reply [REPLY]')
                continue
            # Check if tweet is a reply
            if tweet.is_quote_status == True:
                print('Tweet appears to be a quote [QUOTE]')
                continue

            #for Retweets
            #if not retweeted RT and tag frends
            if "retweet" in text or "rt" in text:
                if not tweet.retweeted:
                    try:
                        tweet.retweet()
                        print("\tRetweeted")
                        new_tweets += 1
                    except tweepy.TweepError as e:
                        print('\tAlready Retweeted')
            
            #for like
            if "like" in text:
                if not tweet.favorited:
            # Mark it as Liked, since we have not done it yet
                    try:
                        tweet.favorite()
                        print('\tTweet liked')
                    except tweepy.TweepError as e:
                        print('\tAlready liked')
            
            #for tag..
            if "tag" in text:
                n=0
                pattern='tag\s\w'
                result = re.search(pattern, text).group()
                print(result)
                if result[4]=="a":
                    n=1
                elif result[4]=="y":
                    n=2
                else:
                    n=int(result[4])
                frens=random.sample(listfrens,n)
                frens_string=listToString(frens)
                api.update_status("@" + user + " " + frens_string, in_reply_to_status_id = str(id),auto_populate_reply_metadata=True)
                print("\tTagged "+str(n)+" frens",frens)            
            
            #for follow
            if "follow" in text:
                try:
                    to_follow = [tweet.retweeted_status.user.screen_name] + [i['screen_name'] for i in tweet.entities['user_mentions']]
                    # Don't follow origin user (person who retweeted)
                except:
                    to_follow = [user] + [i['screen_name'] for i in tweet.entities['user_mentions']]

                for screen_name in list(set(to_follow)):
                    api.create_friendship(screen_name)
                    print('\t' + "Followed: " + screen_name)
            #if "subscribe" in text:


    print ("New Tweets: " + str(new_tweets))






    
#main
queries = ["huntsman giveaway"]
tweets_per_query  = 50
get_tweets(queries,tweets_per_query)