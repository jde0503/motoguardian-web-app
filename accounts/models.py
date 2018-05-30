from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
# from django.db.models.signals import post_save
# from django.dispatch import receiver
from django.core.validators import MaxValueValidator, MinValueValidator
# from django.urls import reverse
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
	mg_imei = models.CharField(max_length=50, unique=True)
	mg_phone = models.CharField(max_length=50,unique=True)
	year = models.CharField(max_length=4)
	make = models.CharField(max_length=100)
	model = models.CharField(max_length=100)
	color = models.CharField(max_length=50)
	cellphone = models.CharField(max_length=50)
	emergency_name = models.CharField(max_length=100)
	emergency_number = models.CharField(max_length=50)
	sensitivity = models.IntegerField(default=5, validators=[MaxValueValidator(10), MinValueValidator(1)])
	trip_tracking = models.BooleanField()
	current_location = models.BooleanField()
	anti_theft = models.BooleanField()
	user = models.ForeignKey(User,on_delete=models.CASCADE,default=1)
	
	def __str__(self):
		return self.mg_imei

class Trip(models.Model):
	device = models.ForeignKey(Device,on_delete=models.CASCADE,default=1)
	# user = models.ForeignKey(Device,on_delete=models.CASCADE,default=1)
	time_stamp = models.DateTimeField(default=timezone.now, blank=False)
	distance_traveled = models.CharField(max_length=50)
	max_speed = models.CharField(max_length=50)
	max_leanAngle = models.CharField(max_length=50)
	
	def __str__(self):
		return '%s - '+ '%s' % (self.user, self.device)


