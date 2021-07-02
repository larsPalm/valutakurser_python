#!/usr/bin/python3
import threading
from multiprocessing import Process
import multiprocessing
import requests
import json
from datetime import date
from dateutil.relativedelta import relativedelta
from atmoicInteger import AtomicInteger


def insert_data(ai_sucess, ai_all):
    end_date = date.today()
    start_date = date.today() + relativedelta(days=-15)
    url = "https://data.norges-bank.no/api/data/EXR/B.USD+AUD+BDT+BRL+GBP+BGN+DKK+" \
          "EUR+PHP+HKD+XDR+I44+INR+IDR+TWI+ISK+JPY+CAD+CNY+HRK+MXN+MMK+NZD+ILS+RON+BYN" \
          "+TWD+PKR+PLN+RUB+SGD+CHF+SEK+ZAR+KRW+THB+CZK+TRY+HUF.NOK.SP?format=sdmx-json&" \
          "startPeriod={}&endPeriod={}&locale=no".format(start_date, end_date)
    test_url = 'https://data.norges-bank.no/api/data/EXR/B.USD+AUD.NOK.SP?format=sdmx-json' \
               '&startPeriod={}&endPeriod={}&locale=no'.format(start_date, end_date)
    #print(test_url)
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
    # base cur names
    base_curs = [elm["id"] for elm in info_json["data"]["structure"]["dimensions"]["series"][1]["values"]]
    # mapping each list in the nested list to a string value which represent the base_cur
    map_cur_values = {cur: values for cur, values in zip(base_curs, currencies)}
    # dates
    dates = [elm["id"] for elm in info_json["data"]["structure"]["dimensions"]["observation"][0]["values"]]
    for cur in map_cur_values:
        for i in range(len(map_cur_values[cur])):
            data = {
                'value': map_cur_values[cur][i],
                'cur_name': cur,
                'dato': dates[i]}
            json_data = json.dumps(data)
            server_url = 'http://127.0.0.1:8080/insert_data/'
            retur = requests.post(server_url, data=json_data)
            if str(retur.content)=="b'success'":
                ai_sucess.increment()
            ai_all.increment()


def get_data(ai_sucess, ai_all):
    for _ in range(10):
        response = requests.get("http://127.0.0.1:8080/get_info/")
        json_response = response.json()
        if str(response.content)!="you should be provided with info, an error has occurred":
            ai_sucess.increment()
        ai_all.increment()


if __name__ == '__main__':
    ai_main = AtomicInteger()
    ai2 = AtomicInteger()
    threads = multiprocessing.cpu_count()
    print(threads)
    muligheter = "1: stresstest henting av data\n" \
                 "2: stresstest pushing av data til server\n" \
                 "3: kombi av 1 og 2"
    try:
        input = int(input(muligheter+": "))
    except:
        input = 0
    if input == 0:
        print("uglydig valg")
    elif input == 1:
        processes = [threading.Thread(target=get_data, args=(ai_main,ai2)) for _ in range(threads)]
        for p in processes:
            p.start()
        for p in processes:
            p.join()
    elif input == 2:
        processes = [threading.Thread(target=insert_data, args=(ai_main,ai2)) for _ in range(threads)]
        for p in processes:
            p.start()
        for p in processes:
            p.join()
    elif input == 3:
        processes = [threading.Thread(target=insert_data, args=(ai_main,ai2)) if x%2==0 else threading.Thread(target=get_data, args=(ai_main,ai2)) for x in range(threads)]
        for p in processes:
            p.start()
        for p in processes:
            p.join()
    print(ai_main.get_value()/ai2.get_value())