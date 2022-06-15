import json
from .models import Currency_value, Rent_value, Rent_info


def data_insert(input_data):
    try:
        data = json.loads(input_data)
        print(data, type(data))
        Currency_value.objects.update_or_create(
            cur_name=data['cur_name'], dato=data['dato'],
            defaults=data
        )
        return "success"
    except:
        return "something bad happened"


def insert_rent_desc(input_data):
    try:
        data = json.loads(input_data)
        print(data, type(data))
        Rent_info.objects.update_or_create(
            id=data['id'], defaults=data
        )
        return "success"
    except:
        return "something bad happened"


def insert_rent_data(input_data):
    try:
        data = json.loads(input_data)
        print(data, type(data))
        Rent_value.objects.update_or_create(
            name=data['name'], dato=data['dato'],
            defaults=data
        )
        return "success"
    except:
        return "something bad happened"
