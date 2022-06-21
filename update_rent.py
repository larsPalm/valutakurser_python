import requests
from datetime import date
from dateutil.relativedelta import relativedelta
import pandas as pd
import datetime
import json


if __name__ == '__main__':
    end_date = date.today()
    start_date = date.today() + relativedelta(months=-13)
    date_info = requests.get("http://127.0.0.1:8080/date_range/").json()
    """end_date = date_info['newest']
    start_date = date_info['oldest']"""
    url = f"https://data.norges-bank.no/api/data/IR/B.NOWA+KPRA..R?format=sdmx-json&startPeriod={start_date}&endPeriod={end_date}&locale=no"
    api_info = requests.get(url).json()
    # raw series data and intial parsing of the api
    rents_info = api_info['data']['dataSets'][0]['series']
    rents_data = []
    teller = 0
    for key in rents_info:
        obs_data = []
        for elm in rents_info[key]['observations']:
            obs_data.append(float(rents_info[key]['observations'][elm][0]))
        rents_data.append(obs_data)
        teller += 1
        if teller == 2:
            break
    for elm in rents_data:
        print(len(elm), elm)
    # dates collected
    dates_info = api_info['data']['structure']['dimensions']['observation'][0]['values']
    dates = [di['name'] for di in dates_info]
    print(dates)
    # info and desc for each rent
    rent_desc = api_info['data']['structure']['dimensions']['series'][1]['values']
    # final parsing and mapping of the data
    rent_ids = [elm['id'] for elm in rent_desc]
    final_rent_info = {}
    for name, ri in zip(rent_ids, rents_data):
        print(len(dates), len(ri))
        final_rent_info[name] = {d: v for d, v in zip(dates, ri)}
        print(name, len(final_rent_info[name].keys()))
    # sending information to the server for storage
    ri_url = "http://127.0.0.1:8080/insert_rent_desc/"
    for elm in rent_desc:
        retur = requests.post(ri_url, data=json.dumps(elm))
        print(retur.status_code, retur.text, elm)
    rd_url = "http://127.0.0.1:8080/insert_rent_data/"
    for key in final_rent_info:
        data = final_rent_info[key]
        for dato in data:
            retur = requests.post(rd_url, data=json.dumps({'name': key,
                                                           'dato': dato,
                                                           'value': data[dato]}))
            print(retur.status_code, retur.text, key)
