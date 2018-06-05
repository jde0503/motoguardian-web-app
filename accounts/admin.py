from django.contrib import admin
from accounts.models import Leads, Device, Trip, Notification

# Register your models here.
admin.site.register(Leads)
admin.site.register(Device)
admin.site.register(Trip)
admin.site.register(Notification)


