## This script is meant to be executed hourly to gather weather data
## Trigger script manually with "exec(open('sprinklercontrolapp/get_weather_data.py').read())"

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

task_name = 'sprinklercontrolapp.tasks.control_smart_sprinkler'

# Fetch weather data for the configured city and schedule the calculation of sprinkler demand
def fetch_and_schedule():
    try:
        lon, lat = get_lon_lat(city)
    except:
        write_error(404)
    else:
        parse_json_current(get_weather_json(lon, lat))


        # Validates wether or not this script has been triggered 1h before sunrise within an intervall of 30 minutes
        if sunrise_DT - 3600 >= current_DT - 1800 and sunrise_DT - 3600 < current_DT + 1800:
            parse_json_forecast(get_weather_json(lon, lat))
            
            # Schedules the demand calculation 1h before sunrise and 1h before sunset
            Schedule.objects.create(
                name='[Morning] Calculate sprinkler demand',
                func=task_name,
                repeats=0,
                schedule_type=Schedule.ONCE,
                next_run=datetime.fromtimestamp(sunrise_DT - 1800)
            )

            Schedule.objects.create(
                name='[Evening] Calculate sprinkler demand',
                func=task_name,
                repeats=0,
                schedule_type=Schedule.ONCE,
                next_run=datetime.fromtimestamp(sunset_DT - 1800)
            )

# Get Longitude and Latitude for a city
def get_lon_lat(city):
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
def get_weather_json(lon, lat):
    url = 'https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&units=metric&1h&dt&exclude=minutely, daily, alerts&appid={}'.format(lat, lon, api_key)
    res = requests.get(url)
    data = res.json()

    if str(res)=="<Response [200]>":
        return data
    else:
        if "message" in data:
            print(str(res)+": "+data['message'])

# Parse current weather data and generate DB entry
def parse_json_current(data):
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
        write_error(404)

# Parse forecast data and generate DB entry
def parse_json_forecast(data):
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
def write_error(num):
    weather_db_entry = WeatherCurrent(dt=int(time.time()), city="", status=str(num), rain1h=0, \
        clouds=0, weather_id=0, weather_type="", weather_desc="", \
        temperature=0, timeStamp_sunrise=0, timeStamp_sunset=0)
    weather_db_entry.save()
    sys.exit(num)

#fetch_and_schedule()