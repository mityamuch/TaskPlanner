from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.utils.datetime_safe import datetime

from .models import Task, TaskExecution

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


def accept_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)

    # Check if the user is authorized to accept the task
    # if request.user.employee != task.assigned_to_employee:
    #     return HttpResponseRedirect(reverse('tasklist'))

    if request.method == 'POST':
        # Create a new task execution instance
        execution = TaskExecution(
            task=task,
            started_at=datetime.now(),
            performed_by=request.user.employee,
            quantitative_indicator=0.0,
        )
        execution.save()

        # Redirect to the task detail page
        return HttpResponseRedirect(reverse('todo:learn_more', args=[task_id]))

    context = {'task': task}
    return render(request, 'TaskAccept.html', context)


def learn_more(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    return render(request, 'TaskKnowMore.html', {'task': task})


def team_tasks(request):
    employee = request.user.employee
    teams = employee.teams.all()
    tasks = Task.objects.filter(assigned_to_team__in=teams).order_by('deadline')
    context = {
        'tasks': tasks
    }
    return render(request, 'TeamTaskList.html', context)


def completed_tasks(request):
    employee = request.user.employee
    task_executions = TaskExecution.objects.filter(performed_by=employee)
    completed_tasks = [te.task for te in task_executions if te.ended_at is not None]
    context = {'tasks': completed_tasks}
    return render(request, 'CompletedTasks.html', context)


def completed_by_team(request):
    # Get the current user's employee object
    employee = request.user.employee

    # Get the teams that the current user is a leader of
    team_leadership = Team.objects.filter(leader=employee)

    # Get the completed tasks for each team that the current user is a leader of
    completed_by_team_tasks = []
    for team in team_leadership:
        tasks = Task.objects.filter(assigned_to_team=team,
                                    executions__performed_by__in=team.employee_set.all()).distinct()
        completed_by_team_tasks.extend([task for task in tasks if
                                        task.executions.last().performed_by in team.employee_set.all() and task.executions.last().ended_at is not None])

    # Get the completed tasks for the current user that are not assigned to a team they lead
    other_completed_tasks = Task.objects.filter(executions__performed_by=employee).exclude(
        assigned_to_team__leader=employee).distinct()

    # Render the completed by team tasks template with the data
    return render(request, 'completed_by_team.html', {
        'completed_by_team_tasks': completed_by_team_tasks,
        'other_completed_tasks': other_completed_tasks,
        'team': team
    })
