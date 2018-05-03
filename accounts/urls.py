from django.urls import path, include
from . import views

urlpatterns = [
    # accounts/login/
    path('login/', views.login, name='login'),

    
    
]