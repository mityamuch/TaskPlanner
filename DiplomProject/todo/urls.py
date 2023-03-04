from django.urls import path
from .views import *

app_name = 'todo'

urlpatterns = [
    path('', index, name='home'),
    path('create/', create_task, name="create"),
    path('accept/<int:task_id>/', accept_task, name='accept'),
    path('learn-more/<int:task_id>/', learn_more, name='learn-more'),
    path('team-tasks/', team_tasks, name='team-tasks'),
    path('completed_tasks/', completed_tasks, name='completed_tasks'),
    path('completed_by_team/', completed_by_team, name='completed_by_team'),
]
