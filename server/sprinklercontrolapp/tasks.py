from sprinklercontrolapp.models import SprinklerPoweredHistory, Sprinkler
from sprinklercontrolapp.weather_data import fetch_and_schedule
from sprinklercontrolapp.smart_sprinkler import schedule
from sprinklercontrolapp.power import setPowerstate

import pytz
from datetime import datetime

def activate(*args):
    for pk in args:
        setPowerstate(pk, True)

def deactivate(*args):
    for pk in args:
        setPowerstate(pk, False)

def control_smart_sprinkler():
    schedule()

def get_weather_data():
    fetch_and_schedule()
