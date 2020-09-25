from django.db import models


# Create your models here.
class Sprinkler(models.Model):
    label = models.CharField(max_length=40, verbose_name='Bezeichnung')
    description = models.CharField(max_length=150, verbose_name='Ort/Beschreibung')
    power = models.BooleanField(verbose_name='Eingeschaltet')
    enabled = models.BooleanField(verbose_name='Aktiviert')

    class Meta:
        verbose_name_plural = "Sprinklers"

    def __str__(self):
        return f'{self.label}'


class Weekday(models.Model):
    label = models.CharField(max_length=20, verbose_name='Bezeichnung')
    
    def __str__(self):
        return f'{self.label}'


class WeeklyRepeatingTimer(models.Model):
    label = models.CharField(max_length=40, verbose_name='Bezeichnung')
    description = models.CharField(max_length=150, verbose_name='Beschreibung')
    timestart = models.TimeField(verbose_name='Startzeit')
    timestop = models.TimeField(verbose_name='Stopzeit')
    weekdays = models.ManyToManyField(Weekday)
    sprinklers = models.ManyToManyField(Sprinkler)
    
    def __str__(self):
        return f'{self.label}'