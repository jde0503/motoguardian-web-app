from rest_framework import serializers
from .models import Device

class DeviceSerializer(serializers.ModelSerializer):

	class Meta:
		model = Device
		fields = ['first_name','last_name','cellphone','mg_imei','mg_phone','year','make',
		'model','color','emergency_name','emergency_number',
		'sensitivity','trip_tracking','anti_theft']
