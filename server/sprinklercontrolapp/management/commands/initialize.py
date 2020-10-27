from django.core.management.base import BaseCommand
from sprinklercontrolapp.models import Weekday
from django_q.models import Schedule
from datetime import datetime, timedelta, date
import pytz

class Command(BaseCommand):
    help = 'Initializes the application before the first start'

    def handle(self, *args, **options):
        if Weekday.objects.count() > 0:
            print('There are already objects in the Weekday table! Continue with initialization regardless? (y/N)')
            
            answer = input()
            if answer != 'y' and answer != 'Y':
                print('Aborted!')
                return

        print('Initializing...')
        Weekday.objects.create(id=0, label='Sonntag')
        Weekday.objects.create(id=1, label='Montag')
        Weekday.objects.create(id=2, label='Dienstag')
        Weekday.objects.create(id=3, label='Mittwoch')
        Weekday.objects.create(id=4, label='Donnerstag')
        Weekday.objects.create(id=5, label='Freitag')
        Weekday.objects.create(id=6, label='Samstag')


        # create plan history job
        Schedule.objects.create(
            name='Fetch history from microcontroller',
            func='sprinklercontrolapp.uart.main.get_history',
            repeats=-1,
            schedule_type=Schedule.HOURLY,
            next_run=datetime.now(tz=pytz.timezone("Europe/Berlin"))+timedelta(hours=1),
        )

        # create weather job
        Schedule.objects.create(
            name='Get weather data',
            func='sprinklercontrolapp.tasks.get_weather_data',
            repeats=-1,
            schedule_type=Schedule.HOURLY,
            next_run=datetime.now(tz=pytz.timezone("Europe/Berlin"))+timedelta(hours=1),
        )
