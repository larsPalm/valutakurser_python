from .models import Currency_value, CustomUser
from django.db.models import Max
from .get_stored import *


def validate_a_basecur(name):
    return name in get_bascurs()


def validate_mult(name_list):
    base_curs = get_bascurs()
    for elm in name_list:
        if elm not in name_list:
            return False
    return True
