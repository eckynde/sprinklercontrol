import requests
import json
import sys
import datetime
from weatherClass.weatherClass import weatherCurrent, weatherForecast
#from models import WeatherCurrent, WeatherForecast

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

        sprinkler1h = "0.00"
        clouds = data['current']['clouds']
        temperature = data['current']['temp']
        timeStamp_sunrise = data['current']['sunrise']
        timeStamp_sunset = data['current']['sunset']
        weather_id = data['current']['weather'][0]['id']
        weather_type = data['current']['weather'][0]['main']
        weather_desc = data['current']['weather'][0]['description']

        currentData = weatherCurrent(dt, city, status, rain1h, sprinkler1h, clouds,weather_id,weather_type,weather_desc,temperature,timeStamp_sunrise,timeStamp_sunset)
        currentData.printObject()

        #wC = WeatherCurrent(dt=dt, city=city, status=status, rain1h=rain1h, sprinkler1h=sprinkler1h,\
        #    clouds=clouds, weather_id=weather_id, weather_type=weather_type,weather_desc=weather_desc, \
        #    temperature=temperature, timeStamp_sunrise=timeStamp_sunrise, timeStamp_sunset=timeStamp_sunset)
        #wC.save()

        #print(datetime.datetime.fromtimestamp(dt).strftime('%H'))

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
            weather_id = objs['weather'][0]['id']
            weather_type = objs['weather'][0]['main']
            weather_desc = objs['weather'][0]['description']   

            forecastList.append(weatherForecast(dt, city, status, rain1h, clouds, weather_id, weather_type, weather_desc, temperature))   

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
