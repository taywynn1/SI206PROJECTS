import pprint
import json
import google.oauth2.credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
import re
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from PIL import Image
import sqlite3

#this file contains the OAuth 2.0 information for this application, including its client_id and
# client_secret.
CLIENT_SECRETS_FILE = "client_secret.json"

# This access scope grants read-only access to the authenticated user's Drive
# account.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
API_SERVICE_NAME = 'gmail'
API_VERSION = 'v1'

def get_token():
  #creating client object from the CLIENT_SECRETS_FILE to perform OAuth 2.0 operations and requesting reqd-only access to User's Gmail
  flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
  #instructing the user to open the authorizatoin URL in their browser, authorize the application, retrieve the authorization code - saved in credentials
  credentials = flow.run_console()
  #building a service object for the API I want to call
  return build(API_SERVICE_NAME, API_VERSION, credentials = credentials)

def execute(service):
	#making a request to the API service using the interface provided by the service object
	results = service.users().threads().list(userId = 'tmwynn@umich.edu', maxResults = 100)
	#executing this request
	response = results.execute()
	message_id = []
	for message in response['threads']:
		message_id.append(message['id'])
	#print(message_id)
	new_data = []
	for ids in message_id:
		message = service.users().messages().get(userId = 'tmwynn@umich.edu', id = ids).execute()
		new_data.append(message)
	return new_data
	#pprint.pprint(response)

#CACHING 

try: 
    f = open('gmail_data.txt', 'r')
    cache_contents = json.loads(f.read()) #opening the file to collect data from cached data instead of live data
    f.close()
except: 
	service = get_token()
	data = execute(service)
	pprint.pprint(data)
	f = open('gmail_data.txt', 'w')
	f.write(json.dumps(data, indent = 2))
	f.close()


#print (len(cache_contents)) #checking to make sure I have 100 results 

#gathering a list of the names of everyone who sent the emails (first and last) - to be used for wordcloud
l = list()
for diction in cache_contents:
	headers = diction['payload']['headers']
	#print(headers[23])
	#print(headers[7])
	emails = headers[23]['value']
	actual_emails = emails.split(' ')
	if len(actual_emails) == 9:
		name = actual_emails[0] + actual_emails[1] + actual_emails[2] + actual_emails[3] + actual_emails[4] + actual_emails[5] + actual_emails[6] + actual_emails[7]
	elif len(actual_emails) == 8:
		name = actual_emails[0] + actual_emails[1] + actual_emails[2] + actual_emails[3] + actual_emails[4] + actual_emails[5] + actual_emails[6] 
	else:
		#len(actual_emails) == 3:
		name = actual_emails[0] + actual_emails[1]
	#print(name)
	l.append(name)
print(l)

#Write data to a database
conn = sqlite3.connect('gmail.sqlite')
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS USERS')
cur.execute('CREATE TABLE USERS (email TEXT, first_name TEXT, last_name TEXT)')

for item in cache_contents:
	names_dict = item['payload']['headers'][23]['value']
	emails = names_dict.split(' ')
	print(emails)
	#gathering all the first names and last names by doing some slicing (some people have longer names than others)
	if len(emails) == 9:
		first_name = emails[0] + " " + emails[1] + " " + emails[2]
		last_name = emails[3] + " " + emails[4] + " " + emails[5] + " " + emails[6] + " " + emails[7]
	elif len(emails) == 8:
		first_name = emails[0] + " " + emails[1] 
		last_name = emails[2] + " " + emails[3] + " " + emails[4] + " " + emails[5] + " " + emails[6] 
	else:
		first_name = emails[0]
		last_name = emails[1]
	#gathering all the emails by slicing (on email some people only have their first name listed throwing off the list)
	if len(emails) == 9:
		name_email = emails[8]
	elif len(emails) == 8:
		name_email = emails[7]
	elif len(emails) == 3:
		name_email = emails[2]
	elif len(emails) == 2:
		name_email = emails[1]
	print(name_email)
	cur.execute('INSERT INTO USERS (email, first_name, last_name) VALUES (?,?,?)', (name_email, first_name, last_name))

conn.commit()

#conn.close()


#Creating a wordcloud

wc = WordCloud(background_color = 'black', width=1200,
                          height=1000).generate(' '.join(l))
plt.imshow(wc)
plt.axis("off")
#plt.show()
