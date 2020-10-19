## This script is meant to be executed hourly to gather weather data

import requests
import json
import sys
import time
from sprinklercontrolapp.models import WeatherCurrent, WeatherForecast, Preferences

## Settings
## "exec(open('sprinklercontrolapp/getWeatherData.py').read())"
apiKey = Preferences.objects.first().apikey
city = Preferences.objects.first().city

## Global Variables
currentDT = ""
sunriseDT = ""
sunsetDT = ""

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

##Parse current data
def parseJsonCurrent(data):
    global currentDT
    global sunriseDT
    global sunsetDT

    if "current" in data:
        dt = data['current']['dt']
        currentDT = dt
        status = "200"
        
        if "rain" in data['current']:
            rain1h = data['current']['rain']['1h']
        else:
            rain1h = "0" 

        clouds = data['current']['clouds']
        temperature = data['current']['temp']
        timeStamp_sunrise = data['current']['sunrise']
        sunriseDT = timeStamp_sunrise
        timeStamp_sunset = data['current']['sunset']
        sunsetDT = timeStamp_sunset
        weather_id = data['current']['weather'][0]['id']
        weather_type = data['current']['weather'][0]['main']
        weather_desc = data['current']['weather'][0]['description']

        wTemp = WeatherCurrent(dt=dt, city=city, status=status, rain1h=rain1h,\
            clouds=clouds, weather_id=weather_id, weather_type=weather_type,weather_desc=weather_desc, \
            temperature=temperature, timeStamp_sunrise=timeStamp_sunrise, timeStamp_sunset=timeStamp_sunset)
        wTemp.save()
    else:
        writeError(404)

##Parse forecast data
def parseJsonForecast(data):
    global currentDT
    global sunriseDT
    global sunsetDT

    if "hourly" in data:
        for objs in data['hourly']:
            if objs['dt'] < sunsetDT: 

                dt = objs['dt']
                status = "200"
            
                if "rain" in objs:
                    rain1h = objs['rain']['1h']
                else:
                    rain1h = "0" 

                clouds = objs['clouds']
                temperature = objs['temp']
                weather_id = objs['weather'][0]['id']
                weather_type = objs['weather'][0]['main']
                weather_desc = objs['weather'][0]['description']   

                wTemp = WeatherForecast(dt=dt, city=city, status=status, rain1h=rain1h,\
                    clouds=clouds, weather_id=weather_id, weather_type=weather_type,weather_desc=weather_desc, \
                    temperature=temperature)
                wTemp.save()

def writeError(num):
    wTemp = WeatherCurrent(dt=int(time.time()) , city="", status=str(num), rain1h=0,\
        clouds=0, weather_id=0, weather_type="",weather_desc="", \
        temperature=0, timeStamp_sunrise=0, timeStamp_sunset=0)
    wTemp.save()
    sys.exit(num)


#Prüfen ob Parameter übergeben wurde
try:
    lon, lat = getLonLat(city)
except:
    writeError(404)
else:
    parseJsonCurrent(getWeatherJson(lon, lat))

    ## Validiert, ob das skript zum Zeitpunkt des Sonnenaufgangs ausgeführt wurde
    if sunriseDT >= currentDT-1800 and sunriseDT < currentDT+1800:
        parseJsonForecast(getWeatherJson(lon, lat))