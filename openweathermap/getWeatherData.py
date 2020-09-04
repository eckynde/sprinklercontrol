import requests

city = input('Stadnamen hier eingeben:')
#print('Dies ist ein Test! Ihre eingegebene Stadt war:{}!!!'.format(city))

######Dieser API Key holt aktuelle Wetterdaten: api.openweathermap.org/data/2.5/weather?q={{STADT}}&units=metric&appid={{API_KEY}}'
url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid='.format(city)

res = requests.get(url)

data = res.json()

print(res)
print(data)