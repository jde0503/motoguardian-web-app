from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from accounts.models import Leads
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.mail import send_mail, EmailMessage
from django.urls import reverse, reverse_lazy
from .forms import CustomUserCreationForm, DeviceForm
from django.contrib import messages
from django.views.generic import TemplateView, DetailView, ListView
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib.auth.models import User
from .models import Device, Trip, Notification
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import DeviceSerializer, TripSerializer, NotificationSerializer
from rest_framework import status
from django.http import JsonResponse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import requests
from django.db.models import Q
from django.http import Http404

#Renders Info of each device
class DeviceView(TemplateView):
    login_required = True
    template_name = 'dashboard/device.html'
    # dashboard/<mg_imei>/
    slug_field = 'mg_imei'
    slug_url_kwarg = 'mg_imei'
    
    def get(self, request, mg_imei ):
        devices = Device.objects.filter(mg_imei=mg_imei)
        try:
            # trips = Trip.objects.filter(device_IMEI=mg_imei).order_by('-datetime')
            notifications = Notification.objects.filter(device_IMEI=mg_imei).order_by('-datetime')
            latest_notification = Notification.objects.filter(device_IMEI=mg_imei).latest('datetime')
        except Notification.DoesNotExist:
            return render(request, self.template_name, {'devices':devices})
        for notification in notifications:
            latVal = str(notification.lat)
            lngVal = str(notification.lng)
            url = 'http://maps.googleapis.com/maps/api/geocode/json?latlng=%s,%s&sensor=false' % (latVal,lngVal)
            json_data = requests.get(url).json()
            try:
                location = json_data['results'][0]['formatted_address']
            except IndexError:
                location = "location not available"
            notification.location = location
        latest_notification.location = location
        lat_current = str(latest_notification.lat)
        lng_current = str(latest_notification.lng)
        url = 'http://maps.googleapis.com/maps/api/geocode/json?latlng=%s,%s&sensor=false' % (lat_current,lng_current)
        json_data = requests.get(url).json()
        try:
            location = json_data['results'][0]['formatted_address']
        except IndexError:
            location = "waiting for Google Maps API. Please refresh."
        latest_notification.location = location

        # print(notifications.location)
        args = {'devices':devices, 'notifications':notifications,'latest_notification':latest_notification}
        return render(request, self.template_name, args)

#View for Trip History
class TripView(TemplateView):
    login_required = True
    template_name = 'dashboard/trip.html'
    
    slug_field = 'mg_imei'
    slug_url_kwarg = 'mg_imei'
    def get(self, request, mg_imei):
        # trips = Trip.objects.filter(device_IMEI=mg_imei)
        query = request.GET.get('trip_number')

        if query:
            distinct_trip = Trip.objects.filter(device_IMEI=mg_imei).values('trip_number').distinct()
            num_speed = []
            num_lean = []
            trip_number = Trip.objects.filter(
            Q(trip_number=str(query)),
            Q(device_IMEI=mg_imei),
            ).order_by('-datetime')
            for item in trip_number:
                num_speed.append(float(item.speed))
                num_lean.append(float(item.lean_angle))
            sum_speed = sum(num_speed)
            sum_lean = sum(num_lean) 
            n_speed = len(num_speed)
            n_lean = len(num_lean) 


            
            trip_info = Trip.objects.filter(
            Q(trip_number=str(query)),
            Q(device_IMEI=mg_imei),
            )
            trip_info = trip_info.latest('datetime')
            trip_info.query = 1
            trip_info.avg_speed = sum_speed/n_lean
            trip_info.avg_lean = sum_lean/n_lean
            args = {'trip':trip_number, 'distinct_trip':distinct_trip, 'trip_info':trip_info}
            return render(request, self.template_name, args)

        # else get query set of most recent trip
        else:
            #get lastest trip number
            try: 
                latest_num = Trip.objects.filter(device_IMEI=mg_imei).latest('datetime')
            except Trip.DoesNotExist:
                raise Http404("No trips recorded.")
            lastest_trip_number = latest_num.trip_number
            distinct_trip = Trip.objects.filter(device_IMEI=mg_imei).values('trip_number').distinct()
            # distinct_trip = Trip.objects.filter(device_IMEI=mg_imei).order_by('-datetime').distinct('trip_number')
            # print(distinct_trip[0].trip_number)

            latest_trip = Trip.objects.filter(
            Q(trip_number=str(lastest_trip_number)),
            Q(device_IMEI=mg_imei),
            )
            num_speed = []
            num_lean = []
            for item in latest_trip:
                num_speed.append(float(item.speed))
                num_lean.append(float(item.lean_angle))
            sum_speed = sum(num_speed)
            sum_lean = sum(num_lean) 
            n_speed = len(num_speed)
            n_lean = len(num_lean)
            
            trip_info = latest_trip.latest('datetime')
            trip_info.query = 0 
            trip_info.avg_speed = sum_speed/n_lean
            trip_info.avg_lean = sum_lean/n_lean 

            args = {'trip':latest_trip,'distinct_trip':distinct_trip,'trip_info':trip_info}
            return render(request, self.template_name, args)

# Lists all device on dashboard
class DashboardView(ListView):
    login_required = True
    template_name = 'dashboard/dashboard.html'
    context_object_name = 'devices'

    def get_queryset(self):
        user = self.request.user
        return Device.objects.filter(user=user)
    def get(self, request):
        user = self.request.user
        devices = Device.objects.filter(user=user)
        
        for device in devices:
            try:
                notifications = Notification.objects.filter(device_IMEI=device.mg_imei).latest('datetime')
            except Notification.DoesNotExist:
                continue
            
            device.lat = notifications.lat
            device.lng = notifications.lng

            url = 'http://maps.googleapis.com/maps/api/geocode/json?latlng=%s,%s&sensor=false' % (str(device.lat),str(device.lng))
            json_data = requests.get(url).json()
            try:
                location = json_data['results'][0]['formatted_address']
            except IndexError:
                location = "waiting for Google Maps API, please refresh page"
            device.location = location
            # device.location = location
            
            device.notification_type = notifications.notification_type
            
            if notifications.notification_type == "security_armed":
                device.armed = True
            elif notifications.notification_type == "security_disarmed":
                device.armed = False
            
            elif notifications.notification_type == "ignition_on":
                device.ignition = True
            elif notifications.notification_type == "ignition_off":
                device.ignition = False
            else:
                pass

            if notifications.notification_type == "crash_detected":
                device.crash = True
            else:
                device.crash = False 
            
            if notifications.notification_type == "theft_detected":
                device.theft = True
            else:
                device.theft = False 

            device.datetime = notifications.datetime

            device.save()
            
        args = {'devices':devices}
        return render(request, self.template_name, args)

@login_required
def add_device(request):
    if request.method == 'POST':
        f = DeviceForm(request.POST)
        if f.is_valid():
            new_device = f.save(commit=False)
            new_device.mg_phone = '+1' + new_device.mg_phone
            new_device.user=request.user
            new_device.save()
            f.save()
            return redirect('dashboard')
    else:
        f = DeviceForm()
    return render(request, 'dashboard/device_form.html', {'form':f})

class DeviceUpdate(SuccessMessageMixin,UpdateView):
    login_required = True
    model = Device
    template_name = 'dashboard/device_edit.html'
   
    slug_field = 'mg_imei'
    slug_url_kwarg = 'mg_imei'

    success_message = 'Device settings successfully saved!'

    fields = ['first_name','last_name','cellphone', 'mg_phone','year','make',
    'model','color','emergency_name','emergency_number',
    'sensitivity','trip_tracking','anti_theft']

    def get_success_url(self):
        
        return reverse('device-detail',kwargs={'mg_imei': self.object.mg_imei})

class DeviceDelete(DeleteView):
    login_required = True
    model = Device
    template_name = 'dashboard/device_confirm_delete.html'
    slug_field = 'mg_imei'
    slug_url_kwarg = 'mg_imei'
    success_url = reverse_lazy('dashboard')


class DeviceSettings(APIView):

    def get(self,request):
        query = request.GET.get('mg_imei')
        devices = Device.objects.filter(mg_imei=query)     
        serializer = DeviceSerializer(devices, many=True)
        return JsonResponse(serializer.data[0], safe=False)

    def post(self,request):
        pass


# User Registration View
def register(request):
    if request.method == 'POST':
        f = CustomUserCreationForm(request.POST)
        if f.is_valid():
            f.save()
            return render(request, 'registration/registration_success.html', {'form': f})
    else:
        f = CustomUserCreationForm()

    return render(request, 'registration/register.html', {'form': f})

# POST Email 
def email_leads(request):
    if request.method == 'POST':
        email = request.POST['email']

        with open('email_body.txt', 'r') as file:
                # create new Emails object
            Leads.objects.create(
                email_address=email
            )
            email = EmailMessage('MotoGuardian - Thank you!', file.read(), to=[email])
            email.send()

            return HttpResponse('')

# Logout View
def logout_view(request):
    logout(request)
    return render(request, 'landing.html', {})


@method_decorator(csrf_exempt, name='dispatch')
class TripAPI(APIView):

    def post(self, request, format=None):
        serializer = TripSerializer(data=request.data)
        x=request.POST.get("mg_imei")
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@method_decorator(csrf_exempt, name='dispatch')
class NotificationAPI(APIView):

    def post(self, request, format=None):
        serializer = NotificationSerializer(data=request.data)
     
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#












