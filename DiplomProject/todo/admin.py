from django.contrib import admin
from django.contrib.admin import AdminSite

from .models import Role, Permissions, Team, Employee, Task, TaskExecution


class PermissionsAdmin(admin.ModelAdmin):
    list_display = ('role', 'can_view', 'can_create', 'can_update', 'can_delete')
    list_filter = ('role', 'can_view', 'can_create', 'can_update', 'can_delete')
    search_fields = ('role__name',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.select_related('role')
        return qs

    def __str__(self):
        return f'Права доступа {self.role.name}'

    class Meta:
        model = Permissions
        verbose_name = 'Права доступа'
        verbose_name_plural = 'Права доступа'


class PermissionsInline(admin.TabularInline):
    model = Permissions


class RoleAdmin(admin.ModelAdmin):
    inlines = [PermissionsInline]
    list_display = ['name', 'description', 'can_view', 'can_create', 'can_update', 'can_delete']

    def can_view(self, obj):
        return ('✓' if obj.permissions.first().can_view else '✗') if obj.permissions.exists() else ''

    can_view.short_description = 'Просмотр'

    def can_create(self, obj):
        return ('✓' if obj.permissions.first().can_create else '✗') if obj.permissions.exists() else ''

    can_create.short_description = 'Создание'

    def can_update(self, obj):
        return ('✓' if obj.permissions.first().can_update else '✗') if obj.permissions.exists() else ''

    can_update.short_description = 'Редактирование'

    def can_delete(self, obj):
        return ('✓' if obj.permissions.first().can_delete else '✗') if obj.permissions.exists() else ''

    can_delete.short_description = 'Удаление'

    class Meta:
        model = Role
        verbose_name = 'Роль'
        verbose_name_plural = 'Роли'


class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'leader', 'description')


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'get_team_name')
    list_filter = ('teams', 'role')

    def get_team_name(self, obj):
        return ', '.join([t.name for t in obj.teams.all()])

    get_team_name.short_description = 'Команда'


class TaskAdmin(admin.ModelAdmin):
    list_display = (
        'task_text', 'created_by', 'assigned_to_employee', 'assigned_to_team', 'status', 'priority', 'deadline')
    list_filter = ('created_at', 'assigned_to_employee', 'assigned_to_team', 'status', 'priority')


class TaskExecutionAdmin(admin.ModelAdmin):
    list_display = ('task', 'started_at', 'ended_at', 'performed_by', 'quantitative_indicator', 'comments', 'on_time')
    list_filter = ('started_at', 'ended_at', 'performed_by', 'on_time')


admin.site.register(Permissions, PermissionsAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(TaskExecution, TaskExecutionAdmin)
admin.site.register(Role, RoleAdmin)
