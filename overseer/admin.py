from django.contrib import admin
from .models import Task, SubTask
# Register your models here.


class SubTaskInline(admin.TabularInline):
    model = SubTask


class TaskAdmin(admin.ModelAdmin):
    search_fields = ('title',)
    readonly_fields = ('id',)
    inlines = (SubTaskInline,)
    list_display = ('id', 'title', 'pub_date', 'due_date')


class SubTaskAdmin(admin.ModelAdmin):
    search_fields = ('title', 'status')
    readonly_fields = ('id',)
    list_display = ('id', 'title', 'pub_date', 'status', 'due_date')


admin.site.register(Task, TaskAdmin)
admin.site.register(SubTask, SubTaskAdmin)
