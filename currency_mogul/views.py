from django.shortcuts import render
from .api_utils import *

# Create your views here.


def index(request):
    context = {
        'all_currencies': all_currencies
    }
    if request.method == 'POST':
        amount = request.POST['from_amount']
        from_curr = request.POST['from_curr']
        context.update({
            'money_dict': show_all_rates(amount, from_curr)
        })
    else:
        context.update({
            'money_dict': show_all_rates()
        })
    return render(request, 'currency_mogul/index.html', context=context)
