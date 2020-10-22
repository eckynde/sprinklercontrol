## "exec(open('sprinklercontrolapp/controlSmartSprinkler.py').read())"

##--------------------Imports--------------------##
from sprinklercontrolapp.models import WeatherCurrent, WeatherForecast, Sprinkler
import time, datetime
from datetime import timezone


##--------------------Functions--------------------##
#returns demand in sprinklertime (h)
def calcDemandSunrise(objs):
    demand = float(objs.demand)
    output = float(objs.output)
    demand_until_sunset = (demand - cumultative_rain1h_history - cumultative_rain1h_forecast)*0.75
    if demand_until_sunset > 0 and output > 0:
        return demand_until_sunset/output
    else:
        return 0

def calcDemandSunset(objs):
    demand = float(objs.demand)
    output = float(objs.output)
    demand_until_sunset = (demand - cumultative_rain1h_history - cumultative_rain1h_forecast)*0.75
    
    demand_compensation = demand - demand_until_sunset - cumultative_rain1h_fullhistory 

    if demand_compensation > 0 and output > 0:
        return demand_compensation/output
    else:
        return 0

    
##--------------------Queries and data aquisition--------------------##
#Simple queries
smartSprinklers = Sprinkler.objects.filter(mode='S')
latestCurrent = WeatherCurrent.objects.latest('dt')

#TimeCalc
currentTime = datetime.datetime.utcnow()
year = currentTime.strftime("%Y")
month = currentTime.strftime("%m")
day = currentTime.strftime("%d")
# year / month / day / hour / min / sec
currentDay = int(datetime.datetime(int(year),int(month),int(day),0,0,0).replace(tzinfo=timezone.utc).timestamp())

#Advanced queries
sprinklerRainHistory = WeatherCurrent.objects.filter(dt__gte = currentDay, dt__lte = latestCurrent.timeStamp_sunrise)
sprinklerRainForecast = WeatherForecast.objects.filter(dt__gte = currentDay)
sprinklerRainFullHistory = WeatherCurrent.objects.filter(dt__gte = currentDay)


##--------------------Main Script--------------------##
#Calculation of rain since 0:00 current day (cumultative) 
cumultative_rain1h_history = 0.00
for objs in sprinklerRainHistory:
    cumultative_rain1h_history += float(objs.rain1h)

cumultative_rain1h_forecast = 0.00
for objs in sprinklerRainForecast:
    cumultative_rain1h_forecast += float(objs.rain1h)

cumultative_rain1h_fullhistory = 0.00
for objs in sprinklerRainFullHistory:
    cumultative_rain1h_fullhistory += float(objs.rain1h)


#Calculation of daily demand for smart sprinklers
for objs in smartSprinklers:
    print(calcDemandSunrise(objs))

for objs in smartSprinklers:
    print(calcDemandSunset(objs))