import re #for email verification

from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q #for searching

from task.models import *
from .utils import login_required

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

@login_required
def task_view(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        priority = request.POST.get('priority')
        due_date = request.POST.get('due')
        description = request.POST.get('description')
        if title is None or title == 'title':
            messages.error(request, 'You must provide a title for your task')
        else:
            user_id = request.session.get("user_id")
            user = User.objects.get(id = user_id)
            Task.objects.create(
                title = title,
                priority = priority,
                due_date = due_date,
                description = description,
                owner = user
            )
    
    user_id = request.session.get("user_id")
    user = User.objects.get(id = user_id)
    
    tasks = user.tasks.all() #select # from tasks where user_id = user.id
    # print(tasks)
    search = request.GET.get("search")
    if search:
        tasks = tasks.filter(
            Q(title__icontains=search) |
            Q(description__icontains=search)
        )


    return render(request, 'task/index.html', {"tasks": tasks, "search": search})

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

@login_required
def detail_view(request, id):
    if request.method == 'POST':
        status = request.POST.get("status")
        task = Task.objects.get(id=id)
        task.status = status
        task.save()
        return redirect('task_detail', id=id)
    task = Task.objects.get(id=id)
    return render(request, 'task/details.html', {'task': task})

@login_required
def logout_view(request):
    request.session.flush()
    messages.success(request, 'Successfully Logged out!!')
    return redirect('login')


def delete_task(request, id):
    task = Task.objects.get(id=id)
    task.delete()
    return redirect('tasks')