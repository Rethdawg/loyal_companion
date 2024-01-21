from django.shortcuts import render, redirect
from .models import BirthdayNote, Birthday, Memo, Category
from .forms import MemoForm, CategoryForm
from django.contrib import messages
from django.views import generic
from django.http import JsonResponse
from django.core.paginator import Paginator
# Create your views here.


def index(request):
    if request.method == 'POST':
        form_data = MemoForm(request.POST)
        if form_data.is_valid():
            new_memo = Memo(
                title=form_data.cleaned_data['title'],
                content=form_data.cleaned_data['content'],
                status='P'
            )
            new_memo.save()
            new_memo.category.set(form_data.cleaned_data['category'])
            messages.success(request, 'Memo created!')
    np_form = MemoForm
    recent_memos = Memo.objects.all().order_by('-last_modified')[:5]
    all_categories = Category.objects.all()
    all_birthdays = Birthday.objects.all()
    for bd in all_birthdays:
        bd.alert_user(request=request)
    ordered_birthdays = all_birthdays.order_by('bdate')
    context = {
        'recent_memos': recent_memos,
        'all_categories': all_categories,
        'ordered_birthdays': ordered_birthdays,
        'np_form': np_form
    }
    return render(request, 'memory_crystal/index.html', context=context)


class MemoList(generic.ListView):
    model = Memo
    template_name = 'memo_list.html'
    paginate_by = 4
    queryset = Memo.objects.all().order_by('-pub_date')


class MemoDetailView(generic.DetailView):
    model = Memo
    template_name = 'memo_detail.html'
