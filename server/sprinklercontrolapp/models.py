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
