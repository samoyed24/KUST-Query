from django.db import models
from django.utils import timezone

class Logging(models.Model):
    IP_address = models.CharField(max_length=20)
    location = models.CharField(max_length = 100)
    time = models.DateTimeField("time visiting")
    def __str__(self):
        return self.IP_address + self.location

# class LastQuery(models.Model):                      
#     IP_address = models.CharField(max_length=20)
#     time = models.DateTimeField("last query") 
# 以上这些暂时不用

class Message(models.Model):
    username = models.CharField(max_length=32)
    message = models.CharField(max_length=500)
    time = models.DateTimeField("time sent")

    
    

