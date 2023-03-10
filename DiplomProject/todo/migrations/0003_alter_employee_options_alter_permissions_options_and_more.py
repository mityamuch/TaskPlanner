# Generated by Django 4.1.5 on 2023-03-04 22:33

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('todo', '0002_remove_team_role'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='employee',
            options={'verbose_name': 'Сотрудник', 'verbose_name_plural': '3. Сотрудники'},
        ),
        migrations.AlterModelOptions(
            name='permissions',
            options={'verbose_name': 'Права доступа', 'verbose_name_plural': '6. Права доступа'},
        ),
        migrations.AlterModelOptions(
            name='role',
            options={'verbose_name': 'Роль', 'verbose_name_plural': '5. Роли'},
        ),
        migrations.AlterModelOptions(
            name='task',
            options={'verbose_name': 'Задачу', 'verbose_name_plural': '1. Задачи'},
        ),
        migrations.AlterModelOptions(
            name='taskexecution',
            options={'verbose_name': 'Результат выполнения', 'verbose_name_plural': '2. Результаты выполнения'},
        ),
        migrations.AlterModelOptions(
            name='team',
            options={'verbose_name': 'Команда', 'verbose_name_plural': '4. Команды'},
        ),
        migrations.AddField(
            model_name='task',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='task_files/'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='role',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='todo.role', verbose_name='Роль'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='teams',
            field=models.ManyToManyField(blank=True, to='todo.team', verbose_name='Команда'),
        ),
        migrations.AlterField(
            model_name='permissions',
            name='can_create',
            field=models.BooleanField(default=False, verbose_name='Создание'),
        ),
        migrations.AlterField(
            model_name='permissions',
            name='can_delete',
            field=models.BooleanField(default=False, verbose_name='Удаление'),
        ),
        migrations.AlterField(
            model_name='permissions',
            name='can_update',
            field=models.BooleanField(default=False, verbose_name='Редактирование'),
        ),
        migrations.AlterField(
            model_name='permissions',
            name='can_view',
            field=models.BooleanField(default=False, verbose_name='Просмотр'),
        ),
        migrations.AlterField(
            model_name='role',
            name='description',
            field=models.TextField(blank=True, verbose_name='Описание роли'),
        ),
        migrations.AlterField(
            model_name='role',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Название роли'),
        ),
        migrations.AlterField(
            model_name='task',
            name='assigned_to_employee',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='assigned_employee_tasks', to='todo.employee', verbose_name='Назначенный сотрудник'),
        ),
        migrations.AlterField(
            model_name='task',
            name='assigned_to_team',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='assigned_team_tasks', to='todo.team', verbose_name='Назначенная команда'),
        ),
        migrations.AlterField(
            model_name='task',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата создания'),
        ),
        migrations.AlterField(
            model_name='task',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_tasks', to=settings.AUTH_USER_MODEL, verbose_name='Автор задачи'),
        ),
        migrations.AlterField(
            model_name='task',
            name='deadline',
            field=models.DateTimeField(verbose_name='Срок выполнения'),
        ),
        migrations.AlterField(
            model_name='task',
            name='estimated_duration',
            field=models.DurationField(blank=True, default=datetime.timedelta(days=1), null=True, verbose_name='Предполагаемая длительность'),
        ),
        migrations.AlterField(
            model_name='task',
            name='notes',
            field=models.TextField(blank=True, verbose_name='Заметки'),
        ),
        migrations.AlterField(
            model_name='task',
            name='priority',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='Приоритет'),
        ),
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.CharField(default='В процессе', max_length=50, verbose_name='Статус'),
        ),
        migrations.AlterField(
            model_name='task',
            name='task_text',
            field=models.CharField(max_length=255, verbose_name='Текст задачи'),
        ),
        migrations.AlterField(
            model_name='taskexecution',
            name='comments',
            field=models.TextField(blank=True, verbose_name='Комментарии'),
        ),
        migrations.AlterField(
            model_name='taskexecution',
            name='ended_at',
            field=models.DateTimeField(verbose_name='Конец выполнения'),
        ),
        migrations.AlterField(
            model_name='taskexecution',
            name='on_time',
            field=models.BooleanField(default=True, verbose_name='Вовремя'),
        ),
        migrations.AlterField(
            model_name='taskexecution',
            name='performed_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='todo.employee', verbose_name='Выдана'),
        ),
        migrations.AlterField(
            model_name='taskexecution',
            name='quantitative_indicator',
            field=models.FloatField(verbose_name='Процент выполнения'),
        ),
        migrations.AlterField(
            model_name='taskexecution',
            name='started_at',
            field=models.DateTimeField(verbose_name='Начало выполнения'),
        ),
        migrations.AlterField(
            model_name='taskexecution',
            name='task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='executions', to='todo.task', verbose_name='Задача'),
        ),
        migrations.AlterField(
            model_name='team',
            name='description',
            field=models.TextField(blank=True, verbose_name='Описание команды'),
        ),
        migrations.AlterField(
            model_name='team',
            name='leader',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='team_leader', to=settings.AUTH_USER_MODEL, verbose_name='Руководитель команды'),
        ),
        migrations.AlterField(
            model_name='team',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Название команды'),
        ),
    ]
