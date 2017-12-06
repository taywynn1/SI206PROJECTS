import unittest
import itertools
import collections
import tweepy
import twitter_info # same deal as always...
import json
import sqlite3
import pprint

##### TWEEPY SETUP CODE:
# Authentication information should be in a twitter_info file...
consumer_key = twitter_info.consumer_key
consumer_secret = twitter_info.consumer_secret
access_token = twitter_info.access_token
access_token_secret = twitter_info.access_token_secret
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Set up library to grab stuff from twitter with your authentication, and 
# return it in a JSON format 
api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

#CACHING!
try: 
    f = open('twitter_data.txt', 'r')
    cache_contents = json.loads(f.read()) #opening the file to collect datafrom cached data instead of live data
    f.close()
except: 
	results = api.user_timeline(screen_name = 'allido_is_WYNN', count = 103) #for some reason to get 100 I needed a count of 103
	#pprint.pprint(results)
	#print(len(results)) #checking to make sure I have 100 results
	f = open('twitter_data.txt', 'w')
	f.write(json.dumps(results, indent = 2))
	f.close()