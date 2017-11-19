import os
import pprint
import json
import google.oauth2.credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow

#this file contains the OAuth 2.0 information for this application, including its client_id and
# client_secret.
CLIENT_SECRETS_FILE = "client_secret.json"

# This access scope allows for full read/write access to the
# authenticated user's account.
SCOPES = ['https://www.googleapis.com/auth/youtube']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'

def get_token():
  #creating client object from the CLIENT_SECRETS_FILE to perform OAuth 2.0 operations and requesting reqd-only access to User's Gmail
  flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
  #instructing the user to open the authorizatoin URL in their browser, authorize the application, retrieve the authorization code - saved in credentials
  credentials = flow.run_console()
  #building a service object for the API I want to call
  return build(API_SERVICE_NAME, API_VERSION, credentials = credentials)

def execute(service):
	#making a request to the API service using the interface provided by the service object
	results = service.videos().list(part = 'snippet,contentDetails,statistics', chart = 'mostPopular', regionCode='US', maxResults = 50)
	#executing this request
	response = results.execute()
	nextPageToken = response.get('nextPageToken')
	next_results = service.videos().list(part = 'snippet,contentDetails,statistics', chart = 'mostPopular', regionCode='US', maxResults = 50, pageToken = nextPageToken)
	next_response = next_results.execute()
	response['items'] = response['items'] + next_response['items']
	return response

#CACHING 

try: 
    f = open('youtube_data.txt', 'r')
    cache_contents = json.loads(f.read()) #opening the file to collect datafrom cached data instead of live data
    f.close()
except: 
	service = get_token()
	data = execute(service)
	pprint.pprint(data)
	f = open('youtube_data.txt', 'w')
	f.write(json.dumps(data, indent = 2))
	f.close()

print(len(cache_contents['items'])) #checking to make sure I got back 100 results!