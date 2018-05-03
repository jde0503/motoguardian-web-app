from django.contrib import admin
from django.urls import path, include
from dashboard import views

urlpatterns = [
# dashboard/<username>/
    path('/',view.dashboard, name='dashboard'),
]
