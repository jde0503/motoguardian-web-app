"""MotoGuardian URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, reverse
from accounts import views
from django.views.generic import TemplateView
from accounts.views import (
    DashboardView,
    DeviceView,
    DeviceUpdate,
    DeviceDelete,
    DeviceSettings,
    TripAPI,
    NotificationAPI

    )
from rest_framework.urlpatterns import format_suffix_patterns
# from django.urls import reverse


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name="landing.html"), name="landing"),
    path('about/', TemplateView.as_view(template_name="about.html"), name="about"),
    path('faqs', TemplateView.as_view(template_name="faqs.html"), name="faqs"),
    path('getting_started', TemplateView.as_view(template_name="getting_started.html"), name="getting_started"),
    path('email-leads/', views.email_leads, name='email-leads'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('register/', views.register, name='register'),
    

    # Shows the dashboard for ALL devices
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('dashboard/add-device/', views.add_device, name='add-device'),
    # Shows info for each device
    path('dashboard/<mg_imei>/', DeviceView.as_view(), name='device-detail'),
    path('dashboard/<mg_imei>/edit/', DeviceUpdate.as_view(), name='device-update'),
    path('dashboard/<mg_imei>/delete/', DeviceDelete.as_view(), name='device-delete'),

    
    # URL to GET device settings 
    path('device-settings/',DeviceSettings.as_view()),
    path('trip/', TripAPI.as_view()),
    path('notification/',NotificationAPI.as_view()),

]

urlpatterns = format_suffix_patterns(urlpatterns)
