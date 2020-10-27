from django.core.management.base import BaseCommand
from sprinklercontrolapp.models import Weekday

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
        Weekday.objects.create(label='Sonntag')
        Weekday.objects.create(label='Montag')
        Weekday.objects.create(label='Dienstag')
        Weekday.objects.create(label='Mittwoch')
        Weekday.objects.create(label='Donnerstag')
        Weekday.objects.create(label='Freitag')
        Weekday.objects.create(label='Samstag')
