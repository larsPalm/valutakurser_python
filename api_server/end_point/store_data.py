import json
from .models import Currency_value


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
