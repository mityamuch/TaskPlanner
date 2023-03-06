from django.urls import path
from .views import *

app_name = 'todo'

urlpatterns = [
    path('', index, name='home'),
    path('create/', create_task, name="create"),
    path('accept/<int:task_id>/', accept_task, name='accept'),
    path('learn-more/<int:task_id>/', learn_more, name='learn-more'),
    path('team-tasks/', team_tasks, name='team-tasks'),
    path('issued_tasks/', issued_tasks, name='issued-tasks'),
    path('completed_tasks/', completed_tasks, name='completed_tasks'),
    path('completed_by_team/', completed_by_team, name='completed_by_team'),
    path('learn-more/<int:task_id>/download/', download_file, name='download-file'),
    path('return_task/<int:task_id>/', return_task, name='return-task'),
    path('edit/<int:task_id>/', edit_task, name='edit-task'),
]
