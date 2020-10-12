#!/usr/bin/env python

import requests
import json
import sys
from weatherClass.weatherClass import weatherCurrent, weatherForecast

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

##Parse current data
def parseJsonCurrent(data):

    if "current" in data:
        dt = data['current']['dt']
        status = "200"
        
        if "rain" in data['current']:
            rain1h = data['current']['rain']['1h']
        else:
            rain1h = "0" 

        sprinkler1h = "?"
        clouds = data['current']['clouds']
        temperature = data['current']['temp']
        sunrise = data['current']['sunrise']
        sunset = data['current']['sunset']
        weatherID = data['current']['weather'][0]['id']
        weatherType = data['current']['weather'][0]['main']
        weatherDesc = data['current']['weather'][0]['description']

        currentData = weatherCurrent(dt, status, rain1h, "NULL" ,clouds,weatherID,weatherType,weatherDesc,temperature,sunrise,sunset)
        currentData.printObject()

##Parse forecast data
def parseJsonForecast(data):

    forecastList = []

    if "hourly" in data:
        for objs in data['hourly']:
            dt = objs['dt']
            status = "200"
        
            if "rain" in objs:
                rain1h = objs['rain']['1h']
            else:
                rain1h = "0" 

            clouds = objs['clouds']
            temperature = objs['temp']
            weatherID = objs['weather'][0]['id']
            weatherType = objs['weather'][0]['main']
            weatherDesc = objs['weather'][0]['description']   

            forecastList.append(weatherForecast(dt, status, rain1h, clouds, weatherID, weatherType, weatherDesc, temperature))   
    else:
        print("yeetS")

    for x in forecastList:
        x.printObject()





#Prüfen ob Parameter übergeben wurde
if not(len(sys.argv) != 2):
    city = sys.argv[1]
    
    try:
        lon, lat = getLonLat(city)
    except:
        sys.exit(99)
    else:
        parseJsonForecast(getWeatherJson(lon, lat))
        parseJsonCurrent(getWeatherJson(lon, lat))

else:
    print('[ Invalid Number of Arguments. ]')
