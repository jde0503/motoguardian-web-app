from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from accounts.models import Leads
from django.http import HttpResponse, HttpResponseRedirect
from django.core.mail import send_mail, EmailMessage
from django.urls import reverse, reverse_lazy
from .forms import CustomUserCreationForm, DeviceForm
from django.contrib import messages
from django.views.generic import TemplateView, DetailView, ListView
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib.auth.models import User
from .models import Device
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import DeviceSerializer
from rest_framework import status
from django.http import JsonResponse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin

# from django.core.urlresolvers import reverse_lazy


# Create your views here.

#Renders the Dashboard
class DeviceView(TemplateView):
    login_required = True
    template_name = 'dashboard/device.html'
    
    slug_field = 'mg_imei'
    slug_url_kwarg = 'mg_imei'
    
    def get(self, request, mg_imei ):
        # user = request.user
        devices = Device.objects.filter(mg_imei=mg_imei)
        args = {'devices':devices}
        # print(devices)
        return render(request, self.template_name, args)

# Lists all device on dashboard
class DashboardView(ListView):
    login_required = True
    # model = Device
    template_name = 'dashboard/dashboard.html'
    context_object_name = 'devices'

    def get_queryset(self):
        user = self.request.user
        return Device.objects.filter(user=user)

# when clicked on ,shows the info on each device (notifications, location history, statistics, etc.) 
# class DeviceView(DetailView):
#     model = Device
#     template_name = 'dashboard/device.html'
#     context_object_name = 'devices'
#     # pk_url_kwarg = "mg_imei"



class DeviceSettings(APIView):
    def get(self,request):
        query = request.GET.get('mg_imei')
        devices = Device.objects.filter(mg_imei=query)
 
       
        serializer = DeviceSerializer(devices, many=True)
        # return Response(serializer.data)
        return JsonResponse(serializer.data[0], safe=False)

    def post(self,request):
        pass


def logout_view(request):
    logout(request)
    return render(request, 'landing.html', {})

# def devices(request):
#     User.objects.get(username=the_username).pk
    
@login_required
def add_device(request):
    if request.method == 'POST':
        f = DeviceForm(request.POST)
        if f.is_valid():
            new_device = f.save(commit=False)
            new_device.user=request.user
            new_device.save()
            # print(f['color'].value())
            # print(f.data['color'])
            f.save()
            return redirect('dashboard')
            # return render(request, 'dashboard/devices.html',{'form':f})
    else:
        f = DeviceForm()
    return render(request, 'dashboard/device_form.html', {'form':f})

class DeviceUpdate(SuccessMessageMixin,UpdateView):
    model = Device
    template_name = 'dashboard/device_edit.html'
   
    slug_field = 'mg_imei'
    slug_url_kwarg = 'mg_imei'

    success_message = 'Device settings successfully saved!'

    fields = ['first_name','last_name','cellphone','mg_imei','mg_phone','year','make',
    'model','color','emergency_name','emergency_number',
    'sensitivity','trip_tracking','anti_theft']

    def get_success_url(self):
        
        return reverse('device-detail',kwargs={'mg_imei': self.object.mg_imei})

class DeviceDelete(DeleteView):
    model = Device
    template_name = 'dashboard/device_confirm_delete.html'
    slug_field = 'mg_imei'
    slug_url_kwarg = 'mg_imei'
    success_url = reverse_lazy('dashboard')
    # def get_success_url(self):
    #     return reverse_lazy('dashboard')
    
def register(request):
    if request.method == 'POST':
        f = CustomUserCreationForm(request.POST)
        if f.is_valid():
            f.save()
            messages.success(request, 'Account created successfully')
            # return redirect('register')
            # return HttpResponseRedirect(reverse('login'))
            return render(request, 'registration/registration_success.html', {'form': f})
    else:
        f = CustomUserCreationForm()

    return render(request, 'registration/register.html', {'form': f})


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



