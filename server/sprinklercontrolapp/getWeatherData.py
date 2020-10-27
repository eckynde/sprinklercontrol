## This script is meant to be executed hourly to gather weather data
## Trigger script manually with "exec(open('sprinklercontrolapp/getWeatherData.py').read())"

##--------------------Imports--------------------##
import requests
import json
import sys
import time, datetime
from datetime import datetime
from sprinklercontrolapp.models import WeatherCurrent, WeatherForecast, Preferences
from django_q.models import Schedule


##--------------------Important-variables--------------------##
# Load Preferences
api_key = Preferences.objects.first().apikey
city = Preferences.objects.first().city


# Global Variables
current_DT = ""
sunrise_DT = ""
sunset_DT = ""


##--------------------Functions--------------------##
# Get Longitude and Latitude
def getLonLat(city):
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&1h&dt&appid={}'.format(city, api_key)
    res = requests.get(url)
    data = res.json()

    if str(res)=="<Response [200]>":
        if "coord" in data:
            return data['coord']['lon'], data['coord']['lat']
    else:
        if "message" in data:
            print(str(res)+": "+data['message'])


# Get Weather Data win Longitude and Latitude as JSON File
def getWeatherJson(lon, lat):
    url = 'https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&units=metric&1h&dt&exclude=minutely, daily, alerts&appid={}'.format(lat, lon, api_key)
    res = requests.get(url)
    data = res.json()

    if str(res)=="<Response [200]>":
        return data
    else:
        if "message" in data:
            print(str(res)+": "+data['message'])


# Parse current weather data and generate DB entry
def parseJsonCurrent(data):
    global current_DT
    global sunrise_DT
    global sunset_DT

    if "current" in data:
        dt = data['current']['dt']
        current_DT = dt
        status = "200"
        
        if "rain" in data['current']:
            rain1h = data['current']['rain']['1h']
        else:
            rain1h = "0" 

        clouds = data['current']['clouds']
        temperature = data['current']['temp']
        timeStamp_sunrise = data['current']['sunrise']
        sunrise_DT = timeStamp_sunrise
        timeStamp_sunset = data['current']['sunset']
        sunset_DT = timeStamp_sunset
        weather_id = data['current']['weather'][0]['id']
        weather_type = data['current']['weather'][0]['main']
        weather_desc = data['current']['weather'][0]['description']
        weather_icon = data['current']['weather'][0]['icon']

        weather_db_entry = WeatherCurrent(dt=dt, city=city, status=status, rain1h=rain1h,\
            clouds=clouds, weather_id=weather_id, weather_type=weather_type,weather_desc=weather_desc, \
            temperature=temperature, timeStamp_sunrise=timeStamp_sunrise, timeStamp_sunset=timeStamp_sunset, icon_ID=weather_icon)
        weather_db_entry.save()
    else:
        writeError(404)


# Parse forecast data and generate DB entry
def parseJsonForecast(data):
    global current_DT
    global sunrise_DT
    global sunset_DT

    if "hourly" in data:
        for objs in data['hourly']:
            if objs['dt'] < sunset_DT: 

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
                weather_icon = objs['weather'][0]['icon']   

                weather_db_entry = WeatherForecast(dt=dt, city=city, status=status, rain1h=rain1h,\
                    clouds=clouds, weather_id=weather_id, weather_type=weather_type,weather_desc=weather_desc, \
                    temperature=temperature, icon_ID=weather_icon)
                weather_db_entry.save()


# Throws an error by ID and generates an DB entry
def writeError(num):
    weather_db_entry = WeatherCurrent(dt=int(time.time()) , city="", status=str(num), rain1h=0,\
        clouds=0, weather_id=0, weather_type="",weather_desc="", \
        temperature=0, timeStamp_sunrise=0, timeStamp_sunset=0)
    weather_db_entry.save()
    sys.exit(num)


##--------------------Main script--------------------##
# Checks wether or not the longitude and latitude have been received 
try:
    lon, lat = getLonLat(city)
except:
    writeError(404)
else:
    parseJsonCurrent(getWeatherJson(lon, lat))


    # Validates wether or not this script has been triggered 1h before sunrise within an intervall of an half hour
    if sunrise_DT-3600 >= current_DT-1800 and sunrise_DT-3600 < current_DT+1800:
        parseJsonForecast(getWeatherJson(lon, lat))
        
        # Schedules the demand calculation 1h before sunrise and 1h before sunset
        name = str(datetime.fromtimestamp(current_DT)) + ' ctrlSprinkler Morning' 
        Schedule.objects.create(name=name,func='tasks.controlSmartSprinkler',repeats=1 ,schedule_type=Schedule.ONCE,next_run=datetime.fromtimestamp(sunrise_DT-1800))

        name = str(datetime.fromtimestamp(current_DT)) + ' ctrlSprinkler Evening' 
        Schedule.objects.create(name=name,func='tasks.controlSmartSprinkler',repeats=1 ,schedule_type=Schedule.ONCE,next_run=datetime.fromtimestamp(sunset_DT-1800))
