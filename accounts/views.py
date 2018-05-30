from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from accounts.models import Leads
from django.http import HttpResponse, HttpResponseRedirect
from django.core.mail import send_mail, EmailMessage
from django.urls import reverse
from .forms import CustomUserCreationForm, DeviceForm
from django.contrib import messages
from django.views import generic
from django.contrib.auth.decorators import login_required
# from .models import Profile
from django.db import transaction
from django.contrib.auth.models import User

# from django.views.generic.edit import CreateView, UpdateView, DeleteView
# from django.core.urlresolvers import reverse_lazy


# Create your views here.
@login_required
def dashboard(request):
    return render(request, 'dashboard/dashboard.html')

# class ProfileView(generic.ListView):
#     template_name = 'dashboard/profile.html'
#     context_object_name = 'settings'

#     def get_queryset(self):
#         return Profile.objects.all()

# class ProfileCreate(CreateView):
#     template_name = 'dashboard/profile_form.html'
#     model = Profile
#     fields = ['cellphone', 'year', 'make', 'model',
#             'color', 'mg_imei', 'mg_phone', 'emergency_name',
#             'emergency_number', 'sensitivity', 'trip_tracking',
#              'current_location', 'anti_theft']

# class ProfileUpdate(UpdateView):
#     template_name = 'dashboard/profile_form.html'
#     model = Profile
#     fields = ['cellphone', 'year', 'make', 'model',
#             'color', 'mg_imei', 'mg_phone', 'emergency_name',
#             'emergency_number', 'sensitivity', 'trip_tracking',
#              'current_location', 'anti_theft']


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
            return render(request, 'dashboard/devices.html',{'form':f})
    else:
        f = DeviceForm()
    return render(request, 'dashboard/device_form.html', {'form':f})




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



