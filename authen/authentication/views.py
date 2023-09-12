from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.core.mail import send_mail, EmailMessage
from login import settings
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str

# Create your views here.
def home(request):
    return render(request, 'authentication/index.html')

def signup(request):
    if request.method == "POST":
        username = request.POST.get('username')
        first_name = request.POST.get('fname')
        last_name = request.POST.get('lname')
        email = request.POST.get('email')
        password = request.POST.get('pass')
        confirm_password = request.POST.get('pass1')

        if User.objects.filter(username=username):
            messages.error(request, "USERNAME ALREADY TAKEN")
            return redirect('signup')
        if User.objects.filter(email=email):
            messages.error(request, "EMAIL EXISTS")
            return redirect('signup')
        if len(username)>10:
            messages.error(request, "username too long")
            return redirect('signup')
        if password != confirm_password:
            messages.error(request, "PASSWORD DOES NOT MATCH")
            return redirect('signup')

        my_user = User.objects.create_user(username=username, email=email, password=password)
        my_user.is_active = True
        my_user.first_name = first_name
        my_user.last_name = last_name
        my_user.save()
        return redirect('signin')
    return render(request, 'authentication/signup.html')

def signin(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('pass')

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            first_name = user.first_name

            return render(request, 'authentication/index.html', {'fname': first_name})
        else:
            messages.error(request, "username or password")
            return HttpResponse("invalid input")
            
    

    return render(request, 'authentication/signin.html')

def signout(request):
    logout(request)
    messages.success(request, "logged out")
    return render(request, 'authentication/index.html')

