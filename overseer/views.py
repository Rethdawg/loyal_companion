from django.shortcuts import render, reverse
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from .forms import TaskForm, SubtaskForm
from .models import Task, SubTask
from django.views import generic
from django.views.generic.edit import FormMixin
# Create your views here.


def index(request):
    if request.method == 'POST':
        query_text = request.POST['search_text']
        task_list = Task.objects.filter(title__icontains=query_text)
    else:
        task_list = Task.objects.all()
        # ren_task_list = RenewableTask.objects.all()
    paginator = Paginator(task_list, 4)
    page_number = request.GET.get('page')
    paged_tasks = paginator.get_page(page_number)
    context = {
        'task_list': paged_tasks,
    }
    return render(request, 'overseer/index.html', context=context)


class TaskDetailView(generic.DetailView, FormMixin):
    model = Task
    template_name = 'overseer/task_detail.html'
    form_class = SubtaskForm

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.instance.main_task = self.object
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('task-detail', kwargs={'pk': self.object.id})


class TaskCreateView(generic.CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'overseer/task_update_form.html'

    def get_success_url(self):
        return reverse('task-detail', kwargs={'pk': self.object.id})


class TaskUpdateView(generic.UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'overseer/task_update_form.html'

    def get_success_url(self):
        return reverse('task-edit', kwargs={'pk': self.object.id})


class TaskDeleteView(generic.DeleteView):
    model = Task
    template_name = 'overseer/task_detail.html'
    success_url = reverse_lazy('overseer-index')


class SubtaskCreateView(generic.CreateView):
    model = SubTask
    template_name = 'overseer/subtask_update_form.html'
    form_class = SubtaskForm

    def get_success_url(self):
        return reverse('task-detail', kwargs={'pk': self.object.main_task.id})


class SubtaskUpdateView(generic.UpdateView):
    model = SubTask
    template_name = 'overseer/subtask_update_form.html'
    form_class = SubtaskForm

    def get_success_url(self):
        return reverse('task-detail', kwargs={'pk': self.object.main_task.id})


class SubtaskDeleteView(generic.DeleteView):
    model = SubTask
    template_name = 'overseer/task_detail.html'

    def get_success_url(self):
        return reverse('task-detail', kwargs={'pk': self.object.main_task.id})
