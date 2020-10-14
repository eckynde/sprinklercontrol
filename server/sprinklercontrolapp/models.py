from django.db import models


# Create your models here.
class Sprinkler(models.Model):
    label = models.CharField(max_length=40, verbose_name='Bezeichnung')
    description = models.CharField(max_length=150, verbose_name='Ort/Beschreibung')
    power = models.BooleanField(verbose_name='Eingeschaltet')
    mode = models.CharField(max_length=1, default='P', verbose_name='Modus')

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


class IrrigationPlan(models.Model):
    label = models.CharField(max_length=40, verbose_name='Bezeichnung')
    description = models.CharField(max_length=150, verbose_name='Beschreibung')
    active = models.BooleanField()
    timers = models.ManyToManyField(WeeklyRepeatingTimer)
    
    def __str__(self):
        return f'{self.label}'

    def save(self):

        if self.active == True:
            IrrigationPlan.objects.filter(active=True).update(active=False)

        super().save()

class WeatherCurrent(models.Model):
    dt = models.BigIntegerField(verbose_name='Zeitstempel Dataload')
    city = models.CharField(max_length=40, verbose_name='Stadt')
    status = models.CharField(max_length=16, verbose_name='Status')
    rain1h = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='Regen 1h')
    sprinkler1h = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='Sprinkler 1h')
    clouds = models.IntegerField(verbose_name='Wolken')
    weather_id = models.IntegerField(verbose_name='Wetter ID')
    weather_type = models.CharField(max_length=40, verbose_name='Wetter Typ')
    weather_desc = models.CharField(max_length=40, verbose_name='Wetter Beschreibung')
    temperature = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='Temperatur')
    timeStamp_sunrise = models.BigIntegerField(verbose_name='Zeitstempel Sonnenaufgang')
    timeStamp_sunset = models.BigIntegerField(verbose_name='Zeitstempel Sonnenuntergang')

    def __str__(self):
        return f'{self.dt}'

class WeatherForecast(models.Model):
    dt = models.BigIntegerField(verbose_name='Zeitstempel Dataload')
    city = models.CharField(max_length=40, verbose_name='Stadt')
    status = models.CharField(max_length=16, verbose_name='Status')
    rain1h = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='Regen 1h')
    clouds = models.IntegerField(verbose_name='Wolken')
    weather_id = models.IntegerField(verbose_name='Wetter ID')
    weather_type = models.CharField(max_length=40, verbose_name='Wetter Typ')
    weather_desc = models.CharField(max_length=40, verbose_name='Wetter Beschreibung')
    temperature = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='Temperatur')
 
    def __str__(self):
        return f'{self.dt}'