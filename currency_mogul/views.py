from django.shortcuts import render
from .api_utils import show_historical, show_all_rates, convert_currency
from .utils import clear_graph
from .models import Currency
# Create your views here.


def index(request):
    """
    Function that displays the index page of the app.
    :param request: request object
    :return: index render
    """
    context = {
        'all_currencies': Currency.objects.all()
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
    """
    Function that controls the display of the historical graph page.
    :param request: request object
    :return: renders historical graph
    """
    context = {
        'all_currencies': Currency.objects.all()
    }
    if request.method == 'POST':
        clear_graph()
        from_curr = request.POST['from_curr']
        to_curr = request.POST['to_curr']
        amount = request.POST['amount']
        from_date = request.POST['from_date']
        to_date = request.POST['to_date']
        context.update({
            'from_curr': from_curr,
            'to_curr': to_curr,
            'amount': amount,
            'from_date': from_date,
            'to_date': to_date,
        })
        show_historical(from_date, to_date, from_curr, to_curr, amount)
    return render(request, 'currency_mogul/historical-rates.html', context=context)


def converter(request):
    """
    Function responsible for showing the currency conversion page.
    :param request: request object
    :return: render currency converter page
    """
    context = {
        'all_currencies': Currency.objects.all()
    }
    if request.method == 'POST':
        from_curr = request.POST['from_curr']
        from_amount = request.POST['amount']
        to_curr = request.POST['to_curr']

        context.update({
            'money_dict': convert_currency(from_curr, to_curr, from_amount),
            'from_amount': from_amount,
        })
    return render(request, 'currency_mogul/converter.html', context=context)
