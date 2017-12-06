import json
import requests
import pprint
from facebook_info import access_token
import sqlite3
import datetime
import matplotlib.pyplot as plt
import numpy as np


baseurl = "https://graph.facebook.com/v2.3/me/feed" # Baseurl expecting you to format in either "me" or a group ID

## Building the Facebook parameters dictionary
url_params = {}
url_params["access_token"] = access_token
url_params["fields"] = "message,story,comments,likes,created_time,from" # This is the Facebook API's way of getting posts: comments, and each comment's likes/poster/message/time created, the post's likes, the post's message (if there is one), the person who posted the post, and the post's created time
url_params["limit"] = 25 #default limit


#CACHING!
try: 
    f = open('facebook_data.txt', 'r')
    cache_contents = json.loads(f.read()) #opening the file to collect datafrom cached data instead of live data
    f.close()
except: 
	r = requests.get(baseurl,params=url_params)

	feed = json.loads(r.text) #returns a dictionary and in order to support paging we want to add it to a list

	fb_data_lst = [feed] #includes one dictionary of our first 25 posts
	for i in range(3): #we want 100 posts. We've already gotten 25 in our first request so now we only need to do 3 more to give us 100
		next_url = feed["paging"]["next"] 
		resp = requests.get(next_url)
		feed = json.loads(resp.text)
		fb_data_lst.append(feed)

	f = open('facebook_data.txt', 'w')
	f.write(json.dumps(fb_data_lst, indent = 2))
	f.close()

#print(cache_contents)

#Write data to a database
conn = sqlite3.connect('facebook.sqlite')
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS POSTS')
cur.execute('CREATE TABLE POSTS (month TEXT, day TEXT, year TEXT, hour TEXT, minute TEXT, second TEXT)')

for item in cache_contents:
	for diction in item['data']:
		month = diction['created_time'][5:7]
		day = diction['created_time'][8:10]
		year = diction['created_time'][0:4]
		hour = diction['created_time'][11:13]
		minute = diction['created_time'][14:16]
		second = diction['created_time'][17:19]
		cur.execute('INSERT INTO POSTS (month, day, year, hour, minute, second) VALUES (?,?,?,?,?,?)', (month, day, year, hour, minute, second))

conn.commit()
#Visualizing the data
early_am = {}
am = {}
afternoon = {}
pm = {}

weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

#Created dictionaries for the four different time periods where the keys are the days (Mon, Tues, etc.) and the values are the number of facebook posts posted during that itme period
for dicts in cache_contents:
	for thing in dicts['data']:
		x = datetime.date(int(thing['created_time'][0:4]), int(thing['created_time'][5:7]), int(thing['created_time'][8:10])).ctime()
		days = datetime.date(int(thing['created_time'][0:4]), int(thing['created_time'][5:7]), int(thing['created_time'][8:10]))
		#print(x, days)
		dates = x.split()
		l = ['00','01','02','03','04','05']
		hour = thing['created_time'][11:13]
		if dates[0] == 'Mon' and hour in l:
			if dates[0] in early_am:
				early_am[dates[0]] +=1
			else:
				early_am[dates[0]] = 1 
		if dates[0] == 'Tue' and hour in l:
			if dates[0] in early_am:
				early_am[dates[0]] +=1
			else:
				early_am[dates[0]] = 1 
		if dates[0] == 'Wed' and hour in l:
			if dates[0] in early_am:
				early_am[dates[0]] +=1
			else:
				early_am[dates[0]] = 1 
		if dates[0] == 'Thu' and hour in l:
			if dates[0] in early_am:
				early_am[dates[0]] +=1
			else:
				early_am[dates[0]] = 1 
		if dates[0] == 'Fri' and hour in l:
			if dates[0] in early_am:
				early_am[dates[0]] +=1
			else:
				early_am[dates[0]] = 1 
		if dates[0] == 'Sat' and hour in l:
			if dates[0] in early_am:
				early_am[dates[0]] +=1
			else:
				early_am[dates[0]] = 1 
		if dates[0] == 'Sun' and hour in l:
			if dates[0] in early_am:
				early_am[dates[0]] +=1
			else:
				early_am[dates[0]] = 1 

for dicts in cache_contents:
	for thing in dicts['data']:
		x = datetime.date(int(thing['created_time'][0:4]), int(thing['created_time'][5:7]), int(thing['created_time'][8:10])).ctime()
		days = datetime.date(int(thing['created_time'][0:4]), int(thing['created_time'][5:7]), int(thing['created_time'][8:10]))
		#print(x, days)
		dates = x.split()
		l = ['06','07','08','09','10','11']
		hour = thing['created_time'][11:13]
		if dates[0] == 'Mon' and hour in l:
			if dates[0] in am:
				am[dates[0]] +=1
			else:
				am[dates[0]] = 1 
		if dates[0] == 'Tue' and hour in l:
			if dates[0] in am:
				am[dates[0]] +=1
			else:
				am[dates[0]] = 1 
		if dates[0] == 'Wed' and hour in l:
			if dates[0] in am:
				am[dates[0]] +=1
			else:
				am[dates[0]] = 1 
		if dates[0] == 'Thu' and hour in l:
			if dates[0] in am:
				am[dates[0]] +=1
			else:
				am[dates[0]] = 1 
		if dates[0] == 'Fri' and hour in l:
			if dates[0] in am:
				am[time] +=1
			else:
				am[dates[0]] = 1 
		if dates[0] == 'Sat' and hour in l:
			if dates[0] in am:
				am[dates[0]] +=1
			else:
				am[dates[0]] = 1 
		if dates[0] == 'Sun' and hour in l:
			if dates[0] in am:
				am[dates[0]] +=1
			else:
				am[dates[0]] = 1 

for dicts in cache_contents:
	for thing in dicts['data']:
		x = datetime.date(int(thing['created_time'][0:4]), int(thing['created_time'][5:7]), int(thing['created_time'][8:10])).ctime()
		days = datetime.date(int(thing['created_time'][0:4]), int(thing['created_time'][5:7]), int(thing['created_time'][8:10]))
		dates = x.split()
		l = ['12','13','14','15','16','17']
		hour = thing['created_time'][11:13]
		if dates[0] == 'Mon' and hour in l:
			if dates[0] in afternoon:
				afternoon[dates[0]] +=1
			else:
				afternoon[dates[0]] = 1 
		if dates[0] == 'Tue' and hour in l:
			if dates[0] in afternoon:
				afternoon[dates[0]] +=1
			else:
				afternoon[dates[0]] = 1 
		if dates[0] == 'Wed' and hour in l:
			if dates[0] in afternoon:
				afternoon[dates[0]] +=1
			else:
				afternoon[dates[0]] = 1 
		if dates[0] == 'Thu' and hour in l:
			if dates[0] in afternoon:
				afternoon[dates[0]] +=1
			else:
				afternoon[dates[0]] = 1 
		if dates[0] == 'Fri' and hour in l:
			if dates[0] in afternoon:
				afternoon[dates[0]] +=1
			else:
				afternoon[dates[0]] = 1 
		if dates[0] == 'Sat' and hour in l:
			if dates[0] in afternoon:
				afternoon[dates[0]] +=1
			else:
				afternoon[dates[0]] = 1 
		if dates[0] == 'Sun' and hour in l:
			if dates[0] in afternoon:
				afternoon[dates[0]] +=1
			else:
				afternoon[dates[0]] = 1 

for dicts in cache_contents:
	for thing in dicts['data']:
		x = datetime.date(int(thing['created_time'][0:4]), int(thing['created_time'][5:7]), int(thing['created_time'][8:10])).ctime()
		days = datetime.date(int(thing['created_time'][0:4]), int(thing['created_time'][5:7]), int(thing['created_time'][8:10]))
		dates = x.split()
		l = ['18','19','20','21','22','23']
		hour = thing['created_time'][11:13]
		if dates[0] == 'Mon' and hour in l:
			if dates[0] in pm:
				pm[dates[0]] +=1
			else:
				pm[dates[0]] = 1 
		if dates[0] == 'Tue' and hour in l:
			if dates[0] in pm:
				pm[dates[0]] +=1
			else:
				pm[dates[0]] = 1 
		if dates[0] == 'Wed' and hour in l:
			if dates[0] in pm:
				pm[dates[0]] +=1
			else:
				pm[dates[0]] = 1 
		if dates[0] == 'Thu' and hour in l:
			if dates[0] in pm:
				pm[dates[0]] +=1
			else:
				pm[dates[0]] = 1 
		if dates[0] == 'Fri' and hour in l:
			if dates[0] in pm:
				pm[dates[0]] +=1
			else:
				pm[dates[0]] = 1 
		if dates[0] == 'Sat' and hour in l:
			if dates[0] in pm:
				pm[dates[0]] +=1
			else:
				pm[dates[0]] = 1 
		if dates[0] == 'Sun' and hour in l:
			if dates[0] in pm:
				pm[dates[0]] +=1
			else:
				pm[dates[0]] = 1 

#added the values (of each specific time of day) from the dictionary into a list to get them in order (Mon-Sun)
correct_early_am = []
correct_early_am.append(early_am['Mon'])
correct_early_am.append(early_am['Tue'])
correct_early_am.append(early_am['Wed'])
correct_early_am.append(early_am['Thu'])
correct_early_am.append(early_am['Fri'])
correct_early_am.append(early_am['Sat'])
correct_early_am.append(early_am['Sun'])

correct_am = []
correct_am.append(am['Mon'])
correct_am.append(am['Thu'])
correct_am.append(am['Sun'])

correct_afternoon = []
correct_afternoon.append(afternoon['Mon'])
correct_afternoon.append(afternoon['Tue'])
correct_afternoon.append(afternoon['Wed'])
correct_afternoon.append(afternoon['Thu'])
correct_afternoon.append(afternoon['Fri'])
correct_afternoon.append(afternoon['Sun'])

correct_pm = []
correct_pm.append(pm['Mon'])
correct_pm.append(pm['Tue'])
correct_pm.append(pm['Wed'])
correct_pm.append(pm['Thu'])
correct_pm.append(pm['Fri'])
correct_pm.append(pm['Sat'])
correct_pm.append(pm['Sun'])

#Creating twitter data 
f = open('twitter_data.txt', 'r')
contents = json.loads(f.read())
#pprint.pprint(contents)


twitter_early_am = {}
twitter_am = {}
twitter_afternoon = {}
twitter_pm = {}

#Created dictionaries for the four different time periods where the keys are the days (Mon, Tues, etc.) and the values are the number of facebook posts posted during that itme period
for dicts in contents:
	time = dicts['created_at']
	dates = time.split()
	l = ['00','01','02','03','04','05']
	hour = dicts['created_at'][11:13]
	if dates[0] == 'Mon' and hour in l:
		if dates[0] in twitter_early_am:
			twitter_early_am[dates[0]] +=1
		else:
			twitter_early_am[dates[0]] = 1 
	if dates[0] == 'Tue' and hour in l:
		if dates[0] in twitter_early_am:
			twitter_early_am[dates[0]] +=1
		else:
			twitter_early_am[dates[0]] = 1 
	if dates[0] == 'Wed' and hour in l:
		if dates[0] in twitter_early_am:
			twitter_early_am[dates[0]] +=1
		else:
			twitter_early_am[dates[0]] = 1 
	if dates[0] == 'Thu' and hour in l:
		if dates[0] in twitter_early_am:
			twitter_early_am[dates[0]] +=1
		else:
			twitter_early_am[dates[0]] = 1 
	if dates[0] == 'Fri' and hour in l:
		if dates[0] in twitter_early_am:
			twitter_early_am[dates[0]] +=1
		else:
			twitter_early_am[dates[0]] = 1 
	if dates[0] == 'Sat' and hour in l:
		if dates[0] in twitter_early_am:
			twitter_early_am[dates[0]] +=1
		else:
			twitter_early_am[dates[0]] = 1 
	if dates[0] == 'Sun' and hour in l:
		if dates[0] in twitter_early_am:
			twitter_early_am[dates[0]] +=1
		else:
			twitter_early_am[dates[0]] = 1 

for dicts in contents:
	time = dicts['created_at']
	dates = time.split()
	l = ['06','07','08','09','10','11']
	hour = dicts['created_at'][11:13]
	if dates[0] == 'Mon' and hour in l:
		if dates[0] in twitter_am:
			twitter_am[dates[0]] +=1
		else:
			twitter_am[dates[0]] = 1 
	if dates[0] == 'Tue' and hour in l:
		if dates[0] in twitter_am:
			twitter_am[dates[0]] +=1
		else:
			twitter_am[dates[0]] = 1 
	if dates[0] == 'Wed' and hour in l:
		if dates[0] in twitter_am:
			twitter_am[dates[0]] +=1
		else:
			twitter_am[dates[0]] = 1 
	if dates[0] == 'Thu' and hour in l:
		if dates[0] in twitter_am:
			twitter_am[dates[0]] +=1
		else:
			twitter_am[dates[0]] = 1 
	if dates[0] == 'Fri' and hour in l:
		if dates[0] in twitter_am:
			twitter_am[dates[0]] +=1
		else:
			twitter_am[dates[0]] = 1 
	if dates[0] == 'Sat' and hour in l:
		if dates[0] in twitter_am:
			twitter_am[dates[0]] +=1
		else:
			twitter_am[dates[0]] = 1 
	if dates[0] == 'Sun' and hour in l:
		if dates[0] in twitter_am:
			twitter_am[dates[0]] +=1
		else:
			twitter_am[dates[0]] = 1 
print(twitter_am)
for dicts in contents:
	time = dicts['created_at']
	dates = time.split()
	l = ['12','13','14','15','16','17']
	hour = dicts['created_at'][11:13]
	if dates[0] == 'Mon' and hour in l:
		if dates[0] in twitter_afternoon:
			twitter_afternoon[dates[0]] +=1
		else:
			twitter_afternoon[dates[0]] = 1 
	if dates[0] == 'Tue' and hour in l:
		if dates[0] in twitter_afternoon:
			twitter_afternoon[dates[0]] +=1
		else:
			twitter_afternoon[dates[0]] = 1 
	if dates[0] == 'Wed' and hour in l:
		if dates[0] in twitter_afternoon:
			twitter_afternoon[dates[0]] +=1
		else:
			twitter_afternoon[dates[0]] = 1 
	if dates[0] == 'Thu' and hour in l:
		if dates[0] in twitter_afternoon:
			twitter_afternoon[dates[0]] +=1
		else:
			twitter_afternoon[dates[0]] = 1 
	if dates[0] == 'Fri' and hour in l:
		if dates[0] in twitter_afternoon:
			twitter_afternoon[dates[0]] +=1
		else:
			twitter_afternoon[dates[0]] = 1 
	if dates[0] == 'Sat' and hour in l:
		if dates[0] in twitter_afternoon:
			twitter_afternoon[dates[0]] +=1
		else:
			twitter_afternoon[dates[0]] = 1 
	if dates[0] == 'Sun' and hour in l:
		if dates[0] in twitter_afternoon:
			twitter_afternoon[dates[0]] +=1
		else:
			twitter_afternoon[dates[0]] = 1 

for dicts in contents:
	time = dicts['created_at']
	dates = time.split()
	l = ['18','19','20','21','22','23']
	hour = dicts['created_at'][11:13]
	if dates[0] == 'Mon' and hour in l:
		if dates[0] in twitter_pm:
			twitter_pm[dates[0]] +=1
		else:
			twitter_pm[dates[0]] = 1 
	if dates[0] == 'Tue' and hour in l:
		if dates[0] in twitter_pm:
			twitter_pm[dates[0]] +=1
		else:
			twitter_pm[dates[0]] = 1 
	if dates[0] == 'Wed' and hour in l:
		if dates[0] in twitter_pm:
			twitter_pm[dates[0]] +=1
		else:
			twitter_pm[dates[0]] = 1 
	if dates[0] == 'Thu' and hour in l:
		if dates[0] in twitter_pm:
			twitter_pm[dates[0]] +=1
		else:
			twitter_pm[dates[0]] = 1 
	if dates[0] == 'Fri' and hour in l:
		if dates[0] in twitter_pm:
			twitter_pm[dates[0]] +=1
		else:
			twitter_pm[dates[0]] = 1 
	if dates[0] == 'Sat' and hour in l:
		if dates[0] in twitter_pm:
			twitter_pm[dates[0]] +=1
		else:
			twitter_pm[dates[0]] = 1 
	if dates[0] == 'Sun' and hour in l:
		if dates[0] in twitter_pm:
			twitter_pm[dates[0]] +=1
		else:
			twitter_pm[dates[0]] = 1 

twitter_correct_early_am = []
twitter_correct_early_am.append(twitter_early_am['Mon'])
twitter_correct_early_am.append(twitter_early_am['Tue'])
twitter_correct_early_am.append(twitter_early_am['Wed'])
twitter_correct_early_am.append(twitter_early_am['Thu'])
twitter_correct_early_am.append(twitter_early_am['Fri'])
twitter_correct_early_am.append(twitter_early_am['Sat'])
twitter_correct_early_am.append(twitter_early_am['Sun'])

twitter_correct_am = []
twitter_correct_am.append(twitter_am['Mon'])
twitter_correct_am.append(twitter_am['Thu'])
twitter_correct_am.append(twitter_am['Sat'])


twitter_correct_afternoon = []
twitter_correct_afternoon.append(twitter_afternoon['Mon'])
twitter_correct_afternoon.append(twitter_afternoon['Tue'])
twitter_correct_afternoon.append(twitter_afternoon['Wed'])
twitter_correct_afternoon.append(twitter_afternoon['Thu'])
twitter_correct_afternoon.append(twitter_afternoon['Fri'])
twitter_correct_afternoon.append(twitter_afternoon['Sun'])

twitter_correct_pm = []
twitter_correct_pm.append(twitter_pm['Mon'])
twitter_correct_pm.append(twitter_pm['Tue'])
twitter_correct_pm.append(twitter_pm['Wed'])
twitter_correct_pm.append(twitter_pm['Thu'])
twitter_correct_pm.append(twitter_pm['Fri'])
twitter_correct_pm.append(twitter_pm['Sat'])
twitter_correct_pm.append(twitter_pm['Sun'])

#Creating the figure

plt.figure(figsize=(20,3))
N = 7
N1 = 3
N2 = 6
ind = np.arange(N) 
ind1 = np.arange(N1)
ind2 = np.arange(N2)


rects1 = plt.bar(ind - .4, correct_early_am, width = .2, align='center', label = 'Facebook', color = 'darkslateblue')
rects2 = plt.bar(ind -.4, twitter_correct_early_am, width = .2, align='center', label = 'Twitter', bottom = correct_early_am, color = 'darkslategray')

rects3 = plt.bar(ind1 - .2, correct_am, width = .2, align='center', color = 'goldenrod', label = 'Facebook')
rects4 = plt.bar(ind1 - .2, twitter_correct_am, width = .2, align='center', bottom = correct_am, color = 'cadetblue', label = "Twitter")

rects5 = plt.bar(ind2, correct_afternoon, width = .2, align='center', color = 'darkslateblue')
rects6 = plt.bar(ind2, twitter_correct_afternoon, width = .2, align='center', bottom = correct_afternoon, color = 'darkslategray')

rects7 = plt.bar(ind + .2, correct_pm, width = .2, align='center', color = 'goldenrod')
rects8 = plt.bar(ind + .2, twitter_correct_pm, width = .2, align='center', bottom = correct_pm, color = 'cadetblue')

days_of_week = np.arange(len(weekdays))
plt.xticks(days_of_week, weekdays)
plt.ylabel("Popularity")
plt.xlabel("Days of the Week")
plt.title("Facebook Activity At Certain Times of the Day Across the Course of a Week")
plt.legend()

#add labels to each bar
for rect in rects1:
	height = rect.get_height()
	plt.text(rect.get_x() + rect.get_width()/2.0, 1.0*height,
                '12am-5:59am',
                ha='center', va='bottom')
for rect in rects3:
	height = rect.get_height()
	plt.text(rect.get_x() + rect.get_width()/2.0, 1.10*height,
                '6am-11:59am',
                ha='center', va='bottom')
for rect in rects5:
	height = rect.get_height()
	plt.text(rect.get_x() + rect.get_width()/2.0, 1.10*height,
                '12pm-17:59pm',
                ha='center', va='bottom')
for rect in rects8:
	height = rect.get_height()
	plt.text(rect.get_x() + rect.get_width()/2.0, 1.10*height,
                '18pm-11:59pm',
                ha='center', va='bottom')

#plt.show()