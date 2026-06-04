from functools import wraps
from django.contrib import messages
from django.shortcuts import redirect

# creating a decorator
def login_required(view_func):
    """
    Custom decorator to require user login for views
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if 'user_id' not in request.session:
            messages.error(request, 'Please login to access this page!')
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper