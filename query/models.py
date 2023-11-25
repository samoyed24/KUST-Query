from django.db import models
from django.utils import timezone

class Logging(models.Model):
    IP_address = models.CharField(max_length=20)
    location = models.CharField(max_length = 100)
    time = models.DateTimeField("time visiting")
