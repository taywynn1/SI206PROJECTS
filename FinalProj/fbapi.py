import json
import requests
import pprint
from facebook_info import access_token


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
for item in cache_contents:
	print (len(item['data']))