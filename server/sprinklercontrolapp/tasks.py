from sprinklercontrolapp.models import SprinklerPoweredHistory, Sprinkler
from sprinklercontrolapp.weather_data import fetch_and_schedule
from sprinklercontrolapp.smart_sprinkler import schedule

import pytz
from datetime import datetime

def activate(*args):
    for objs in args:
        Sprinkler.objects.filter(pk=objs).update(power=True)
        SprinklerPoweredHistory.objects.create(sprinkler=Sprinkler.objects.get(pk=objs), timeofevent=datetime.now(tz=pytz.timezone("Europe/Berlin")), powered=True)

def deactivate(*args):
    for objs in args:
        Sprinkler.objects.filter(pk=objs).update(power=False)
        SprinklerPoweredHistory.objects.create(sprinkler=Sprinkler.objects.get(pk=objs), timeofevent=datetime.now(tz=pytz.timezone("Europe/Berlin")), powered=False)

def control_smart_sprinkler():
    schedule()

def get_weather_data():
    fetch_and_schedule()
