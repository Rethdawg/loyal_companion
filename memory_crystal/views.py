from django.db.models import Q
from django.shortcuts import render, redirect, get_list_or_404, reverse
from django.urls import reverse_lazy
from .models import BirthdayNote, Birthday, Memo, Category
from .forms import MemoForm, CategoryForm, BirthdayForm, BirthdayNoteForm, MemoFormSet
from django.contrib import messages
from django.views import generic
from django.views.generic.edit import FormMixin
from django.core.paginator import Paginator
# Create your views here.


def index(request):
    """
    Function responsible for the index view. In case of a POST method saved the contents of a memo form as a new memo.
    :param request: request object
    :return: render of index.html
    """
    if request.method == 'POST':
        form_data = MemoForm(request.POST)
        if form_data.is_valid():
            new_memo = Memo(
                title=form_data.cleaned_data['title'],
                content=form_data.cleaned_data['content'],
            )
            new_memo.save()
            if form_data.cleaned_data['category']:
                new_memo.category.set(form_data.cleaned_data['category'])
            messages.success(request, 'Memo created!')
            return redirect('memo-detail', slug=new_memo.slug)
        else:
            messages.error(request, 'An error had occured.')
            return redirect('memory-index')
    np_form = MemoForm
    recent_memos = Memo.objects.all().order_by('-last_modified')[:5]
    all_categories = Category.objects.all()
    ordered_birthdays = Birthday.objects.all().order_by('bdate')
    context = {
        'recent_memos': recent_memos,
        'all_categories': all_categories,
        'ordered_birthdays': ordered_birthdays,
        'np_form': np_form
    }
    return render(request, 'memory_crystal/index.html', context=context)


class MemoList(generic.ListView):
    """
    Class-based view of all memos, paginated by 4.
    """
    model = Memo
    template_name = 'memo_list.html'
    paginate_by = 4
    queryset = Memo.objects.all().order_by('-pub_date')


def memo_by_category(request, category_name: str):
    """
    Function responsible for the memo by category view. Paginated by 4.
    :param request: request object
    :param category_name: str
    :return: render memo_category.html
    """
    memo_list = get_list_or_404(Memo.objects.filter(category__name__icontains=category_name).order_by('-pub_date'))
    paginator = Paginator(memo_list, 4)
    page_number = request.GET.get('page')
    paged_memos = paginator.get_page(page_number)
    return render(request, 'memory_crystal/memo_category.html', {'memo_list': paged_memos})


class MemoDetailView(generic.DetailView):
    """
    Class-based view responsible for the memo detail view.
    """
    model = Memo
    template_name = 'memory_crystal/memo_detail.html'


class MemoUpdateView(generic.UpdateView):
    """
    Class-based view responsible for viewing the memo update view.
    """
    model = Memo
    success_url = '/notes'
    template_name = 'memory_crystal/memo_update_form.html'
    form_class = MemoForm


class MemoDeleteView(generic.DeleteView):
    """
    Class-based view responsible for the memo delete view. Does not have a template of its own, navigates to the index
    upon success.
    """
    model = Memo
    success_url = reverse_lazy('memory-index')
    template_name = 'memory_crystal/memo_detail.html'


def birthday_list_view(request):
    """
    Function responsible for the birthday view. If the request method is POST, saved a new instance of the Birthday
    model. Upon creation of a birthday redirects to its detail view.
    :param request: request object
    :return: render of birthday_list.html
    """
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
    """
    Class-based view responsible for the birthday detail view. Modified functions allow for a return to the detail view
    upon adding a new BirthdayNote instance.
    """
    model = Birthday
    template_name = 'memory_crystal/birthday_detail.html'
    form_class = BirthdayNoteForm

    def post(self, request, *args, **kwargs):
        """
        Modified form validation
        :param request: request obj
        :param args: args
        :param kwargs: kwargs
        :return: None
        """
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        """
        Modified to automatically provide a foreign key to a new BirthdayNote class.
        :param form:
        :return:
        """
        form.instance.birthday = self.object
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        """
        Modified to redirect back to the Birthday detail view using parent id.
        :return:
        """
        return reverse('birthday-detail', kwargs={'pk': self.object.id})


class BirthdayUpdateView(generic.UpdateView):
    """
    Class-based view of the birthday update view.
    """
    model = Birthday
    form_class = BirthdayForm
    template_name = 'memory_crystal/birthday_update_form.html'

    def get_success_url(self):
        """
        Modified to return to the Birthday insance's detail view using its own id.
        :return: render of birthday_detail.html
        """
        return reverse('birthday-detail', kwargs={'pk': self.get_object().id})


class BirthdayDeleteView(generic.DeleteView):
    """
    Class-based view responsible for the Birthday delete view. Does not have a template of its own, navigates to the
    list of birthdays upon success.
    """
    model = Birthday
    template_name = 'memory_crystal/birthday_detail.html'
    success_url = reverse_lazy('birthdays-all')


class BirthdayNoteUpdateView(generic.UpdateView, FormMixin):
    """
    Class-based view of the BirthdayNote update view.
    """
    model = BirthdayNote
    template_name = 'memory_crystal/birthdaynote_update_form.html'
    form_class = BirthdayNoteForm

    def get_success_url(self):
        """
        Modified to return to the parent's detail view using the parent's id.
        :return:
        """
        return reverse('birthday-detail', kwargs={'pk': self.get_object().birthday.id})


class BirthdayNoteDeleteView(generic.DeleteView):
    """
    Class-based view responsible for the BirthdayNote delete view. Does not have a template of its own, navigates to the
    parent Birthday detail view upon success.
    """
    model = BirthdayNote
    template_name = 'memory_crystal/birthday_detail.html'

    def get_success_url(self):
        """
         Modified to return to the parent's detail view using the parent's id.
         :return:
         """
        return reverse('birthday-detail', kwargs={'pk': self.get_object().id})


class CategoryCreateView(generic.CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'memory_crystal/category_update_form.html'
    success_url = reverse_lazy('memory-index')


class CategoryDeleteView(generic.DeleteView):
    model = Category
    template_name = 'memory_crystal/category_list.html'
    success_url = reverse_lazy('memory-index')


def search(request):
    query_text = request.GET['search_text']
    search_results = Memo.objects.filter(Q(title__icontains=query_text) |
                                         Q(category__name__icontains=query_text)
                                         )
    context = {
        'search_results': search_results,
        'query_text': query_text
    }
    return render(request, 'memory_crystal/search.html', context=context)
