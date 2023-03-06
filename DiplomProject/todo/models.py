from django.contrib.auth.models import User
from django.db import models
import datetime


class Role(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название роли')
    description = models.TextField(blank=True, verbose_name='Описание роли')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Роль'
        verbose_name_plural = '5. Роли'


class Permissions(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='permissions')
    can_view = models.BooleanField(default=False, verbose_name='Просмотр')
    can_create = models.BooleanField(default=False, verbose_name='Создание')
    can_update = models.BooleanField(default=False, verbose_name='Редактирование')
    can_delete = models.BooleanField(default=False, verbose_name='Удаление')

    def __str__(self):
        return f'Права доступа {self.role.name}'

    class Meta:
        verbose_name = 'Права доступа'
        verbose_name_plural = '6. Права доступа'


class Team(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название команды')
    leader = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='team_leader', null=True, blank=True,
                               verbose_name='Руководитель команды')
    description = models.TextField(blank=True, verbose_name='Описание команды')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Команда'
        verbose_name_plural = '4. Команды'


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    teams = models.ManyToManyField(Team, blank=True, verbose_name='Команда')
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Роль')
    telegram_chat_id = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = '3. Сотрудники'


class Task(models.Model):
    task_text = models.CharField(max_length=255, verbose_name='Текст задачи')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    deadline = models.DateTimeField(verbose_name='Срок выполнения')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_tasks',
                                   verbose_name='Автор задачи')
    assigned_to_employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='assigned_employee_tasks',
                                             blank=True, null=True, verbose_name='Назначенный сотрудник')
    assigned_to_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='assigned_team_tasks', blank=True,
                                         null=True, verbose_name='Назначенная команда')
    priority = models.PositiveSmallIntegerField(default=0, verbose_name='Приоритет')
    status = models.CharField(max_length=50, default='В процессе', verbose_name='Статус')
    estimated_duration = models.DurationField(null=True, default=datetime.timedelta(days=1), blank=True,
                                              verbose_name='Предполагаемая длительность')
    notes = models.TextField(blank=True, verbose_name='Заметки')
    file = models.FileField(upload_to='task_files/', blank=True, null=True)

    def __str__(self):
        return self.task_text

    class Meta:
        verbose_name = 'Задачу'
        verbose_name_plural = '1. Задачи'


class TaskExecution(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='executions', verbose_name='Задача')
    started_at = models.DateTimeField(verbose_name='Начало выполнения')
    ended_at = models.DateTimeField(verbose_name='Конец выполнения')
    performed_by = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name='Выдана')
    quantitative_indicator = models.FloatField(verbose_name='Процент выполнения')
    comments = models.TextField(blank=True, verbose_name='Комментарии')
    on_time = models.BooleanField(default=True, verbose_name='Вовремя')

    class Meta:
        verbose_name = 'Результат выполнения'
        verbose_name_plural = '2. Результаты выполнения'


class TaskHistory(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, verbose_name='Задача')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    action = models.CharField(max_length=255, verbose_name='Действие')
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Время')

    class Meta:
        verbose_name = 'История задачи'
        verbose_name_plural = '7. Истории задач'
