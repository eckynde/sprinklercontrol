#!/usr/bin/env python

import requests
import json
import sys
from weatherClass.weatherClass import weatherClass

apiKey = "ca55cf484b9838023ef2239091a6b5e9"

##Get Longitude and Latitude
def getLonLat(city):
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&1h&dt&appid={}'.format(city, apiKey)
    res = requests.get(url)
    data = res.json()

    if str(res)=="<Response [200]>":
        if "coord" in data:
            return data['coord']['lon'], data['coord']['lat']
    else:
        if "message" in data:
            print(str(res)+": "+data['message'])
            sys.exit(99)

##Get Weather Data win Longitude and Latitude as JSON File
def getWeatherJson(lon, lat):
    url = 'https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&units=metric&1h&dt&exclude=minutely, daily, alerts&appid={}'.format(lat, lon, apiKey)
    res = requests.get(url)
    data = res.json()

    if str(res)=="<Response [200]>":
        return data
    else:
        if "message" in data:
            print(str(res)+": "+data['message'])
            sys.exit(99)

##Parse the whole fucking json and start DB Queries
def parseJson(json):
    print(json)






print("______________________________________________________"+"\n")

#Prüfen ob Parameter übergeben wurde
if not(len(sys.argv) != 2):
    city = sys.argv[1]
    
    try:
        lon, lat = getLonLat(city)
    except:
        sys.exit(99)
    else:
        parseJson(getWeatherJson(lon, lat))

else:
    print('[ Invalid Number of Arguments. ]')

print("\n"+"______________________________________________________")