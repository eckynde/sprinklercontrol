from django.db import models
import uuid

# Create your models here.
class Sprinkler(models.Model):
    uuid = models.UUIDField(primary_key=False, default=uuid.uuid4, editable=False, db_index=True)
    label = models.CharField(max_length=40, verbose_name='Bezeichnung')
    description = models.CharField(max_length=150, verbose_name='Ort/Beschreibung')
    power = models.BooleanField(verbose_name='Eingeschaltet', default=False)
    mode = models.CharField(max_length=1, default='P', verbose_name='Modus')
    demand = models.DecimalField(max_digits=6, decimal_places=2, default='0', verbose_name='Bedarf in mm am Tag')
    output = models.DecimalField(max_digits=6, decimal_places=2, default='0', verbose_name='Leistung in mm/h')

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
    weekdays = models.ManyToManyField(Weekday, verbose_name='Wochentage')
    sprinklers = models.ManyToManyField(Sprinkler, verbose_name='Sprinkler')
    
    def __str__(self):
        return f'{self.label}'


class IrrigationPlan(models.Model):
    label = models.CharField(max_length=40, verbose_name='Bezeichnung')
    description = models.CharField(max_length=150, verbose_name='Beschreibung')
    active = models.BooleanField(verbose_name='Aktiv')
    timers = models.ManyToManyField(WeeklyRepeatingTimer, verbose_name='Zeitintervalle')
    
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
    clouds = models.IntegerField(verbose_name='Wolken')
    weather_id = models.IntegerField(verbose_name='Wetter ID')
    weather_type = models.CharField(max_length=40, verbose_name='Wetter Typ')
    weather_desc = models.CharField(max_length=40, verbose_name='Wetter Beschreibung')
    temperature = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='Temperatur')
    timeStamp_sunrise = models.BigIntegerField(verbose_name='Zeitstempel Sonnenaufgang')
    timeStamp_sunset = models.BigIntegerField(verbose_name='Zeitstempel Sonnenuntergang')
    icon_ID = models.CharField(max_length=5,default='', verbose_name='Icon ID')

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
    icon_ID = models.CharField(max_length=5,default='', verbose_name='Icon ID')
 
    def __str__(self):
        return f'{self.dt}'




# Abstract singleton model, followed by settings model

class Singleton(models.Model):

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1
        super(Singleton, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj


class Preferences(Singleton):
    city = models.CharField(max_length=40, default='Bielefeld,DE', verbose_name='Stadt')
    apikey = models.CharField(max_length=40, default='', verbose_name='API-Key')


class SprinklerPoweredHistory(models.Model):
    sprinkler = models.ForeignKey(Sprinkler, on_delete=models.CASCADE, verbose_name=Sprinkler)
    timeofevent = models.DateTimeField(verbose_name="Eventzeit")
    powered = models.BooleanField(verbose_name="Angeschaltet")

