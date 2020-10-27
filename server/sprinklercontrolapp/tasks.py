from sprinklercontrolapp.models import SprinklerPoweredHistory, Sprinkler
from sprinklercontrolapp.weather_data import fetch_and_schedule
from sprinklercontrolapp.smart_sprinkler import schedule
from sprinklercontrolapp.power import setPowerstate

import pytz
from datetime import datetime

# smart activate/deactivate
def activate(*args):
    for pk in args:
        setPowerstate(pk, True)

def deactivate(*args):
    for pk in args:
        setPowerstate(pk, False)

# smart do scheduling run / pull weather data
def control_smart_sprinkler():
    schedule()

def get_weather_data():
    fetch_and_schedule()

#get_weather_data()