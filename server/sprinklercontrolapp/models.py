from django.db import models


# Create your models here.
class Sprinkler(models.Model):
    label = models.CharField(max_length=40, verbose_name='Bezeichnung')
    location = models.CharField(max_length=150, verbose_name='Ort/Beschreibung')
    power = models.BooleanField(verbose_name='Eingeschaltet')
    enabled = models.BooleanField(verbose_name='Aktiviert')

    class Meta:
        verbose_name_plural = "Sprinklers"

    def __str__(self):
        return f'{self.label}'

class WeeklyRepeatingTimer(models.Model):
    weekdays = [
        (1,'Montag'),
        (2,'Dienstag'),
        (3,'Mittwoch'),
        (4,'Donnerstag'),
        (5,'Freitag'),
        (6,'Samstag'),
        (7,'Sonntag'),
    ]
    label = models.CharField(max_length=40, verbose_name='Bezeichnung')
    description = models.CharField(max_length=150, verbose_name='Beschreibung')
    timestart = models.TimeField(verbose_name='Startzeit')
    timestop = models.TimeField(verbose_name='Stopzeit')
    monday = models.BooleanField(verbose_name='Montag')
    tuesday = models.BooleanField(verbose_name='Dienstag')
    wednesday = models.BooleanField(verbose_name='Mittwoch')
    thursday = models.BooleanField(verbose_name='Donnerstag')
    friday = models.BooleanField(verbose_name='Freitag')
    saturday = models.BooleanField(verbose_name='Samstag')
    sunday = models.BooleanField(verbose_name='Sonntag')
    sprinklers = models.ManyToManyField(Sprinkler)
    
    def __str__(self):
        return f'{self.label}'
