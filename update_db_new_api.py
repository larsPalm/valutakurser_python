import os
import json
import requests
from datetime import date
from dateutil.relativedelta import relativedelta


if __name__ == '__main__':
    payload = {}
    headers = {
        "apikey":  os.getenv('fixer_api_key')
    }
    """date_info = requests.get("http://127.0.0.1:8080/date_range/").json()
    end_date = date_info['newest']"""
    end_date = date.today()
    start_date = date.today() + relativedelta(months=-1)
    url = f"https://api.apilayer.com/fixer/timeseries?start_date={start_date}&end_date={end_date}&base=EUR"
    api_data = requests.request("GET", url, headers=headers, data=payload).json()
    base = api_data['base']
    data = api_data['rates']
    for date in data:
        data_per_day = data[date]
        if date == list(data.keys())[0]:
            print(list(data_per_day.keys()))
        for base in data_per_day:
            base_val = {
                'value': data_per_day[base],
                'cur_name': base,
                'dato': date}
            if base == "USD":
                print(base_val)
            """json_data = json.dumps(base_val)
            server_url = 'http://127.0.0.1:8080/insert_data/'
            retur = requests.post(server_url, data=json_data)
            print(retur.status_code, retur.content)"""

