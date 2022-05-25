from .models import Currency_value, CustomUser
from django.db.models import Max
import datetime
from pandas import DataFrame
import json


def get_all_values():
    try:
        qs = Currency_value.objects.all()
        currency_data = {}
        dates = []
        for info in qs:
            if info.cur_name not in currency_data.keys():
                currency_data[info.cur_name] = {}
            if info.dato not in dates:
                dates.append(info.dato)
            currency_data[info.cur_name][info.dato] = info.value
        df = DataFrame(currency_data, index=dates)
        df = df.sort_index()
        df.index.name = 'dates'
        return df.to_json(orient='index')
    except:
        print('something wrong happened')
        return {}


def get_all_values_v2():
    """
    Alternative to get_all_values(), not as good as get_all_values()
    :return:
    """
    try:
        qs = Currency_value.objects.all()
        currencies = {}
        dates = []
        names = []
        for info in qs:
            if info.cur_name not in names:
                currencies[info.cur_name] = []
                names.append(info.cur_name)
            if info.dato not in dates:
                dates.append(info.dato)
            currencies[info.cur_name].append(info.value)
        data = dict()
        data['currencies'] = currencies
        data['dates'] = dates
        json_data = json.dumps(data)
        return json_data
    except:
        print('something wrong happened')
        return {}


def get_bascurs():
    sql_response = Currency_value.objects.values('cur_name').distinct()
    base_curs = []
    for elm in sql_response:
        base_curs.append(elm['cur_name'])
    return base_curs


def get_a_cur(name):
    dates = get_dates()
    return [Currency_value.objects.get(dato=date, cur_name=name).value for date in dates]


def get_newest_for_a_cur(name):
    max_year = Currency_value.objects.all().aggregate(Max('dato'))['dato__max']
    return Currency_value.objects.get(dato=max_year, cur_name=name).value


def convert_between(cur1, cur2, ammount):
    c1 = get_newest_for_a_cur(cur1)
    c2 = get_newest_for_a_cur(cur2)
    return round((c1/c2)*ammount, 2)


def get_newest_for_all():
    bases = get_bascurs()
    data = {}
    for base in bases:
        data[base] = get_newest_for_a_cur(base)
    return data


def newest_date():
    return Currency_value.objects.all().aggregate(Max('dato'))['dato__max']


def get_dates():
    date_dict = Currency_value.objects.values('dato').distinct()
    return [elm['dato'] for elm in date_dict]


def get_mult_curs_with_dates(base, name_list):
    dates = get_dates()
    base_cur_value = [Currency_value.objects.get(dato=date, cur_name=base).value for date in dates]
    values = {}
    date_obj = [datetime.datetime.strptime(d, "%Y-%m-%d").date() for d in dates]
    for elm in name_list:
        cur_val = [Currency_value.objects.get(dato=date, cur_name=elm).value for date in dates]
        values[elm] = [round(y1 / y2, 4) for y1, y2 in zip(cur_val, base_cur_value)]
    title = f'{base} vs '
    for elm in values:
        title += elm
        if elm != name_list[-1]:
            title += ', '
    max_val, min_val = -100, -100
    for key in values:
        for elm in values[key]:
            if max_val < elm:
                max_val = elm
            if min_val < 0:
                min_val = elm
            elif min_val > 0 and min_val > elm:
                min_val = elm
    return values, date_obj, title, min_val, max_val


def compare_2_cur(from_cur, to_cur):
    datoer = get_dates()
    cur1_values = [Currency_value.objects.get(dato=date, cur_name=from_cur).value for date in datoer]
    cur2_values = [Currency_value.objects.get(dato=date, cur_name=to_cur).value for date in datoer]
    graph_value = [round(v1 / v2, 4) for v1, v2 in zip(cur1_values, cur2_values)]
    x_values = [datetime.datetime.strptime(d, "%Y-%m-%d").date() for d in datoer]
    return graph_value, x_values
