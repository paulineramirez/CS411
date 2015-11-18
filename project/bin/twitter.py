import web
import gettweets

urls = (
    '/', 'Tweets'
    ,'/search', 'Search'
    ,'/FAQ' ,'FAQ'
    ,'/about','About'
    ,'/startups','Startups'
    , '/applyforfunding', 'RequestFunding'
    )
app = web.application(urls, globals())

render = web.template.render('templates/')
searchQuery = "hasnotchanged"

class Tweets(object):
    def GET(self):
        return render.main() 


    def POST(self): 
        form = web.input()
        if form.keys()[0] == "FAQ":
                raise web.redirect('/FAQ')
        if form.keys()[0] == "tweets":
            if len(form.tweets) == 0:
                return "Enter a search > 0 characters"
            global searchQuery
            searchQuery = str(form.tweets)
            raise web.redirect('/search') 
        if form.keys()[0] == "startups":
            raise web.redirect('/startups')
        if form.keys()[0] == "home":
            raise web.redirect('/')
        if form.keys()[0] == "about":
            raise web.redirect('/about')
        if form.keys()[0] == "signup":
            raise web.redirect('/signup')
        if form.keys()[0] == "funding":
            raise web.redirect('/applyforfunding')

class Search:
    def GET(self):
        global searchQuery    

        ts = gettweets.getTweets(searchQuery)
        ts = ts
        return render.index(ts = ts)
       
class FAQ:
    def GET(self):
        return render.FAQ()

class About:
    def GET(self):
        return render.about()

class Startups:
    def GET(self):
        return render.startups()

class RequestFunding:
    def GET(self):
        return render.applyforfunding()

if __name__ == "__main__":
    app.run()




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
