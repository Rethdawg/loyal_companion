from django.contrib import admin
from .models import Task, SubTask
# Register your models here.


class SubTaskInline(admin.TabularInline):
    """
    Class allowing for subtasks to be inline of Task instances in the admin panel.
    """
    model = SubTask


class TaskAdmin(admin.ModelAdmin):
    """
    Class that modifies the display of Task instances and editing in the admin panel.
    """
    search_fields = ('title',)
    readonly_fields = ('id',)
    inlines = (SubTaskInline,)
    list_display = ('id', 'title', 'pub_date', 'due_date')


class SubTaskAdmin(admin.ModelAdmin):
    """
    Class that modifies the display of Subtask instances and editing in the admin panel.
    """
    search_fields = ('title', 'status')
    readonly_fields = ('id',)
    list_display = ('id', 'title', 'pub_date', 'status', 'due_date')


admin.site.register(Task, TaskAdmin)
admin.site.register(SubTask, SubTaskAdmin)
