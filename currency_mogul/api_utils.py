# Module containing utilities on calling APIs, as well as their endpoints and keys
import requests as reqs
from .utils import plot_currency
from django.contrib import messages

HOST_FRANKFURTER = "http://api.frankfurter.app"
ENDPOINT = '/latest'
ENDPOINT_CURRENCIES = '/currencies'
all_currencies = reqs.get(HOST_FRANKFURTER + ENDPOINT_CURRENCIES).json()


def show_all_rates(amount: float = 1, from_curr: str = 'EUR') -> dict:
    """
    Retrieves all rates from the frankfurter API. If there is no response, returns an empty dictionary.
    :param amount: float
    :param from_curr: str
    :return: dict
    """
    payload = {
        'amount': amount,
        'from': from_curr
    }
    frankfurter_r = reqs.get(HOST_FRANKFURTER + ENDPOINT, params=payload)
    if frankfurter_r.ok:
        money_dict = frankfurter_r.json()
    else:
        money_dict = {}
    return money_dict


def show_latest_relevant_rates() -> dict:
    """
    Function that fetches all rates via the show_all_rates() command, then retrieves a smaller subset of the data.
    :return: dict
    """
    money_dict = show_all_rates()
    if money_dict:
        relevant_rates = {
            'USD, us dollar': money_dict['rates']['USD'],
            'JPY, japanese yen': money_dict['rates']['JPY'],
            'GBP, pound sterling': money_dict['rates']['GBP'],
            'PLN, polish zloty': money_dict['rates']['PLN'],
            'CNY, chinese yuan renminbi': money_dict['rates']['CNY']
        }
    else:
        relevant_rates = {}
    return relevant_rates


def convert_currency(from_cur: str, to_cur: str, amount: float) -> dict:
    """
    Converts currency via the Frankfurter API.
    :param from_cur: str
    :param to_cur: str
    :param amount: float
    :return: dict
    """
    payload = {
        'from': from_cur,
        'to': to_cur,
        'amount': amount
    }
    frankfurter_r = reqs.get(HOST_FRANKFURTER + ENDPOINT, params=payload)
    if frankfurter_r.ok:
        frankfurter_r = frankfurter_r.json()
        money_dict = {
            'from': frankfurter_r['base'],
            'to': to_cur,
            'amount': frankfurter_r['rates'][to_cur]
        }
    else:
        money_dict = {}
    return money_dict


def show_historical(request, from_time: str, to_time: str, from_cur: str, to_cur: str, amount: float) -> None:
    """
    Receives a set of values and uses them to call the Frankfurter api for historical rates.
    :param request: request obj
    :param from_time: str
    :param to_time: str
    :param from_cur: str
    :param to_cur: str
    :param amount: float
    :return:
    """
    payload = {
        'from': from_cur,
        'to': to_cur,
        'amount': amount
    }
    frankfurter_r = reqs.get(f"{HOST_FRANKFURTER}/{from_time}..{to_time}", params=payload)
    if frankfurter_r.ok:
        historical_dict = frankfurter_r.json()
        plot_currency(historical_dict)
    else:
        messages.error(request, 'Bad response from the API. It is down, or the details you provided'
                                'weren\'t valid.')
