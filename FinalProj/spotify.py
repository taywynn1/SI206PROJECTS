
import spotipy
import json
import pprint
import spotipy.util as util
from spotipy_info import username, scope, client_id, client_secret, redirect_uri

token = util.prompt_for_user_token(username, scope, client_id, client_secret, redirect_uri)

sp = spotipy.Spotify(auth=token)
   


try: 
    f = open('spotify.txt', 'r')
    cache_contents = json.loads(f.read()) #opening the file to collect datafrom cached data instead of live data
    f.close()
except: 
	results = sp.current_user_saved_tracks(limit = 20)
	tracks = results['items']
    #Creating a while loop to support pagination. I've already gotten 20 results so Ijust need to run my loop 4 times to get 100 results
	next = 0
	while next <4:
		other = sp.next(results)
		tracks.extend(other['items'])
		next +=1
	pprint.pprint(tracks)
	f = open('spotify.txt', 'w')
	f.write(json.dumps(tracks, indent = 2))
	f.close()

print (len(cache_contents)) #checking to make sure I got back 100 results!
        #track = item['track']
        #print (track['name'] + ' - ' + track['artists'][0]['name'])
