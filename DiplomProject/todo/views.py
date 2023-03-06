import os
from datetime import timezone
from django.conf import settings

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.urls import reverse
from django.utils import timezone
from django.utils.encoding import smart_str

from .models import TaskExecution, Permissions, TaskHistory
from .forms import TaskForm
from .models import Task, Team, Employee


# Create your views here.

def index(request):
    current_user_id = request.user.id
    emploee = Employee.objects.filter(user_id=current_user_id).first()
    tasksfromemploee = Task.objects.filter(assigned_to_employee=emploee.id).order_by('deadline')

    user_permissions = Permissions.objects.filter(role=emploee.role).first()
    can_create_tasks = user_permissions.can_create if user_permissions else False

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
        'can_create_tasks': can_create_tasks,
    }
    return render(request, 'tasklist.html', context)


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


def completed_tasks(request):
    employee = request.user.employee
    task_executions = TaskExecution.objects.filter(performed_by=employee).order_by('ended_at')
    completed_tasks = [te.task for te in task_executions if te.ended_at is not None]
    context = {'tasks': completed_tasks,
               }
    return render(request, 'CompletedTasks.html', context)


def learn_more(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    task_executions = TaskExecution.objects.filter(task=task)
    is_completed = False
    if task_executions.exists():
        if task_executions[0].ended_at is not None:
            # task is completed, handle accordingly
            is_completed = True
            pass

    history = TaskHistory.objects.filter(task=task).order_by('-timestamp')
    context = {'task': task,
               'is_completed': is_completed,
               'task_executions': task_executions,
               'history': history
               }
    return render(request, 'TaskKnowMore.html', context)


def download_file(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    file_path = os.path.join(settings.MEDIA_ROOT, task.file.name)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/octet-stream")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404


def issued_tasks(request):
    tasks = Task.objects.filter(created_by=request.user.id)
    current_user_id = request.user.id
    employee = Employee.objects.filter(user_id=current_user_id).first()

    task_executions = TaskExecution.objects.all()
    user_permissions = Permissions.objects.filter(role=employee.role).first()
    can_update_tasks = user_permissions.can_update if user_permissions else False

    context = {'tasks': tasks,
               'task_executions': task_executions,
               'can_update_tasks': can_update_tasks,
               }
    return render(request, 'issued_tasks.html', context)


def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST, request.FILES)
        if form.is_valid():
            task = form.save(commit=False)
            task.created_by = request.user
            task.status = "Выдана"
            task.save()
            form.save_m2m()
            TaskHistory.objects.create(task=task, action='Создана', timestamp=timezone.now(), user=request.user)
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
        task.status = 'Завершена'
        task.save()
        TaskHistory.objects.create(task=task, action='Завершена', timestamp=timezone.now(), user=request.user)
        # Redirect to the task detail page
        return HttpResponseRedirect(reverse('todo:learn-more', args=[task_id]))

    context = {'task': task}
    return render(request, 'TaskAccept.html', context)


def return_task(request, task_id):
    task = Task.objects.get(id=task_id)
    task_execution = get_object_or_404(TaskExecution, task_id=task_id)
    task_execution.delete()
    task.status = "Выдана"
    task.save()
    TaskHistory.objects.create(task=task, action='Возвращена', timestamp=timezone.now(), user=request.user)
    return redirect('todo:issued-tasks')


def edit_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            TaskHistory.objects.create(task=task, action='Отредактирована', timestamp=timezone.now(), user=request.user)
            return redirect('todo:issued-tasks')
    else:
        form = TaskForm(instance=task)
    return render(request, 'edit_task.html', {'form': form, 'task': task})
