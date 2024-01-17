# Module containing utilities on calling APIs, as well as their endpoints and keys
import requests as reqs
from .utils import plot_currency

HOST_FRANKFURTER = "http://api.frankfurter.app"
ENDPOINT = '/latest'
ENDPOINT_CURRENCIES = '/currencies'
all_currencies = reqs.get(HOST_FRANKFURTER + ENDPOINT_CURRENCIES).json()


def show_all_rates(amount=1, from_curr='EUR'):
    payload = {
        'amount': amount,
        'from': from_curr
    }
    frankfurter_r = reqs.get(HOST_FRANKFURTER + ENDPOINT, params=payload)
    if frankfurter_r.ok:
        money_dict = frankfurter_r.json()
    else:
        money_dict = None
    return money_dict


def show_latest_relevant_rates():
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
        relevant_rates = None
    return relevant_rates


def convert_currency(from_cur, to_cur, amount):
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
        money_dict = None
    return money_dict


def show_historical(from_time, to_time, from_cur, to_cur):
    payload = {
        'from': from_cur,
        'to': to_cur
    }
    frankfurter_r = reqs.get(f"{HOST_FRANKFURTER}/{from_time}..{to_time}", params=payload)
    if frankfurter_r.ok:
        historical_dict = frankfurter_r.json()
        plot_currency(historical_dict)
