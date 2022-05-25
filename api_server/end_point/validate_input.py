from .get_stored import get_bascurs


def validate_a_basecur(name):
    return name in get_bascurs()


def validate_mult(name_list):
    base_curs = get_bascurs()
    for elm in name_list:
        if elm not in base_curs:
            return False
    return True
