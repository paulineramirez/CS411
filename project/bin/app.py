import web
import gettweets
from web import form
import json
import mysql

# Pages

urls = (
    '/', 'Tweets'
    ,'/search', 'Search'
    ,'/FAQ' ,'FAQ'
    ,'/about','About'
    ,'/startups','Startups'
    , '/applyforfunding', 'RequestFunding'
    )
app = web.application(urls, globals())

render = web.template.render('templates/', base = 'layout')
searchQuery = "hasnotchanged"

#David's Code
#DB = web.database(dbn='mysql', user='mysql_user', pw='mysql_password', db='riskitbiscuit')


# Apply for funding form
vemail = form.regexp(r".*@.*", "Must be a valid email address")

# the form itself 
funding_form = form.Form(
    form.Textbox("company_name", description="Enter your company name:"),
    form.Textbox("company-desc", description="What does your company do?"),
    form.Textbox("money", description="How much money does your company need?"),
    form.Textbox("contact_name", description="Contact name:"),
    form.Textbox("contact_email", vemail, description="What is your email?"),
    form.Textbox("contact_phone", description="What is your phone number?"),
    form.Dropdown("type", \
        [('type1', "early start up/seed"), \
         ('type2', "early stages"), \
         ('type3', "expansion"), \
         ('type4', "later stages") \
         ]),
    form.Textbox("website", description="Company website:"),
    form.Textbox("startup_twitter", description="Company twitter:"),
    form.Button("submit", type="submit", description="Register your company")
    )

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
        return form


class Search:
    def GET(self):
        global searchQuery    

        ts = gettweets.getTweets(searchQuery)
        return render.index(ts = ts)
       
class FAQ:
    def GET(self):
        return render.FAQ()

class About:
    def GET(self):
        return render.about()

class Startups:
    def GET(self):
        #David's Code
        #startupsTable = DB.select('startups') #startupsDB is, from the DB object (which is selecting, from the database it's connected to, the table 'startups'), the actual 'startups' table being passed in as an argument to rendering, 
        #return render.startups(startupsTable) #that here, allows the table to be called using python code from the startups HTML template
        return render.startups()

class RequestFunding:
    def GET(self):
        f = funding_form()
        return render.applyforfunding(f = f)

    def POST(self):
        f = funding_form()
        if f.validates():
            return f


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
