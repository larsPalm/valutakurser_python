from time import sleep
from celery import shared_task
from urllib.request import urlopen, Request
import requests
from datetime import date
from dateutil.relativedelta import relativedelta
from .models import Currency_value
import pandas as pd
import datetime

from .models import Currency_value
@shared_task('initial')
def initial():
    print("intitial insertion of data")
    end_date = date.today()
    start_date = date.today() + relativedelta(months=-6)
    url = "https://data.norges-bank.no/api/data/EXR/B.USD+AUD+BDT+BRL+GBP+BGN+DKK+" \
          "EUR+PHP+HKD+XDR+I44+INR+IDR+TWI+ISK+JPY+CAD+CNY+HRK+MXN+MMK+NZD+ILS+RON+BYN" \
          "+TWD+PKR+PLN+RUB+SGD+CHF+SEK+ZAR+KRW+THB+CZK+TRY+HUF.NOK.SP?format=sdmx-json&" \
          "startPeriod={}&endPeriod={}&locale=no".format(start_date, end_date)
    test_url = 'https://data.norges-bank.no/api/data/EXR/B.USD+AUD.NOK.SP?format=sdmx-' \
               'json&startPeriod={}&endPeriod={}&locale=no'.format(start_date, end_date)
    api_info = requests.get(test_url)
    info_json = api_info.json()
    currencies = []
    # extracting the values per currency per day
    for key in info_json["data"]["dataSets"][0]["series"]:
        attributes = info_json["data"]["dataSets"][0]["series"][key]["attributes"]
        cur_dict = info_json["data"]["dataSets"][0]["series"][key]["observations"]
        if (attributes[0] == 1 or attributes[0] == 2 or attributes[0] == 0) and attributes[2] == 1:
            currencies.append([round(float(cur_dict[key][0]) / 100.0, 4) for key in cur_dict])
        else:
            currencies.append([round(float(cur_dict[key][0]), 4) for key in cur_dict])
    #base cur names
    base_curs = [elm["id"] for elm in info_json["data"]["structure"]["dimensions"]["series"][1]["values"]]
    # mapping each list in the nested list to a string value which represent the base_cur
    map_cur_values = {cur: values for cur, values in zip(base_curs, currencies)}
    #dates
    dates = [elm["id"] for elm in info_json["data"]["structure"]["dimensions"]["observation"][0]["values"]]
    for cur in map_cur_values:
        for i in range(len(map_cur_values[cur])):
            Currency_value.objects.create(
                value =map_cur_values[cur][i],
                cur_name = cur,
                dato =dates[i]
            )
            sleep(1)
    pass

@shared_task('update_data')
def update_curency():
    end_date = date.today()
    start_date = date.today() + relativedelta(months=-6)
    url = "https://data.norges-bank.no/api/data/EXR/B.USD+AUD+BDT+BRL+GBP+BGN+DKK+" \
          "EUR+PHP+HKD+XDR+I44+INR+IDR+TWI+ISK+JPY+CAD+CNY+HRK+MXN+MMK+NZD+ILS+RON+BYN" \
          "+TWD+PKR+PLN+RUB+SGD+CHF+SEK+ZAR+KRW+THB+CZK+TRY+HUF.NOK.SP?format=sdmx-json&" \
          "startPeriod={}&endPeriod={}&locale=no".format(start_date, end_date)
    api_info = requests.get(url)
    info_json = api_info.json()
    currencies = []
    # extracting the values per currency per day
    for key in info_json["data"]["dataSets"][0]["series"]:
        attributes = info_json["data"]["dataSets"][0]["series"][key]["attributes"]
        cur_dict = info_json["data"]["dataSets"][0]["series"][key]["observations"]
        if (attributes[0] == 1 or attributes[0] == 2 or attributes[0] == 0) and attributes[2] == 1:
            currencies.append([round(float(cur_dict[key][0]) / 100.0, 4) for key in cur_dict])
        else:
            currencies.append([round(float(cur_dict[key][0]), 4) for key in cur_dict])
    # base cur names
    base_curs = [elm["id"] for elm in info_json["data"]["structure"]["dimensions"]["series"][1]["values"]]
    # mapping each list in the nested list to a string value which represent the base_cur
    map_cur_values = {cur: values for cur, values in zip(base_curs, currencies)}
    # dates
    dates = [elm["id"] for elm in info_json["data"]["structure"]["dimensions"]["observation"][0]["values"]]
    for cur in map_cur_values:
        for i in range(len(map_cur_values[cur])):
            new_data = {'cur_name':cur,'dato':dates[i],'value':map_cur_values[cur][i]}
            Currency_value.objects.update_or_create(
                cur_name=cur,dato=dates[i],
                defaults=new_data
            )
    pass
"""print('hei')
print(Currency_value.objects.all())
if not Currency_value.objects.all():
    initial()
print("hei")
while True:
    sleep(100)
    update_curency()"""
