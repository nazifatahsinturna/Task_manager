
from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login_view, name='login'),
    path('task/', task_view, name='tasks'),
    path('signup/', signup_view, name='signup'),
    path('detail/', detail_view),
    path('logout/', logout_view, name='logout'),
    path('delete/<int:id>', delete_task, name='delete_task')
]
