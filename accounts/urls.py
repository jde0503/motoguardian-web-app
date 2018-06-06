from django.urls import path, include
from . import views
from django.contrib.auth.views import login, logout



urlpatterns = [

    path('login/', login, {'template_name': 'registration/login.html'}),
    path('logout/', logout, {'template_name': 'registration/login.html'}),

]
