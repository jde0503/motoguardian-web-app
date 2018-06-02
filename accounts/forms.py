# from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Device
from django.core.exceptions import ValidationError
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
    )
from django.forms import ModelForm
from django.utils.text import slugify


class CustomUserCreationForm(forms.Form):
    username = forms.CharField(label='Username', min_length=4, max_length=150)
    first_name = forms.CharField(label='First Name', min_length=2, max_length=150)
    last_name = forms.CharField(label='Last Name', min_length=2, max_length=150)
    email = forms.EmailField(label='Email')
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)
    #phone_number for arduino
    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        r = User.objects.filter(username=username)
        if r.count():
            raise  ValidationError("Username already exists")
        return username

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        r = User.objects.filter(email=email)
        if r.count():
            raise  ValidationError("Email already exists")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match!")

        return password2

    def save(self, commit=True):
        user = User.objects.create_user(
            self.cleaned_data['username'],
            self.cleaned_data['email'],
            self.cleaned_data['password1'],
            first_name = self.cleaned_data['first_name'].capitalize(),
            last_name = self.cleaned_data['last_name'].capitalize()
        )
        return user
    # class Meta:
    #     model = User
    #     fields = ['Username', 'First Name', 'Last Name','Email', 'Password', 'Re-enter Password']

class DeviceForm(ModelForm):
    # mg_imei = forms.CharField(label='IMEI', min_length=4, max_length=150)
    class Meta:
        model = Device
        
        fields = ['first_name','last_name','cellphone','mg_imei','mg_phone','year','make',
        'model','color','emergency_name','emergency_number',
        'sensitivity','trip_tracking','anti_theft']
        
        labels = {
            'first_name': 'First Name',
            'last_name':'Last Name',
            'cellphone':'Cellphone Number',
            'mg_imei':'IMEI',
            'mg_phone':'MotoGuardian Phone Number',
            'make': 'Make',
            'model': 'Model',
            'year': 'Year',
            'color':'Color',
            'emergency_name': 'Emergency Contact Name',
            'emergency_number':'Emergency Contact Phone Number',
            'sensitivity':'Sensitivity',
            'trip_tracking':'Trip Tracking',
            'anti_theft':'Alarm',
        }

        help_texts = {
            'mg_imei':'(International Mobile Equipment Identity)',
            'sensitivity':'(1-10)',
            'trip_tracking':'Check to enable this feature',
            'anti_theft':'Check to enable this feature',
        }

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'cellphone': forms.TextInput(attrs={'class': 'form-control'}),
            'mg_imei': forms.TextInput(attrs={'class': 'form-control'}),
            'mg_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'mg_imei': forms.TextInput(attrs={'class': 'form-control'}),
            'mg_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'make': forms.TextInput(attrs={'class': 'form-control'}),
            'model': forms.TextInput(attrs={'class': 'form-control'}),
            'year': forms.TextInput(attrs={'class': 'form-control'}),
            'emergency_name': forms.TextInput(attrs={'class': 'form-control'}),
            'emergency_number': forms.TextInput(attrs={'class': 'form-control'}),
            'color': forms.TextInput(attrs={'class': 'form-control'}),
            'sensitivity': forms.TextInput(attrs={'class': 'form-control'}),
        }

        error_messages = {
                    'mg_imei': {
                        'unique': ("This IMEI is already registered"),
                    },
                    'mg_phone': {
                        'unique': ("This phone number is already registered"),
                    },
                }




