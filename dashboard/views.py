from django.shortcuts import render
from django.urls import reverse_lazy
from .models import FeedEntry, CitiesForWeather
from .forms import CitiesForWeatherForm
from memory_crystal.models import Memo, Birthday
from overseer.models import Task
from django.core.paginator import Paginator
from currency_mogul.api_utils import show_all_rates
from django.views import generic
from .utils import retrieve_all_tracked_forecasts
from django.contrib import messages
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
    # Tracked citied context
    tracked_cities = CitiesForWeather.objects.all()
    # Weather context
    weather_forecasts = retrieve_all_tracked_forecasts()
    if weather_forecasts is None:
        weather_forecasts = []
    # Form context
    city_form = CitiesForWeatherForm
    # Currency context
    money_dict = show_all_rates()
    # Birthday context
    all_birthdays = Birthday.objects.all().order_by('-bdate')
    context = {
        'all_entries': paged_entries,
        'recent_memos': recent_memos,
        'task_list': task_list,
        'weather_forecasts': weather_forecasts,
        'city_form': city_form,
        'tracked_cities': tracked_cities,
        'money_dict': money_dict,
        'all_birthdays': all_birthdays
    }
    return render(request, 'dashboard/homepage.html', context=context)


class CityForWeatherCreateView(generic.CreateView):
    model = CitiesForWeather
    template_name = 'dashboard/homepage.html'
    success_url = reverse_lazy('homepage')
    form_class = CitiesForWeatherForm

    def form_invalid(self, form, *args, **kwargs):
        messages.error(self.request, 'Location not found.')
        return homepage(self.request)


class CityForWeatherDeleteView(generic.DeleteView):
    model = CitiesForWeather
    template_name = 'dashboard/homepage.html'
    success_url = reverse_lazy('homepage')
