import tweepy
import re
import hidden #twitter keys
import string
import random
import datetime

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
    #load friends
    listfrens=get_frens()
    #eth address
    eth_address="0xdb7d6c8d88ae3019da3fbede995d62323fc66881"
    for query in queries:
        print ("Starting new query: " + query)
        for tweet in tweepy.Cursor(api.search, q=query+" giveaway -filter:retweets", tweet_mode="extended").items(tweets_per_query ):
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
                print('\tTweet appears to be a retweet [RETWEET]')
                continue
            
            # Check if tweet is a retweet
            if text.startswith("rt @"):
                print('\tTweet appears to be a retweet [RETWEET]')
                continue
            # Check if tweet is a reply
            if text.startswith("@"):
                print('\tTweet appears to be a reply [REPLY]')
                continue
            # Check if tweet is a reply
            if tweet.is_quote_status == True:
                print('\tTweet appears to be a quote [QUOTE]')
                continue
            # Check if tweet is a external link
            if "with the link" in text or "gleam" in text or "come and join the" in text or "@SzymekJa" in text:
                print('\tSkipping external link giveaway')
                continue
            # Check for fakes
            if "@rambo_tuga" in text or "@csgoskinslucky" in text or "@ensigskins" in text or "@rihardinjss" in text or "@csgodarknet" in text or "@go_giveaway" in text or "@csgogamblecode1" in text:
                print('\tSkipping fake giveaway')
                continue
            
            #check if it ended already
            """time_passed=None
            time_left=0
            if "ends in" in text:
                pattern='(ends in)\s\d+\s\w+'
                result = re.search(pattern, text).group()
                time_left=int(re.search('\d+', result[8:]).group())
                unit= re.search('[a-z]+', result[8:]).group()

            if "rolling in" in text:
                pattern='(rolling in)\s\d+\s\w+'
                result = re.search(pattern, text).group()
                time_left=int(re.search('\d+', result[11:]).group())
                unit= re.search('[a-z]+', result[11:]).group()
            
            time_passed=tweet.created_at+ datetime.timedelta(hours=time_left)
            
            print(time_passed)
            """
            #for Retweets
            #if not retweeted RT and tag frends
            if "retweet" in text or "rt" in text:
                if not tweet.retweeted:
                    try:
                        tweet.retweet()
                        print("\tRetweeted")
                        new_tweets += 1

                        if "eth address" in text:
                            api.update_status(eth_address, in_reply_to_status_id = str(id),auto_populate_reply_metadata=True)
                            print("\tETH address replied")
                        #for tag..
                        if "tag" in text:
                            try:
                                n=0
                                pattern='tag\s\w'
                                result = re.search(pattern, text).group()
                                print(result)
                                if result[4]=="a":
                                    n=1
                                elif result[4]=="y" or result[4]=="f":
                                    n=2
                                else:
                                    n=int(result[4])
                                frens=random.sample(listfrens,n)
                                frens_string=listToString(frens)
                                api.update_status(frens_string, in_reply_to_status_id = str(id),auto_populate_reply_metadata=True)
                                print("\tTagged "+str(n)+" frens",frens)
                            except:
                                print('\tunable to tag freinds, try tagging manually')
                    except tweepy.TweepError as e:
                        print('\tAlready Retweeted')
                        continue
            
            #for like
            if "like" in text:
                if not tweet.favorited:
            # Mark it as Liked, since we have not done it yet
                    try:
                        tweet.favorite()
                        print('\tTweet liked')
                    except tweepy.TweepError as e:
                        print('\tAlready liked')
            
            
            
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


#fetch friends from a separate file named frens.txt
def get_frens():
    with open('frens.txt') as f:
        cities = f.readlines()
        cities = [x.strip() for x in cities]
    return cities



    
#main
keyword=input("which giveaway u want to search for\n")
queries = [keyword] #list to store queries
tweets_per_query  = int(input("no. of tweets to search for\n"))
get_tweets(queries,tweets_per_query)