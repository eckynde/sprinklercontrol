## This script calculates the demand of each sprinkler and schedules its active timeframes
## Trigger script manually with "exec(open('sprinklercontrolapp/control_smart_sprinkler.py').read())"

from sprinklercontrolapp.models import WeatherCurrent, WeatherForecast, Sprinkler
import time, datetime
from datetime import timezone, datetime
from django_q.models import Schedule

def run():
    # Simple queries
    smart_sprinklers = Sprinkler.objects.filter(mode='S')
    latest_current = WeatherCurrent.objects.latest('dt')

    # TimeCalc
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

    # Advanced queries
    sprinkler_rain_history = WeatherCurrent.objects.filter(dt__gte = current_day_DT, dt__lte = latest_current.timeStamp_sunrise)
    sprinkler_rain_forecast = WeatherForecast.objects.filter(dt__gte = current_day_DT)
    sprinkler_rain_full_history = WeatherCurrent.objects.filter(dt__gte = current_day_DT)

    # Calculation of rain since 0:00 current day (cumulative) 
    cumulative_rain1h_history = 0.00
    for objs in sprinkler_rain_history:
        cumulative_rain1h_history += float(objs.rain1h)

    cumulative_rain1h_forecast = 0.00
    for objs in sprinkler_rain_forecast:
        cumulative_rain1h_forecast += float(objs.rain1h)

    cumulative_rain1h_fullhistory = 0.00
    for objs in sprinkler_rain_full_history:
        cumulative_rain1h_fullhistory += float(objs.rain1h)

    task_activate = 'sprinklercontrolapp.tasks.activate'
    task_deactivate = 'sprinklercontrolapp.tasks.deactivate'

# Calculation of daily demand for smart sprinklers
def schedule():
    is_morning = sunrise_DT-1800 >= current_time_DT-1800 and sunrise_DT-1800 < current_time_DT+1800
    name_prefix = '[Morning] ' if is_morning else '[Evening] '
    sprinkler_list = []

    # Schedule sprinkler activations
    for objs in smart_sprinklers:
        demand = calc_demand_sunrise(objs) if is_morning else calc_demand_sunset(objs)

        if demand > 0:
            sprinkler_list.append(objs.id)
            Schedule.objects.create(
                name=name_prefix + 'Deactivate sprinkler(s) ' + str(objs.id),
                func=task_deactivate,
                args=str(objs.id),
                repeats=0,
                schedule_type=Schedule.ONCE,
                next_run=get_next_run(is_morning, demand)
            )
    
    sprinkler_ids = ','.join(map(str, sprinkler_list))
    if sprinkler_ids != '':
        Schedule.objects.create(
            name=name_prefix + 'Activate sprinkler(s) ' + sprinkler_ids,
            func=task_activate,
            args=sprinkler_ids,
            repeats=0,
            schedule_type=Schedule.ONCE,
            next_run=get_next_run(is_morning)
        )

def get_next_run(morning, demand = 0):
    demand += sunrise_DT if morning else sunset_DT
    return datetime.fromtimestamp(demand)

#returns demand in sprinklertime (h)
def calc_demand_sunrise(objs):
    demand = float(objs.demand)
    output = float(objs.output)
    demand_until_sunset = (demand - cumulative_rain1h_history - cumulative_rain1h_forecast)*0.75
    if demand_until_sunset > 0 and output > 0:
        return (demand_until_sunset/output)*60*60
    else:
        return 0


def calc_demand_sunset(objs):
    demand = float(objs.demand)
    output = float(objs.output)
    demand_until_sunset = (demand - cumulative_rain1h_history - cumulative_rain1h_forecast)*0.75
    
    demand_compensation = demand - demand_until_sunset - cumulative_rain1h_fullhistory 

    if demand_compensation > 0 and output > 0:
        return (demand_compensation/output)*60*60
    else:
        return 0
