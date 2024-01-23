from django.shortcuts import render
from .models import FeedEntry
from memory_crystal.models import Memo
from overseer.models import Task
from django.core.paginator import Paginator
from django.db.models import Q
# Create your views here.


def homepage(request):
    """
    Homepage view function.
    :param request: request object
    :return: template render
    """
    # RSS feed context generation
    all_entries = FeedEntry.objects.all().order_by('-pub_date')[:30]
    paginator = Paginator(all_entries, 6)
    page_number = request.GET.get('page')
    paged_entries = paginator.get_page(page_number)
    # Recent Memo context
    recent_memos = Memo.objects.all().order_by('-last_modified')[:5]
    # To-Do List context
    task_list = [task for task in Task.objects.all() if task.severity == 'danger' or task.severity == 'warning']
    context = {
        'all_entries': paged_entries,
        'recent_memos': recent_memos,
        'task_list': task_list
    }
    return render(request, 'dashboard/homepage.html', context=context)
