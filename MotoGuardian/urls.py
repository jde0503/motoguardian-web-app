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
from django.urls import path, include
from accounts import views as accounts_views
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name="landing.html"), name="landing"),
    path('about/', TemplateView.as_view(template_name="about.html"), name="about"),
    path('email-leads/', accounts_views.email_leads, name='email-leads'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('register/', accounts_views.register, name='register'),
    path('dashboard/', accounts_views.dashboard, name='dashboard'),
    # path('dashboard/devices/', accounts_views.devices, name='devices'),
    path('dashboard/devices/add/', accounts_views.add_device, name='add_device'),
    # path('dashboard/profile/', accounts_views.ProfileView.as_view(), name='profile'),
    # path('dashboard/profile/edit/',accounts_views.ProfileCreate.as_view(), name='profile-edit'),


]
