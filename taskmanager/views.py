from django.shortcuts import render, redirect

def login_view(request):
    return render(request, 'login.html')

def task_view(request):
    return render(request, 'task/index.html')

def signup_view(request):
    return render(request, 'signup.html')

def detail_view(request):
    return render(request, 'task/details.html')