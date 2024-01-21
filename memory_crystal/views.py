from django.shortcuts import render, redirect, get_list_or_404
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


def memo_by_category(request, category_name):
    memo_list = get_list_or_404(Memo.objects.filter(category__name__icontains=category_name).order_by('-pub_date'))
    paginator = Paginator(memo_list, 4)
    page_number = request.GET.get('page')
    paged_memos = paginator.get_page(page_number)
    return render(request, 'memory_crystal/memo_category.html', {'memo_list': paged_memos})


class MemoDetailView(generic.DetailView):
    model = Memo
    template_name = 'memo_detail.html'


class MemoUpdateView(generic.UpdateView):
    model = Memo
    success_url = '/notes'
    template_name = 'memo_create_form.html'
    form_class = MemoForm


class MemoDeleteView(generic.DeleteView):
    model = Memo
    success_url = '/notes'
    template_name = 'memo_delete.html'


class BirthdayList(generic.ListView):
    model = Birthday
    template_name = 'birthday_list.html'
    queryset = Birthday.objects.all().order_by('-bdate')
