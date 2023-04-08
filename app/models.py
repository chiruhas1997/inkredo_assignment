from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class HolidayHomes(models.Model):
    user_name = models.OneToOneField(User, on_delete=models.CASCADE)
    home_name = models.CharField(max_length=150, unique=True)
    city = models.CharField(max_length=100)
    no_rooms = models.IntegerField()

class HomeImages(models.Model):
    image = models.FileField(upload_to ='uploads/')

class Rooms(models.Model):
    holiday_homes = models.ForeignKey(HolidayHomes, default = None, on_delete=models.CASCADE)
    rents = models.CharField(max_length=100)
    rooom_id = models.CharField(max_length=20, default = None)
    availibility = models.BooleanField(default = True)
    check_in = models.DateTimeField(default = None)
    check_out = models.DateTimeField(default = None)
    rules = models.CharField(max_length = 1000, default = None)