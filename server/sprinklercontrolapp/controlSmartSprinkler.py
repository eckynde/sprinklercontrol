## "exec(open('sprinklercontrolapp/controlSmartSprinkler.py').read())"

##--------------------Imports--------------------##
from sprinklercontrolapp.models import WeatherCurrent, WeatherForecast, Sprinkler
import time, datetime
from datetime import timezone, datetime
from django_q.models import Schedule

##--------------------Functions--------------------##
#returns demand in sprinklertime (h)
def calcDemandSunrise(objs):
    demand = float(objs.demand)
    output = float(objs.output)
    demand_until_sunset = (demand - cumultative_rain1h_history - cumultative_rain1h_forecast)*0.75
    if demand_until_sunset > 0 and output > 0:
        return (demand_until_sunset/output)*60*60
    else:
        return 0

def calcDemandSunset(objs):
    demand = float(objs.demand)
    output = float(objs.output)
    demand_until_sunset = (demand - cumultative_rain1h_history - cumultative_rain1h_forecast)*0.75
    
    demand_compensation = demand - demand_until_sunset - cumultative_rain1h_fullhistory 

    if demand_compensation > 0 and output > 0:
        return (demand_compensation/output)*60*60
    else:
        return 0

    
##--------------------Queries and data aquisition--------------------##
#Simple queries
smartSprinklers = Sprinkler.objects.filter(mode='S')
latestCurrent = WeatherCurrent.objects.latest('dt')

#TimeCalc
currentTime = datetime.utcnow()
year = currentTime.strftime("%Y")
month = currentTime.strftime("%m")
day = currentTime.strftime("%d")
hour = currentTime.strftime("%H")
minute = currentTime.strftime("%M")
second = currentTime.strftime("%S")

# year / month / day / hour / min / sec
currentTimeDT = currentTime.replace(tzinfo=timezone.utc).timestamp()
currentDay = int(datetime(int(year),int(month),int(day),0,0,0).replace(tzinfo=timezone.utc).timestamp())
sunriseDT = int(latestCurrent.timeStamp_sunrise)
sunsetDT = int(latestCurrent.timeStamp_sunset)

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
if sunriseDT-1800 >= currentTimeDT-1800 and sunriseDT-1800 < currentTimeDT+1800:
    sprinkler_list=[]
    name = day + '.' + month + '.' + year +' - deactivate morning - sprinkler: '
    for objs in smartSprinklers:
        demandSunrise = calcDemandSunrise(objs)
        if demandSunrise > 0:
            #Schedule morning deactivation
            sprinkler_list.append(objs.id)
            Schedule.objects.create(name=name+str(objs.id),func='tasks.deaktivate', args=str(objs.id),repeats=1 ,schedule_type=Schedule.ONCE,next_run=datetime.fromtimestamp(sunriseDT+demandSunrise))

    #Schedule morning activation
    name = day + '.' + month + '.' + year +' - activate morning - sprinkler: '
    args = ','.join(map(str,sprinkler_list))
    if args != '':
        Schedule.objects.create(name=name+args,func='tasks.aktivate', args=args,repeats=1 ,schedule_type=Schedule.ONCE,next_run=datetime.fromtimestamp(sunriseDT))
       
else:
    sprinkler_list=[]
    name = day + '.' + month + '.' + year +' - deactivate evening - sprinkler: '
    for objs in smartSprinklers:
        demandSunset = calcDemandSunset(objs)
        if demandSunset > 0:
            #Schedule evening deactivation
            sprinkler_list.append(objs.id)
            Schedule.objects.create(name=name+str(objs.id),func='tasks.deaktivate', args=str(objs.id),repeats=1 ,schedule_type=Schedule.ONCE,next_run=datetime.fromtimestamp(sunsetDT+demandSunset))

    #Schedule evening activation
    name = day + '.' + month + '.' + year +' - activate evening - sprinkler: '
    args = ','.join(map(str,sprinkler_list))
    if args != '':
        Schedule.objects.create(name=name+args,func='tasks.aktivate', args=args,repeats=1 ,schedule_type=Schedule.ONCE,next_run=datetime.fromtimestamp(sunsetDT))