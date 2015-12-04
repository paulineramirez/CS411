import web
import gettweets
from web import form
import json
import sql
import MySQLdb
import config
import math
# Pages

urls = (
    '/', 'Bar'
    ,'/search', 'Search'
    ,'/FAQ' ,'FAQ'
    ,'/about','About'
    ,'/startups','Startups'
    , '/applyforfunding', 'RequestFunding'
    , '/delete', 'Delete'
    )
app = web.application(urls, globals())

render = web.template.render('templates/', base = 'layout')
searchQuery = "hasnotchangedlolol"

# Apply for funding form
vemail = form.regexp(r".*@.*", "Must be a valid email address")

delete_form = form.Form(form.Button("submit", type="submit", description="Register your company", id="deletebtn"))
# the form itself 
funding_form = form.Form(
    form.Textbox("company_name", description="Enter your company name:", class_="form-group"),
    form.Textbox("money", description="How much money does your company need?"),
    form.Textbox("contact_name", description="Contact name:"),
    form.Textbox("contact_email", vemail, description="What is your email?"),
    form.Textbox("contact_phone", description="What is your phone number?"),
    form.Dropdown("type", \
        [(1, "early start up/seed"), \
         (2, "early stages"), \
         (3, "expansion"), \
         (4, "later stages") \
         ], description ="What is the stage of your startup"),
    #form.Checkbox("Academia"),
    #form.Checkbox("Art"),
    #form.Checkbox("Beauty"),
    #form.Checkbox("Business"),
    #form.Checkbox("Data"),
    #form.Checkbox("Education"),
    #form.Checkbox("Fitness"),
    #form.Checkbox("Food"),
    #form.Checkbox("Health"),
    #form.Checkbox("Gaming"),
    #form.Checkbox("IT"),
    #form.Checkbox("Marketing"),
    #form.Checkbox("Music"),
    #form.Checkbox("Sales"),
    #form.Checkbox("Shopping"),
    #form.Checkbox("Travel"),
    #form.Checkbox("Other"),
#    form.Dropdown("category", \
#            [(1, "Academia"),\
#            (2, "Art"),\
#            (3, "Beauty"),\
#            ("business", "Business"),\
#            ("data", "Data"),\
#            ("education", "Education"),\
#            ("fitness", "Fitness"),\
#            ("food", "Food"),\
#            ("health", "Health"),\
#            ("gaming", "Gaming"),\
#            ("IT", "IT"),\
#            ("marketing", "Marketing"),\
#            ("music", "Music"),\
#            ("sales", "Sales"),\
#            ("shopping", "Shopping"),\
#            ("travel", "Travel"),\
#            ("other", "Other")], description = "What industry is your startup in"),
    form.Textbox("website", description="Company website:"),
    form.Textbox("startup_twitter", description="Company twitter:"),
    form.Textarea("company_desc",size="40",maxlength="4000", description="What does your company do?",class_="form-group"),
    form.Button("submit", type="submit", description="Register your company")
    )

'''
class Tweets(object):
	def GET(self):
                return render.main() 
	def POST(self): 
		form = web.input()
		if form.keys()[0] == "tweets":
			if len(form.tweets) == 0:
				return "Enter a search > 0 characters"
			global searchQuery
			searchQuery = str(form.tweets)
			raise web.redirect('/search') '''
class Bar(object):
	def GET(self):
		return render.main() 
	def POST(self): 
		form = web.input()
		if form.keys()[0] == "bar":
			if len(form.bar) == 0:
				return "Error: Enter a search with something!"
			global searchQuery
			searchQuery = str(form.bar)
			urlquery = '/startups?query='+searchQuery
			raise web.redirect(urlquery)
                if form.keys()[0] == "tweets":
                    if len(form.tweets) == 0:
                        return "Error: Enter a query to search for"

                    searchQuery = str(form.tweets)
                    raise web.redirect('/search')

class Search:
    def GET(self):
        global searchQuery    

        ts = gettweets.getTweets(searchQuery)
        print(ts)
        return render.index(ts = ts)
       
class FAQ:
    def GET(self):
        return render.FAQ()

class About:
    def GET(self):
        return render.about()

class Startups:
	def GET(self):
		global searchQuery
		urlstuffs = web.input(filter="default")
		sortFilter = urlstuffs.filter
		if searchQuery == "hasnotchangedlolol":
			startupsTable = config.DB.select('startups').list()
			if sortFilter == "alphabetical":
				startupsTable = sorted(startupsTable, key=lambda startup_item: startup_item.startup_name)
			if len(startupsTable) > 9:
				totalnumpages = math.ceil((float(len(startupsTable)) / float(9)))
				return render.startups(startupsTable = startupsTable, numPages = int(totalnumpages), query = searchQuery, sort=sortFilter)
			else:
				return render.startups(startupsTable = startupsTable, numPages = 0, query = searchQuery, sort=sortFilter)
		else:
			StartupsTable = config.DB.select('startups').list()
			newStartupsTable = []
			passin = searchQuery
			for item in StartupsTable:
				if (searchQuery in str(item.startup_name).lower()) or (searchQuery in str(item.contact_name).lower()) or (searchQuery in str(item.startup_description).lower()):
					newStartupsTable.append(item)
			if sortFilter == "alphabetical":
				newStartupsTable = sorted(newStartupsTable, key=lambda startup_item: startup_item.startup_name)
			if len(newStartupsTable) > 9:
				searchQuery = "hasnotchangedlolol"
				totalnumpages = math.ceil((float(len(newStartupsTable)) / float(9)))
				return render.startups(startupsTable = newStartupsTable, numPages = int(totalnumpages), query = passin, sort=sortFilter)
			else:
				searchQuery = "hasnotchangedlolol"
				return render.startups(startupsTable = newStartupsTable, numPages = 0, query = passin, sort=sortFilter)

class RequestFunding:
    def GET(self):
        f = funding_form()
        return render.applyforfunding(f = f, dup = False)

    def POST(self):
        f = funding_form()
        print(f)
        if f.validates():
            sql.DBConnect(sql.users)
            sql.DBCreate('riskitbiscuit')
            sql.DBCreateTable() 
            
            x = config.DB.select('startups', where="startup_name = "+"'"+f.d.company_name+"'")
#            except MySQLdb.Error, e:
#                print("MYSql Error: ",e)
#                pass
#            else:
            if len(x) != 0:
                return render.applyforfunding(f = f, dup = True);
            config.DB.insert('startups', startup_url=f.d.website, startup_twitter=f.d.startup_twitter,startup_money=f.d.money, startup_name=f.d.company_name,contact_name=f.d.contact_name,contact_email=f.d.contact_email,contact_phone=f.d.contact_phone,startup_stage=f.d.type,startup_description=f.d.company_desc,startup_category="something")
            table =  config.DB.select('startups')  
      
            print(x)
            sql.DBclose() 
            #return f.d.type
            return render.redirect() 

        else:
            return "Did not validate"
class Delete:
    def GET(self):
        d = delete_form
        return render.delete(d=d)

    def POST(self):
        if d.validates:
            sql.DBConnect(sql.users)
            config.DB.query("truncate startups;")
            sql.DBclose()

            return render.redirect(msg = "Emptied db")
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
