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
tagList = []

# Apply for funding form
vemail = form.regexp(r".*@.*", "Must be a valid email address")

delete_form = form.Form(form.Button("Delete All Startups?", type="submit", description="Delete all startups from local database"))
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
    form.Checkbox("Academia"),
    form.Checkbox("Art"),
    form.Checkbox("Beauty"),
    form.Checkbox("Business"),
    form.Checkbox("Data"),
    form.Checkbox("Education"),
    form.Checkbox("Fitness"),
    form.Checkbox("Food"),
    form.Checkbox("Health"),
    form.Checkbox("Gaming"),
    form.Checkbox("IT"),
    form.Checkbox("Marketing"),
    form.Checkbox("Music"),
    form.Checkbox("Sales"),
    form.Checkbox("Shopping"),
    form.Checkbox("Travel"),
    form.Checkbox("Other"),
    form.Textbox("website", description="Company website:"),
    form.Textbox("startup_twitter", description="Company twitter:"),
    form.Textarea("company_desc",size="60",maxlength="4000", description="What does your company do?",class_="form-group"),
    form.Button("submit", type="submit", description="Register your company")
    )

class Bar(object):
	def GET(self):
		return render.main() 
	def POST(self): 
		form = web.input()
		if form.keys()[0] == "bar":
                    if len(form.bar) == 0:
			return "Error: Enter a search with something!"
                    global searchQuery
		    searchQuery = str(form.bar).strip()
		    sQList = searchQuery.split(" ")
                    urlquery = '/startups?query='
                    for word in sQList:
                        urlquery = urlquery + word + "_"
                    urlquery = urlquery[:-1]
                    raise web.redirect(urlquery)
                if form.keys()[0] == "tweets":
                    if len(form.tweets) == 0:
                        return "Error: Enter a query to search for"
                    searchQuery = str(form.tweets).strip()
                    raise web.redirect('/search')

class Search:
    def GET(self):
        global searchQuery    
        ts = gettweets.getTweets(searchQuery)
        searchQuery = "hasnotchangedlolol"
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
		global tagList
		urlstuffs = web.input(sort="default", query="default", tags="default")
		sortFilter = urlstuffs.sort
		if urlstuffs.query != "default" or urlstuffs.tags != "default":
                        del tagList[:]
                        q = urlstuffs.query
                        t = urlstuffs.tags
                        ql = q.split("_")
                        tl = t.split("_")
                        ql2 = []
                        tl2 = []
                        for word in ql:
                                if word != unicode("", "utf-8"):
                                        ql2.append(word)
                        for tag in tl:
                                if tag != unicode("", "utf-8"):
                                        tl2.append(tag)
                        if len(ql2) == 0:
                                searchQuery = ""
                        else:
                                searchQuery = ""
                                for index in range(len(ql2)):
                                        ql2[index] = str(ql2[index])
                                for word in ql2:
                                        searchQuery = searchQuery + word + " "
                                searchQuery = searchQuery[:-1]
                        if len(tl2) != 0:
                                for tag in tl2:
                                        tagList.append(tag)
		if searchQuery == "hasnotchangedlolol":
			startupsTable = config.DB.select('startups').list()
			if len(tagList) != 0:
                                holder = []
                                for item in startupsTable:
                                        itemTags = (item.startup_category).split(",")
                                        itemTags[0] = itemTags[0][6:]
                                        itemTags.pop()
                                        for index in range(1, len(itemTags)):
                                                itemTags[index] = itemTags[index][1:]
                                        for tag in tagList:
                                             if (tag in itemTags) and (item not in holder):
                                                     holder.append(item)
                                del startupsTable[:]
                                for item in holder:
                                        startupsTable.append(item)
			if sortFilter == "alphabetical":
				startupsTable = sorted(startupsTable, key=lambda startup_item: startup_item.startup_name)
			if sortFilter == "startup_stage":
				startupsTable = sorted(startupsTable, key=lambda startup_item: startup_item.startup_stage)
			if len(startupsTable) > 9:
				totalnumpages = math.ceil((float(len(startupsTable)) / float(9)))
				return render.startups(startupsTable = startupsTable, numPages = int(totalnumpages), query = searchQuery, sort=sortFilter, tagL = tagList, url = urlstuffs)
			else:
				return render.startups(startupsTable = startupsTable, numPages = 0, query = searchQuery, sort=sortFilter, tagL = tagList, url = urlstuffs)
		else:
			StartupsTable = config.DB.select('startups').list()
			newStartupsTable = []
			passin = searchQuery
			passinTags = []
			sQList = searchQuery.split(" ")
			for tag in tagList:
                                if tag != unicode("default"):
                                        passinTags.append(tag)
                        del tagList[:]
			if searchQuery == "":
                                for item in StartupsTable:
                                        newStartupsTable.append(item)
                                passin = "hasnotchangedlolol"
                        else:
                                for item in StartupsTable:
                                        for word in sQList:
                                                wordlower = word.lower()
                                                if (item not in newStartupsTable) and ((wordlower in str(item.startup_name).lower()) or (wordlower in str(item.contact_name).lower()) or (wordlower in str(item.startup_description).lower())):
                                                        newStartupsTable.append(item)
                        if len(passinTags) != 0:
                                holder = []
                                for item in newStartupsTable:
                                        itemTags = (item.startup_category).split(",")
                                        itemTags[0] = itemTags[0][6:]
                                        itemTags.pop()
                                        for index in range(1, len(itemTags)):
                                                itemTags[index] = itemTags[index][1:]
                                        for tag in passinTags:
                                             if (tag in itemTags) and (item not in holder):
                                                     holder.append(item)
                                del newStartupsTable[:]
                                for item in holder:
                                        newStartupsTable.append(item)
			if sortFilter == "alphabetical":
				newStartupsTable = sorted(newStartupsTable, key=lambda startup_item: startup_item.startup_name)
			if sortFilter == "startup_stage":
				newStartupsTable = sorted(newStartupsTable, key=lambda startup_item: startup_item.startup_stage)
			if len(newStartupsTable) > 9:
				searchQuery = "hasnotchangedlolol"
				totalnumpages = math.ceil((float(len(newStartupsTable)) / float(9)))
				return render.startups(startupsTable = newStartupsTable, numPages = int(totalnumpages), query = passin, sort=sortFilter, tagL = passinTags, url = urlstuffs)
			else:
				searchQuery = "hasnotchangedlolol"
				return render.startups(startupsTable = newStartupsTable, numPages = 0, query = passin, sort=sortFilter, tagL = passinTags, url = urlstuffs)
	def POST(self):
                global searchQuery
                form = web.input(SAF = [])
                filters = form.SAF
                searchQuery = str(filters[0]).strip()
                filters.pop(0)
                global tagList
                
                if searchQuery == "" and len(filters) == 0:
                        return "Need to search for something with a filter!"
                elif searchQuery == "" and len(filters) != 0:
                        urlquery = '/startups?query=_&tags='
                        for tag in filters:
                                tagList.append(tag)
                                urlquery = urlquery + str(tag) + '_'
                        urlquery = urlquery[:-1]
                else:
                        sQList = searchQuery.split(" ")
                        urlquery = '/startups?query='
                        for word in sQList:
                            urlquery += (word + "_")
                        urlquery = urlquery[:-1]
                        urlquery = urlquery + "&tags="
                        for tag in filters:
                                tagList.append(tag)
                                urlquery = urlquery + str(tag) + "_"
                        urlquery = urlquery[:-1]
                raise web.redirect(urlquery)

class RequestFunding:
    def GET(self):
        f = funding_form()
        print("RENDERING FORM")
        return render.applyforfunding(f = f, dup = False)

    def POST(self):
        f = funding_form()
        if f.validates():
            sql.DBConnect(sql.users)
            sql.DBCreate('riskitbiscuit')
            sql.DBCreateTable()             
            x = config.DB.select('startups', where="startup_name = "+"'"+f.d.company_name+"'")
            print(x.list(),"current selected entry in db")
            categories = "Tags: "
            formdata = web.input()
            print(formdata)
            tags = ['Art', 'Beauty', 'Business', 'Data', 'Education','Fitness','Food','Health','Gaming', 'IT', 'Marketing', 'Music', 'Sales', 'Shopping', 'Travel', 'Other']
            for y in tags:
                if formdata.has_key(y):
                    categories = categories + y + ", "
                    print(categories)
            categories = categories[:-1]
            if len(x) != 0:
                return render.applyforfunding(f = f, dup = True);
            config.DB.insert('startups', startup_url=f.d.website, startup_twitter=f.d.startup_twitter,startup_money=f.d.money, startup_name=f.d.company_name,contact_name=f.d.contact_name,contact_email=f.d.contact_email,contact_phone=f.d.contact_phone,startup_stage=f.d.type,startup_description=f.d.company_desc,startup_category=categories)
            table =  config.DB.select('startups')  
            print(x)
            sql.DBclose()
            return render.redirect(msg = False)

class Delete:
    def GET(self):
        d = delete_form
        return render.delete(d=d)

    def POST(self):
        d = delete_form
        if d.validates:
            sql.DBConnect(sql.users)
            config.DB.query("truncate startups;")
            sql.DBclose()
            return render.redirect(msg = True)

if __name__ == "__main__":
    app.run()




'''
JUNK CODE
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
