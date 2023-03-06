from django import forms
from .models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['task_text', 'deadline', 'assigned_to_employee', 'assigned_to_team', 'priority', 'estimated_duration',
                  'notes', 'file']
        widgets = {
            'task_text': forms.Textarea(attrs={'class': 'form-control'}),
            'deadline': forms.DateInput(attrs={'type': 'date'}),
            'assigned_to_employee': forms.Select(attrs={'class': 'form-control'}),
            'assigned_to_team': forms.Select(attrs={'class': 'form-control'}),
            'estimated_duration': forms.NumberInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control'}),
            'file': forms.FileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'deadline': 'Дедлайн',
            'assigned_to_employee': 'Выдать сотруднику',
            'assigned_to_team': 'Выдать команде',
            'priority': 'Приоритет',
            'notes': 'Заметки',
            'estimated_duration': 'Предполагаемое время выполнения в сутках',
            'task_text': 'Задание',
            'file': 'Файл',
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
