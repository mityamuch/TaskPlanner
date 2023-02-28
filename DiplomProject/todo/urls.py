from django.urls import path
from .views import *

app_name = 'todo'

urlpatterns = [
    path('', index, name='home'),
    path('create/', create_task, name='create_task'),
]