from django import forms
from .models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['task_text', 'deadline', 'assigned_to_employee', 'assigned_to_team', 'priority', 'estimated_duration',
                  'notes']
        widgets = {
            'deadline': forms.DateInput(attrs={'type': 'date'}),
            'assigned_to_employee': forms.Select(attrs={'class': 'form-control'}),
            'assigned_to_team': forms.Select(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control'}),
            'task_text': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'deadline': 'Дедлайн',
            'assigned_to_employee': 'Выдать сотруднику',
            'assigned_to_team': 'Выдать команде',
            'priority': 'Приоритет',
            'notes': 'Заметки',
            'estimated_duration': 'Предполагаемое время выполнения',
            'task_text': 'Задание',
        }
        help_texts = {
            'deadline': 'Введите дату в формате YYYY-MM-DD',
            'assigned_to_employee': 'Выберите сотрудника',
            'assigned_to_team': 'Выберите команду',
        }
        error_messages = {
            'deadline': {
                'invalid': 'Введите дату в нужном формате: YYYY-MM-DD',
            },
            'assigned_to_employee': {
                'invalid': 'Выберите сотрудника',
                'required': 'Выберите сотрудника',
            },
        }
