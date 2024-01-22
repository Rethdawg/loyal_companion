from django.shortcuts import render, redirect, get_list_or_404, reverse
from django.urls import reverse_lazy

from .models import BirthdayNote, Birthday, Memo, Category
from .forms import MemoForm, CategoryForm, BirthdayForm, BirthdayNoteForm
from django.contrib import messages
from django.views import generic
from django.views.generic.edit import FormMixin
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
            redirect('memo-detail', slug=new_memo.slug)
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
    template_name = 'memory_crystal/memo_detail.html'


class MemoUpdateView(generic.UpdateView):
    model = Memo
    success_url = '/notes'
    template_name = 'memory_crystal/memo_update_form.html'
    form_class = MemoForm


class MemoDeleteView(generic.DeleteView):
    model = Memo
    success_url = reverse_lazy('memory-index')
    template_name = 'memory_crystal/memo_detail.html'


def birthday_list_view(request):
    if request.method == 'POST':
        form_data = BirthdayForm(request.POST)
        if form_data.is_valid():
            new_birthday = Birthday(
                person=form_data.cleaned_data['person'],
                bdate=form_data.cleaned_data['bdate']
            )
            new_birthday.save()
            messages.success(request, 'Birthday created!')
            return redirect('birthday-detail', pk=new_birthday.id)
    bd_form = BirthdayForm
    birthday_list = Birthday.objects.all().order_by('bdate')
    context = {
        'bd_form': bd_form,
        'birthday_list': birthday_list
    }
    return render(request, 'memory_crystal/birthday_list.html', context=context)


class BirthdayDetailView(generic.DetailView, FormMixin):
    model = Birthday
    template_name = 'memory_crystal/birthday_detail.html'
    form_class = BirthdayNoteForm

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.instance.birthday = self.object
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('birthday-detail', kwargs={'pk': self.object.id})


class BirthdayUpdateView(generic.UpdateView):
    model = Birthday
    form_class = BirthdayForm
    template_name = 'memory_crystal/birthday_update_form.html'

    def get_success_url(self):
        return reverse('birthday-detail', kwargs={'pk': self.get_object().id})


class BirthdayDeleteView(generic.DeleteView):
    model = Birthday
    template_name = 'memory_crystal/birthday_detail.html'
    success_url = reverse_lazy('birthdays-all')


class BirthdayNoteUpdateView(generic.UpdateView, FormMixin):
    model = BirthdayNote
    template_name = 'memory_crystal/birthdaynote_update_form.html'
    form_class = BirthdayNoteForm

    def get_success_url(self):
        return reverse('birthday-detail', kwargs={'pk': self.get_object().birthday.id})


class BirthdayNoteDeleteView(generic.DeleteView):
    model = BirthdayNote
    template_name = 'memory_crystal/birthday_detail.html'

    def get_success_url(self):
        return reverse('birthday-detail', kwargs={'pk': self.get_object().id})
