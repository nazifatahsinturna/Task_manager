import re #for email verification

from django.shortcuts import render, redirect
from django.contrib import messages

from task.models import *

regex = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,7}"

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        is_authenticated = False
        try: 
            user = User.objects.get(username=username)
            if user.password == password:
                is_authenticated = True
        except User.DoesNotExist:
            messages.error(request, "Login failed! Invalid username")
        if is_authenticated:
            request.session["user_id"] = user.id
            return redirect('tasks')
        else:
            messages.error(request, "Login failed! Wrong Password")
    return render(request, 'login.html')

def task_view(request):
    return render(request, 'task/index.html')

def signup_view(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        username = request.POST.get("username")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm-password")

        if name is None or name == '':
            messages.error(request, 'You must provide a first name!')
        elif not re.fullmatch(regex, email):
            messages.error(request, 'This is not a valid email address')
        elif password != confirm_password:
            messages.error(request, "Password and Confirm password are different")
        elif User.objects.filter(username=username).exists(): #checking if user not already database
            messages.error(request, 'Username not available')
        elif User.objects.filter(email=email).exists(): #checking if email not already database
            messages.error(request, 'There is already an account with this email')
        else:
            User.objects.create( #saving the user
                name = name,
                email = email,
                username = username,
                password =password
            )
            return redirect('login')
        
    return render(request, 'signup.html')

def detail_view(request):
    return render(request, 'task/details.html')

def logout_view(request):
    request.session.flush()
    messages.success(request, 'Successfully Logged out!!')
    return redirect('login')