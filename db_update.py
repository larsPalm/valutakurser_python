import requests
from datetime import date
from dateutil.relativedelta import relativedelta
import pandas as pd
import datetime
import json
from requests.auth import HTTPBasicAuth
import time

def update_values_once():
    # insert data to db at server:
    end_date = date.today()
    start_date = date.today() + relativedelta(months=-1)
    url = "https://data.norges-bank.no/api/data/EXR/B.USD+AUD+BDT+BRL+GBP+BGN+DKK+" \
          "EUR+PHP+HKD+XDR+I44+INR+IDR+TWI+ISK+JPY+CAD+CNY+HRK+MXN+MMK+NZD+ILS+RON+BYN" \
          "+TWD+PKR+PLN+RUB+SGD+CHF+SEK+ZAR+KRW+THB+CZK+TRY+HUF.NOK.SP?format=sdmx-json&" \
          "startPeriod={}&endPeriod={}&locale=no".format(start_date, end_date)
    currencies = []
    api_info = requests.get(url)
    info_json = api_info.json()
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
    map_cur_values = {cur: values for cur, values in zip(base_curs, currencies)}
    # dates
    dates = [elm["id"] for elm in info_json["data"]["structure"]["dimensions"]["observation"][0]["values"]]
    values_per_day ={}
    for index in range(len(dates)):
        vpd = {}
        for key in map_cur_values:
            vpd[key] = map_cur_values[key][index]
        vpd['NOK'] = 1.0000
        values_per_day[dates[index]] = vpd
    print(values_per_day)
    response = requests.get("http://127.0.0.1:8080/dates/")
    json_response = response.json()
    server_dates = json_response['dates']
    for date_val in values_per_day:
        if date_val in server_dates:
            continue
        for cur_val in values_per_day[date_val]:
            data = {
                'value':values_per_day[date_val][cur_val],
                'cur_name':cur_val,
                'dato':date_val
            }
            json_data = json.dumps(data)
            server_url = 'http://127.0.0.1:8080/insert_data/'
            retur = requests.post(server_url, data=json_data)  # ,auth=HTTPBasicAuth(a,b))
            print(retur.status_code, retur.content,date_val)


def update_values_regulary():
    while True:
        update_values_once()
        # timer is the number of seconds in a day
        timer = 60*60*24
        time.sleep(timer)
        print('done waiting')


if __name__ == '__main__':
    update_values_once()
    #update_values_regulary()
