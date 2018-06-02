from rest_framework import serializers
from .models import Device

class DeviceSerializer(serializers.ModelSerializer):

	class Meta:
		model = Device
		fields = ['mg_imei','mg_phone','year','make',
		'model','color','cellphone','emergency_name','emergency_number',
		'sensitivity','trip_tracking','current_location','anti_theft']
