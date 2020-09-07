from django.db import models

# Create your models here.
class sprinkler(models.Model):
    label = models.CharField(max_length=10)
    location = models.CharField(max_length=25)
    power = models.BooleanField()


class restrictions(models.Model):
    label = models.CharField(max_length=10)
    timeStart = models.DateTimeField()
    timeEnd = models.DateTimeField()
    description = models.CharField(max_length=25)
    sprinklerId = models.ForeignKey(sprinkler,on_delete=models.CASCADE)


class waterQuantity(models.Model):
    label = models.CharField(max_length=10)
    sprinklerId = models.ForeignKey(sprinkler,on_delete=models.CASCADE)
    waterQuantity = models.DecimalField(max_digits=10, decimal_places=2)
    timeStart = models.DateTimeField()
    timeEnd = models.DateTimeField()


class generalSettings(models.Model):
    label = models.CharField(max_length=10)
    description = models.CharField(max_length=25)
    value = models.CharField(max_length=10)


class error(models.Model):
    label = models.CharField(max_length=10)
    description = models.CharField(max_length=25)


class sprinklerError(models.Model):
    label = models.CharField(max_length=10)
    sprinklerId = models.ForeignKey(sprinkler,on_delete=models.CASCADE)
    errorId = models.ForeignKey(error,on_delete=models.CASCADE)
    timeStart = models.DateTimeField()
    timeEnd = models.DateTimeField()


class irrigation(models.Model):
    label = models.CharField(max_length=10)
    timeStart = models.DateTimeField()
    timeEnd = models.DateTimeField()
    sprinklerId = models.ForeignKey(sprinkler,on_delete=models.CASCADE)
