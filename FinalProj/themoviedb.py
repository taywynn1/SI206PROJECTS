import json
import requests
import pprint
from themoviedb_info import api_key
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import sqlite3
#CACHING!
try: 
    f = open('themoviedb_data.txt', 'r')
    cache_contents = json.loads(f.read()) #opening the file to collect datafrom cached data instead of live data
    f.close()
except: 
	movie_data_lst = []
	for i in range(5): #limit is 20 per page, so I want to make the call 5 times (20*5). 
		baseurl = "https://api.themoviedb.org/3/tv/top_rated?page={}".format((i+1))
	## Building the The Movie DB parameters dictionary
		url_params = {}
		url_params["api_key"] = api_key
		url_params["language"] = "en-US" 

		r = requests.get(baseurl,params=url_params)

		data = json.loads(r.text) #returns a dictionary and in order to support paging we want to add it to a list
		movie_data_lst.append(data)

#pprint.pprint(movie_data_lst)

	f = open('themoviedb_data.txt', 'w')
	f.write(json.dumps(movie_data_lst, indent = 2))
	f.close()

#print (len(cache_contents))
#print(len(cache_contents[0]['results'])) #checking to make sure I have 100 results!

#Write data to a database
conn = sqlite3.connect('themoviedb.sqlite')
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS TV')
cur.execute('CREATE TABLE TV (name TEXT, popularity INTEGER, overview TEXT)')

for item in cache_contents:
	for dictions in item['results']:
		cur.execute('INSERT OR IGNORE INTO TV (name, popularity, overview) VALUES (?,?,?)', (dictions['name'], dictions['popularity'], dictions['overview']))

conn.commit()

#conn.close()

#Create a dictionary where the keys are the country names and values are how many times they appear
d = {}
for item in cache_contents:
	for dictions in item['results']:
		#print(dictions)
		for country in dictions['origin_country']:
			if country in d:
				d[country] += 1
			else:
				d[country] = 1
#print(d) 

#Create a dictionary (for each country from the dictionary above) where the keys are the tv shows names and values are the popularity  
usaDict = {}
japanDict = {}
englandDict = {}
canadaDict = {}
italyDict = {}

for item in cache_contents:
	for dictions in item['results']:
		if 'US' in dictions['origin_country']:
			usaDict[dictions['name']] = dictions['popularity']
		if 'JP' in dictions['origin_country']:
			japanDict[dictions['name']] = dictions['popularity']
		if 'GB' in dictions['origin_country']:
			englandDict[dictions['name']] = dictions['popularity']
		if 'CA' in dictions['origin_country']:
			canadaDict[dictions['name']] = dictions['popularity']
		if 'IT' in dictions['origin_country']:
			italyDict[dictions['name']] = dictions['popularity']
#print(usaDict)


#sort dictionaries based on popularity
usa_popular = sorted(usaDict, key = lambda x: usaDict[x], reverse = True)
canada_popular = sorted(canadaDict, key = lambda x: canadaDict[x], reverse = True)
japan_popular = sorted(japanDict, key = lambda x: japanDict[x], reverse = True)
england_popular = sorted(englandDict, key = lambda x: englandDict[x], reverse = True)
italy_popular = sorted(italyDict, key = lambda x: italyDict[x], reverse = True)


#Visualizing data with a map

fig, ax = plt.subplots()

map = Basemap(projection = 'mill', llcrnrlat = -90, urcrnrlat = 90, llcrnrlon = -180, urcrnrlon = 180, resolution = 'c')

map.drawcoastlines()
map.drawcountries()
map.fillcontinents(color = 'palegreen', lake_color = 'mediumturquoise')
map.drawmapboundary(fill_color = "mediumturquoise")

#Creating the latitudes and longitudes for each country (in most cases I chose the captal). Did not create a list because I wanted to make each data point a different size on the map. 
lat_usa = 33.9072
lat_canada = 53.4215
lat_england = 51.5074
lat_italy = 41.9028
lat_japan = 35.6895

lon_usa = -96.0369
lon_canada =  -64.6972 
lon_england = -.1278
lon_italy = 12.4962
lon_japan = 139.6917

#Creating the labels for the most popular tv shows in each country

#annotating most popular tv show in the United States
plt.annotate(usa_popular[0], xy = (.16,.65), xycoords='axes fraction', fontsize = 5, fontweight = 'bold', color = 'm')
#annotating most popular tv show in Great Britain
plt.annotate(england_popular[0], xy= (.5, .73), xycoords='axes fraction', xytext=(.45, .85),
            arrowprops=dict(facecolor='black', shrink=0.1), fontsize = 6, fontweight = 'bold', color = 'm')
#annotating most popular tv show in Italy
plt.annotate(italy_popular[0], xy= (.53, .68), xycoords='axes fraction', xytext=(.46, .25),
            arrowprops=dict(facecolor='black', shrink=0.1), fontsize = 6, fontweight = 'bold', color = 'm')
#annotating most popular tv show in Japan
plt.annotate(japan_popular[0], xy= (.905, .64), xycoords='axes fraction', xytext=(.87, .5),
            arrowprops=dict(facecolor='black', shrink=0.04), fontsize = 6, fontweight = 'bold', color = 'm')
#annotating most popular tv show in Canada
plt.annotate(canada_popular[0], xy= (.334, .71), xycoords='axes fraction', xytext=(.3, .58),
            arrowprops=dict(facecolor='black', shrink=0.1), fontsize = 6, fontweight = 'bold', color = 'm')


#Creating the data points that show the most popular origin country for the tv shows extracted
x,y = map(lon_usa,lat_usa)
map.plot(x,y, label = d['US'], marker = '.', color = 'r', markeredgecolor = 'white', markersize = 14)

x,y = map(lon_canada,lat_canada)
map.plot(x,y, label = d['CA'], marker = '.', color = 'r', markeredgecolor = 'white', markersize = 8)

x,y = map(lon_england,lat_england)
map.plot(x,y, label = d['GB'], marker = '.', color = 'r', markeredgecolor = 'white', markersize = 12)

x,y = map(lon_italy,lat_italy)
map.plot(x,y, label = d['IT'], marker = '.', color = 'r', markeredgecolor = 'white', markersize = 6)

x,y = map(lon_japan,lat_japan)
map.plot(x,y, label = d['JP'], marker = '.', color = 'r', markeredgecolor = 'white', markersize = 10)

#make a legend for the map
legend2 = ax.legend(loc = "lower right", facecolor = 'darkgrey', title = 'Origin Country Popularity', prop= {'size':8})
ax.add_artist(legend2)

#Code to show the mapxs
#plt.show()
#plt.savefig('World Map.png')

