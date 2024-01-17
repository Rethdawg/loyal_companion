from django.shortcuts import render
from .api_utils import *
from .utils import clear_graph

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


def historical_graph(request):
    context = {
        'all_currencies': all_currencies
    }
    if request.method == 'POST':
        clear_graph()
        from_curr = request.POST['from_curr']
        to_curr = request.POST['to_curr']
        amount = request.POST['amount']
        from_date = request.POST['from_date']
        to_date = request.POST['to_date']
        posting = True
        context.update({
            'from_curr': from_curr,
            'to_curr': to_curr,
            'amount': amount,
            'from_date': from_date,
            'to_date': to_date,
            'posting': posting,
        })
        print(context)
        show_historical(from_date, to_date, from_curr, to_curr, amount)
    else:
        posting = False
        context.update(
            {'posting': posting
             })
    return render(request, 'currency_mogul/historical-rates.html', context=context)
