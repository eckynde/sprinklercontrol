from django.db import models

# Create your models here.
class Sprinkler(models.Model):
    label = models.CharField(max_length=10)
    location = models.CharField(max_length=25)
    power = models.BooleanField()


class Restriction(models.Model):
    label = models.CharField(max_length=10)
    timeStart = models.DateTimeField()
    timeEnd = models.DateTimeField()
    description = models.CharField(max_length=25)
    sprinklerId = models.ForeignKey(Sprinkler,on_delete=models.CASCADE)


class WaterQuantity(models.Model):
    label = models.CharField(max_length=10)
    sprinklerId = models.ForeignKey(Sprinkler,on_delete=models.CASCADE)
    waterQuantity = models.DecimalField(max_digits=10, decimal_places=2)
    timeStart = models.DateTimeField()
    timeEnd = models.DateTimeField()


class GeneralSettings(models.Model):
    label = models.CharField(max_length=10)
    description = models.CharField(max_length=25)
    value = models.CharField(max_length=10)


class Error(models.Model):
    label = models.CharField(max_length=10)
    description = models.CharField(max_length=25)


class SprinklerError(models.Model):
    label = models.CharField(max_length=10)
    sprinklerId = models.ForeignKey(Sprinkler,on_delete=models.CASCADE)
    errorId = models.ForeignKey(Error,on_delete=models.CASCADE)
    timeStart = models.DateTimeField()
    timeEnd = models.DateTimeField()


class Irrigation(models.Model):
    label = models.CharField(max_length=10)
    timeStart = models.DateTimeField()
    timeEnd = models.DateTimeField()
    sprinklerId = models.ForeignKey(Sprinkler,on_delete=models.CASCADE)
