from django.shortcuts import render
from .models import FeedEntry
from django.core.paginator import Paginator
# Create your views here.


def homepage(request):
    all_entries = FeedEntry.objects.all().order_by('-pub_date')[:30]
    paginator = Paginator(all_entries, 6)
    page_number = request.GET.get('page')
    paged_entries = paginator.get_page(page_number)
    context = {
        'all_entries': paged_entries
    }
    return render(request, 'dashboard/homepage.html', context=context)
