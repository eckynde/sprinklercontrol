## This script calculates the demand of each sprinkler and schedules its active timeframes
## Trigger script manually with "exec(open('sprinklercontrolapp/controlSmartSprinkler.py').read())"

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

    
##--------------------Queries-and-data-aquisition--------------------##
#Simple queries
smart_sprinklers = Sprinkler.objects.filter(mode='S')
latest_current = WeatherCurrent.objects.latest('dt')


#TimeCalc
current_time = datetime.utcnow()
year = current_time.strftime("%Y")
month = current_time.strftime("%m")
day = current_time.strftime("%d")
hour = current_time.strftime("%H")
minute = current_time.strftime("%M")
second = current_time.strftime("%S")


# year / month / day / hour / min / sec
current_time_DT = current_time.replace(tzinfo=timezone.utc).timestamp()
current_day_DT = int(datetime(int(year),int(month),int(day),0,0,0).replace(tzinfo=timezone.utc).timestamp())
sunrise_DT = int(latest_current.timeStamp_sunrise)
sunset_DT = int(latest_current.timeStamp_sunset)


#Advanced queries
sprinkler_rain_history = WeatherCurrent.objects.filter(dt__gte = current_day_DT, dt__lte = latest_current.timeStamp_sunrise)
sprinkler_rain_forecast = WeatherForecast.objects.filter(dt__gte = current_day_DT)
sprinkler_rain_full_history = WeatherCurrent.objects.filter(dt__gte = current_day_DT)


##--------------------Main-script--------------------##
#Calculation of rain since 0:00 current day (cumultative) 
cumultative_rain1h_history = 0.00
for objs in sprinkler_rain_history:
    cumultative_rain1h_history += float(objs.rain1h)

cumultative_rain1h_forecast = 0.00
for objs in sprinkler_rain_forecast:
    cumultative_rain1h_forecast += float(objs.rain1h)

cumultative_rain1h_fullhistory = 0.00
for objs in sprinkler_rain_full_history:
    cumultative_rain1h_fullhistory += float(objs.rain1h)


#Calculation of daily demand for smart sprinklers
if sunrise_DT-1800 >= current_time_DT-1800 and sunrise_DT-1800 < current_time_DT+1800:
    sprinkler_list=[]
    name = day + '.' + month + '.' + year +' - deactivate morning - sprinkler: '
    for objs in smart_sprinklers:
        demandSunrise = calcDemandSunrise(objs)
        if demandSunrise > 0:
            #Schedule morning deactivation
            sprinkler_list.append(objs.id)
            Schedule.objects.create(name=name+str(objs.id),func='tasks.deactivate', args=str(objs.id),repeats=1 ,schedule_type=Schedule.ONCE,next_run=datetime.fromtimestamp(sunrise_DT+demandSunrise))

    #Schedule morning activation
    name = day + '.' + month + '.' + year +' - activate morning - sprinkler: '
    args = ','.join(map(str,sprinkler_list))
    if args != '':
        Schedule.objects.create(name=name+args,func='tasks.activate', args=args,repeats=1 ,schedule_type=Schedule.ONCE,next_run=datetime.fromtimestamp(sunrise_DT))
       
else:
    sprinkler_list=[]
    name = day + '.' + month + '.' + year +' - deactivate evening - sprinkler: '
    for objs in smart_sprinklers:
        demandSunset = calcDemandSunset(objs)
        if demandSunset > 0:
            #Schedule evening deactivation
            sprinkler_list.append(objs.id)
            Schedule.objects.create(name=name+str(objs.id),func='tasks.deactivate', args=str(objs.id),repeats=1 ,schedule_type=Schedule.ONCE,next_run=datetime.fromtimestamp(sunset_DT+demandSunset))

    #Schedule evening activation
    name = day + '.' + month + '.' + year +' - activate evening - sprinkler: '
    args = ','.join(map(str,sprinkler_list))
    if args != '':
        Schedule.objects.create(name=name+args,func='tasks.activate', args=args,repeats=1 ,schedule_type=Schedule.ONCE,next_run=datetime.fromtimestamp(sunset_DT))