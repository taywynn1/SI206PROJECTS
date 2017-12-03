
import spotipy
import json
import pprint
import spotipy.util as util
from spotipy_info import username, scope, client_id, client_secret, redirect_uri
import sqlite3
import matplotlib.pyplot as plt
import numpy as np
#import plotly.plotly as py

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

#Write data to a database
conn = sqlite3.connect('spotify.sqlite')
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS TRACKS')
cur.execute('CREATE TABLE TRACKS (track_name TEXT, popularity INTEGER)')


for item in cache_contents:
	#print(item['track']['name'])
	cur.execute('INSERT INTO TRACKS (track_name, popularity) VALUES (?,?)', (item['track']['name'], item['track']['popularity']))

conn.commit()

#conn.close()

#Visualize data as a histogram
popularity = []
for diction in cache_contents:
	popularity.append(diction['track']['popularity'])
#print(popularity)
name = []
for thing in cache_contents:
	name.append(thing['track']['name'])
#print(name)

track_d = dict(zip(name, popularity))
plt.figure(figsize=(20,3))
colors = ['darkseagreen', 'indianred', 'goldenrod', 'steelblue', 'slateblue', 'indigo', 'salmon', 'darkred', 'darkolivegreen', 'indianred']
plt.bar(range(len(track_d)), track_d.values(), align = 'edge', width = .8, color = colors)
plt.xticks(range(len(track_d)), track_d.keys(), rotation = 'vertical')
plt.xlabel('Track Names')
plt.ylabel('Popularity')
plt.title('Popularity of Recently Added 100 Tracks in User Library')
plt.show()


