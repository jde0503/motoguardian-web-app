from rest_framework import serializers
from .models import Device, Trip, Notification

class DeviceSerializer(serializers.ModelSerializer):

	class Meta:
		model = Device
		fields = ['first_name','last_name','cellphone','mg_imei','mg_phone','year','make',
		'model','color','emergency_name','emergency_number',
		'sensitivity','trip_tracking','anti_theft']

class TripSerializer(serializers.ModelSerializer):

	class Meta:
		model = Trip
		fields = ['device_IMEI','trip_number', 'speed', 'lean_angle', 'lat','lng']

class NotificationSerializer(serializers.ModelSerializer):
	class Meta:
		model = Notification
		fields = ['device_IMEI','notification_type', 'lat','lng']


