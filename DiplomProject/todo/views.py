from django.shortcuts import render, redirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.http import HttpResponse

from .forms import TaskForm
from .models import Task, Team, Employee
from .models import Employee


# Create your views here.

def index(request):
    current_user_id = request.user.id
    # current_team_id = Employee.objects.get(user_id=current_user_id).team_id
    emploee = Employee.objects.filter(user_id=current_user_id).first()
    # emploeeteams = Team.objects.filter(team_id=emploee.teams.id)
    # tasksteams =()
    # for team in emploeeteams:
    # tasksfromteam = Task.objects.filter(assigned_to_team=team.id)
    # tasksteams = tasksteams + tasksfromteam

    tasksfromemploee = Task.objects.filter(assigned_to_employee=emploee.id)

    # in_first = set(tasksfromteam)
    # in_second = set(tasksfromemploee)

    context = {
        'tasks': tasksfromemploee,
        'title': 'Список задач',
    }
    return render(request, 'tasklist.html', context)


def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tasklist')
    else:
        form = TaskForm()
    return render(request, 'task_form.html', {'form': form})
