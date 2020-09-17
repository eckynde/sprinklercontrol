#!/usr/bin/env python

import requests
import json
import sys
from weatherClass.weatherClass import weatherClass

#Prüfen ob Parameter übergeben wurde

print("______________________________________________________"+"\n")

if not(len(sys.argv) != 2):
    city = sys.argv[1]
    #City im Skript angeben
    #city = input('Stadtnamen hier eingeben:')

    ######Dieser API Key holt aktuelle Wetterdaten: api.openweathermap.org/data/2.5/weather?q={{STADT}}&units=metric&appid={{API_KEY}}'
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&1h&dt&appid=XXX'.format(city)

    res = requests.get(url)
    data = res.json()

    ##print(res)
    ##print(data)

    ## Prüfe ob Data-load erfolgreich
    if str(res)=="<Response [200]>":
        print("[ Data load = success ]"+"\n")

        ## Regen in mm
        # 1mm = 1L / m²:
        if "rain" in data:
            rain1h = data['rain']['1h']
        else:
            rain1h = 0

        ## Wolken
        if "clouds" in data:
            clouds = data['clouds']['all']

        ## Wetter
        if "weather" in data:
            weather_id = data['weather'][0]['id']
            weather_type = data['weather'][0]['main']
            weather_desc = data['weather'][0]['description']
            
        ## Temperatur
        if "main" in data:
            temperature = data['main']['temp']

        ## Time Stamps
        if "dt" in data:
            timeStamp_DataLoad = data['dt']
        if "sys" in data:
            timeStamp_Sunrise = data['sys']['sunrise']
            timeStamp_Sunset = data['sys']['sunset']

        currentData = weatherClass(rain1h, clouds, weather_id, weather_type, weather_desc, \
       temperature, timeStamp_DataLoad, timeStamp_Sunrise, timeStamp_Sunset)

        currentData.printObject()
    else:
        print("[ Data load = error ]"+"\n")
        if "message" in data:
            print(str(res)+": "+data['message'])
else:
    print('[ Invalid Number of Arguments. ]')

print("\n"+"______________________________________________________")