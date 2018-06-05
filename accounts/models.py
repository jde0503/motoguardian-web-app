from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
# from django.db.models.signals import post_save
# from django.dispatch import receiver
from django.core.validators import MaxValueValidator, MinValueValidator
from django.urls import reverse
from django.conf import settings



# Create Leads Model (DB Table).
class Leads(models.Model):
    time_stamp = models.DateTimeField(default=timezone.now, blank=False)
    email_address = models.EmailField(unique=True)

    class Meta:
        verbose_name_plural = "Leads"

    def __str__(self):
        return self.email_address


class Device(models.Model):
	first_name = models.CharField(max_length=150)
	last_name = models.CharField(max_length=150)
	cellphone = models.CharField(max_length=50)
	mg_imei = models.CharField(max_length=50, unique=True) 
	mg_phone = models.CharField(max_length=50,unique=True)
	year = models.CharField(max_length=4)
	make = models.CharField(max_length=100)
	model = models.CharField(max_length=100)
	color = models.CharField(max_length=50)
	emergency_name = models.CharField(max_length=100)
	emergency_number = models.CharField(max_length=50)
	sensitivity = models.IntegerField(default=5, validators=[MaxValueValidator(10), MinValueValidator(1)])
	trip_tracking = models.BooleanField()
	anti_theft = models.BooleanField()
	user = models.ForeignKey(User,on_delete=models.CASCADE,default=1)

	def __str__(self):
		return self.mg_imei

class Trip(models.Model):
	
	datetime = models.DateTimeField(default=timezone.now, blank=False)
	trip_number = models.CharField(max_length=150)
	speed = models.CharField(max_length=50)
	lean_angle = models.CharField(max_length=50)
	lat = models.CharField(max_length=50)
	lng = models.CharField(max_length=50)

	device_IMEI = models.ForeignKey(Device, to_field='mg_imei', on_delete=models.CASCADE)

	def __str__(self):
		return 'Trip #%s (%s)' % (self.trip_number, self.device_IMEI)

class Notification(models.Model):

	device_IMEI= models.ForeignKey(Device, on_delete=models.CASCADE, default=1)
	datetime = models.DateTimeField(default=timezone.now, blank=False)
	notification_type = models.CharField(max_length=150)
	lat = models.CharField(max_length=50)
	lng = models.CharField(max_length=50)
	

	def __str__(self):
		return '%s: %s' % (self.device_IMEI.mg_imei, self.datetime)



# arm/dismarm (status)
# iginition on/off
# 


