import os
from datetime import timezone
from django.conf import settings

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.utils import timezone

from .models import Task, TaskExecution
from .forms import TaskForm
from .models import Task, Team, Employee



# Create your views here.

def index(request):
    current_user_id = request.user.id
    emploee = Employee.objects.filter(user_id=current_user_id).first()
    tasksfromemploee = Task.objects.filter(assigned_to_employee=emploee.id)

    taskslist = []
    for task in tasksfromemploee:
        task_executions = TaskExecution.objects.filter(task=task)
        if task_executions.exists():
            if task_executions[0].ended_at is not None:
                # task is completed, handle accordingly
                pass
            else:
                # task is not completed, handle accordingly
                taskslist.append(task)
                pass
        else:
            taskslist.append(task)
            pass
    context = {
        'tasks': taskslist,
        'title': 'Список задач',
    }
    return render(request, 'tasklist.html', context)


def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST, request.FILES)
        if form.is_valid():
            task = form.save(commit=False)
            task.created_by_id = request.user.id
            task.status = "Выдана"
            task.save()
            form.save_m2m()
            return redirect('todo:home')
    else:
        form = TaskForm(initial={'created_by': request.user.id})
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
            started_at=task.created_at,
            ended_at=timezone.now(),
            performed_by=request.user.employee,
            quantitative_indicator=request.POST.get('quantitative_indicator'),
            comments=request.POST.get('comments'),

        )
        if execution.ended_at <= task.deadline:
            execution.on_time = True
        else:
            execution.on_time = False
        execution.save()
        task.status = 'Completed'
        task.save()

        # Redirect to the task detail page
        return HttpResponseRedirect(reverse('todo:learn-more', args=[task_id]))

    context = {'task': task}
    return render(request, 'TaskAccept.html', context)


def learn_more(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    task_executions = TaskExecution.objects.filter(task=task)
    is_completed = False
    if task_executions.exists():
        if task_executions[0].ended_at is not None:
            # task is completed, handle accordingly
            is_completed = True
            pass

    context = {'task': task,
               'is_completed': is_completed,
               'task_executions': task_executions,
               }
    return render(request, 'TaskKnowMore.html', context)


def download_file(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    file_path = os.path.join(settings.MEDIA_ROOT, task.file.name)
    with open(file_path, 'rb') as fh:
        response = HttpResponse(fh.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
        return response

def team_tasks(request):
    employee = request.user.employee
    teams = employee.teams.all()
    tasks = Task.objects.filter(assigned_to_team__in=teams).order_by('deadline')
    taskslist = []
    for task in tasks:
        task_executions = TaskExecution.objects.filter(task=task)
        if task_executions.exists():
            if task_executions[0].ended_at is not None:
                # task is completed, handle accordingly
                pass
            else:
                # task is not completed, handle accordingly
                taskslist.append(task)
                pass
        else:
            taskslist.append(task)
            pass

    context = {
        'tasks': taskslist
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
