from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from accounts.models import Emails
from django.http import HttpResponse, HttpResponseRedirect
from django.core.mail import send_mail, EmailMessage
from django.urls import reverse
from .forms import CustomUserCreationForm
from django.contrib import messages



# Create your views here.
def landing(request):
	return render(request,'landing.html')

def index(request):
	return render(request, 'accounts/index.html')

def login(request):
	return(request, 'registration/login.html')

# def register(request):
# 	if request.method == 'POST':
# 		form = UserCreationForm(request.POST)
# 		if form.is_valid():
# 			form.save() #saves information to db
# 			username = form.cleaned_data['username']
# 			password = form.cleaned_data['password1']
# 			user = authenticate(username=username, password=password) #password is hashed
# 			print(user)
# 			login(user)
# 			return HttpResponseRedirect(reverse('login'))
# 	else:
# 		form = UserCreationForm()
# 	context = {'form' : form}
# 	return render(request, 'registration/register.html',context)

def register(request):
    if request.method == 'POST':
        f = CustomUserCreationForm(request.POST)
        if f.is_valid():
            f.save()
            messages.success(request, 'Account created successfully')
            # return redirect('register')
            return HttpResponseRedirect(reverse('login'))

    else:
        f = CustomUserCreationForm()

    return render(request, 'registration/register.html', {'form': f})

def email(request):
	if request.method == 'POST':
		email = request.POST['email']
		#create new Emails object
		Emails.objects.create(
			email = email
			)

		email = EmailMessage('MotoGuardian', 'Thank you for subscribing to our mailing list', to=[email])
		email.send()

		return HttpResponse('')




