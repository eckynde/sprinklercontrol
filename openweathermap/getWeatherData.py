import requests
import json

city = input('Stadtnamen hier eingeben:')
#print('Dies ist ein Test! Ihre eingegebene Stadt war:{}!!!'.format(city))

######Dieser API Key holt aktuelle Wetterdaten: api.openweathermap.org/data/2.5/weather?q={{STADT}}&units=metric&appid={{API_KEY}}'
url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&1h&dt&appid='.format(city)

res = requests.get(url)
data = res.json()

##print(res)
##print(data)

## Prüfe ob Data-load erfolgreich
if str(res)!="<Response [200]>" :
    print("Data load = error")
else:
    print("Data load = success")

    ## Prüfe ob Regen-Objekt vorhanden:
    if "rain" in data:
        rain1h = data['rain']['1h']
    else:
        rain1h = 0

    ## Wolken
    if "clouds" in data:
        clouds = data['clouds']['all']

    ## Wetter
    if "weather" in data:
        weather_id = data[0]['weather']['id']
        weather_type = data['weather']['main']
        weather_desc = data['weather']['description']
        

    ## Temperatur
    if "main" in data:
        temperature = data['main']['temp']

    ## Time Stamps
    if "dt" in data:
        timeStamp_DataLoad = data['dt']
    if "sys" in data:
        timeStamp_Sunrise = data['sys']['sunrise']
        timeStamp_Sunset = data['sys']['sunset']

    print(rain1h)