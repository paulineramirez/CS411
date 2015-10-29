import json
from TwitterSearch import *

keyword1 = input('Enter a search value: ')
print(keyword1)


search_order = TwitterSearchOrder()
search_order.set_keywords([keyword1])
search_order.set_count(2)
search_order.set_include_entities(False)

ts = TwitterSearch(
	consumer_key = "BkczwDXiYQWAf2klUbnv2hEO0",
	consumer_secret = "JZibmuDUVcQ6utlG9kcoujtbJKHByoC2uM26muO9dpG1K49Hnm",
	access_token = "1051442228-Hrwir9aT8K8kFFg8zfiV9VfCW2QAEk47W5xZrRm",
	access_token_secret = "9dLGcZTYkLnazEBbghnhIwNIXM1fjZDCzQkn2kn4NUUTY"
	)

for happy_tweet in ts.search_tweets_iterable(search_order):
	print('@%s tweeted: %s' % ( happy_tweet['user']['screen_name'], happy_tweet['text']))

'''
tweetarray = []
counter = 0
for happy_tweet in ts.search_tweets_iterable(search_order):
        if counter < 10:
                tweetarray.append((happy_tweet['user']['screen_name'], happy_tweet['text']))
                counter += 1
        else:
                break
print(tweetarray)
'''

'''
consumer_key = "BkczwDXiYQWAf2klUbnv2hEO0"
consumer_secret = "JZibmuDUVcQ6utlG9kcoujtbJKHByoC2uM26muO9dpG1K49Hnm"
access_token = "1051442228-Hrwir9aT8K8kFFg8zfiV9VfCW2QAEk47W5xZrRm"
access_secret = "9dLGcZTYkLnazEBbghnhIwNIXM1fjZDCzQkn2kn4NUUTY"

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)

url = "https://api.twitter.com/1.1/search/tweets.json"


publictweets = api.home_timeline()

for t in publictweets:
	print(t)

'''
