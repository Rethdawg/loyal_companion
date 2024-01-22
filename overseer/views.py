from django.shortcuts import render
from django.views import generic
from django.core.paginator import Paginator
from .models import *
# Create your views here.


def index(request):
    if request.method == 'POST':
        pass
    task_list = Task.objects.all()
    ren_task_list = RenewableTask.objects.all()
    context = {
        'task_list': task_list,
        'ren_task_list': ren_task_list
    }
    return render(request, 'overseer/index.html', context=context)

