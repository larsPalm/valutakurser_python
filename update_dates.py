import requests
from datetime import datetime
import pandas as pd
import json


def fix_missing(rent_name, rent_values, the_dates):
    rent_dates = list(rent_values.keys())
    for i in range(1, len(rent_dates)):
        d1 = datetime.strptime(rent_dates[i-1], "%Y-%m-%d")
        d2 = datetime.strptime(rent_dates[i], "%Y-%m-%d")
        if (d2 - d1).days > 1:
            missing_dates = list(pd.date_range(d1, d2).strftime("%Y-%m-%d"))[1:-1]
            print(rent_dates[i-1], rent_dates[i])
            print(missing_dates)
            delta_value = rent_values[rent_dates[i-1]]-rent_values[rent_dates[i]]
            delta_value_day = delta_value/len(missing_dates)
            cur_val = rent_values[rent_dates[i-1]]
            for elm in missing_dates:
                cur_val = cur_val - delta_value_day
                send_update({'name': rent_name, 'dato': elm, 'value': cur_val})
    if rent_dates[-1] != the_dates[-1]:
        d1 = datetime.strptime(rent_dates[-1], "%Y-%m-%d")
        d2 = datetime.strptime(the_dates[-1], "%Y-%m-%d")
        if (d2 - d1).days > 1:
            missing_dates = list(pd.date_range(d1, d2).strftime("%Y-%m-%d"))[1:]
            for elm in missing_dates:
                send_update({'name': rent_name, 'dato': elm, 'value': rent_values[rent_dates[-1]]})


def send_update(data):
    rd_url = "http://127.0.0.1:8080/insert_rent_data/"
    retur = requests.post(rd_url, data=json.dumps(data))
    print(retur.status_code, retur.text)


if __name__ == '__main__':
    url = "http://127.0.0.1:8080/all_rents/"
    api_info = requests.get(url).json()
    rent_info = {key: api_info[key]['values'] for key in api_info}
    dates = requests.get("http://127.0.0.1:8080/dates_rent/").json()
    for elm in rent_info:
        rent_dates = list(rent_info[elm].keys())
        print(len(rent_dates), len(dates))
        print(rent_dates[-1] == dates[-1])
        print(rent_dates[-1], dates[-1])
        print('------')
        fix_missing(elm, rent_info[elm], dates)

