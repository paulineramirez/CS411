from TwitterSearch import *
import json
def getTweets(keyword1):
  
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
    x = [] 
    counter = 0
    for happy_tweet in ts.search_tweets_iterable(search_order):
        if counter < 10:
             x += [('@%s tweeted: %s' % ( happy_tweet['user']['screen_name'], happy_tweet['text']))]
             
             counter += 1
        else:
            break
    return x



