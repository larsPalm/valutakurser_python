from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.decorators import api_view
import json
import base64
from .get_stored import get_all_values, convert_between, newest_date, \
    get_newest_for_all, get_mult_curs_with_dates, get_bascurs, get_dates, get_dates_rent, compare_2_cur
from .get_stored import get_all_rent_info, get_ids_rent, get_one_rent, get_oldest_newest, get_oldest_newest_rent
from .validate_input import validate_a_basecur
from .make_plot import make_plotly_plot_mult, plot_compare_2_cur, plot_compare_2_cur_mm, \
    get_mult__with_dates, make_matplot_plot_mult, plot_rents, plot_rent_vs_nok
from .store_data import data_insert, insert_rent_data, insert_rent_desc


def index(request):
    return render(request, "home.html")


@api_view(['GET'])
def get_info(request):
    base_curs = get_bascurs()
    return HttpResponse(json.dumps({'created by': {'name': 'Lars Palm',
                                                   'Gtihub': 'https://github.com/larsPalm',
                                                   'Country': 'Kolbotn,Norway',
                                                   'When': 'Summer 2021'},
                                    'info': ['list of our supported currencies',
                                             'made just for fun, not professional',
                                             'Some values may be incorrect due to the shitty api of Norges Bank'],
                                    'url for data': 'http://127.0.0.1:8080/get_info/',
                                    'supported currencies': base_curs}))


@api_view(['POST'])
def insert_data(request):
    return HttpResponse(data_insert(request.body))


@api_view(['GET'])
def get_currency(request):
    return HttpResponse(get_all_values(), content_type='application/json')


def convert(request):
    base_curs = get_bascurs()
    if request.POST:
        from_cur = request.POST['from_cur']
        to_cur = request.POST['to_cur']
        ammount_string = request.POST['quantity']
        if not validate_a_basecur(from_cur) or not validate_a_basecur(to_cur):
            return render(request, 'convert.html', {'bases': base_curs, 'message': 'invalid input'})
        try:
            ammount = float(ammount_string)
        except:
            return render(request, 'convert.html', {'bases': base_curs, 'message': 'invalid input'})
        if from_cur == to_cur:
            msg = f'{ammount} {from_cur} = {ammount} {to_cur}'
            return render(request, 'convert.html', {'bases': base_curs, 'message': msg, 'extra': 'same currency!!'})
        msg = f'{ammount} {from_cur} = {convert_between(from_cur, to_cur, ammount)} {to_cur}'
        return render(request, 'convert.html', {'bases': base_curs, 'message': msg})
    return render(request, 'convert.html', {'bases': base_curs})


def compare(request):
    base_curs = get_bascurs()
    if request.POST:
        to_cur = request.POST['to_cur']
        from_cur = request.POST['from_cur']
        if not validate_a_basecur(request.POST['to_cur']) or not validate_a_basecur(request.POST['from_cur']):
            return render(request, 'compare.html', {'bases': base_curs, 'msg': 'invalid input'})
        else:
            return render(request, 'compare.html', {'bases': base_curs,
                                                    'plot_div': plot_compare_2_cur(from_cur, to_cur),
                                                    'cur_from': from_cur,
                                                    'cur_to': to_cur})
    return render(request, 'compare.html', {'bases': base_curs})


def compare_mm(request):
    base_curs = get_bascurs()
    if request.POST:
        to_cur = request.POST['to_cur']
        from_cur = request.POST['from_cur']
        if not validate_a_basecur(request.POST['to_cur']) or not validate_a_basecur(request.POST['from_cur']):
            return render(request, 'compareMM.html', {'bases': base_curs, 'msg': 'invalid input'})
        else:
            return render(request, 'compareMM.html', {'bases': base_curs,
                                                      'plot_div': plot_compare_2_cur_mm(from_cur, to_cur),
                                                      'cur_from': from_cur,
                                                      'cur_to': to_cur})
    return render(request, 'compareMM.html', {'bases': base_curs})


def get_latest(request):
    response = dict()
    response[newest_date()] = get_newest_for_all()
    return HttpResponse(json.dumps(response))


def base_64_compare(request, from_cur, to_cur):
    base_curs = get_bascurs()
    if to_cur not in base_curs or from_cur not in base_curs:
        return HttpResponse('invalid input')
    else:
        get_mult__with_dates(from_cur, to_cur)
        with open('response.png', "rb") as image_file:
            base64string = base64.b64encode(image_file.read())
            return HttpResponse(base64string)


def get_all_dates(request):
    return HttpResponse(json.dumps({'dates': list(get_dates())}))


def multiple_compare(request):
    base_curs = get_bascurs()
    if request.POST:
        try:
            base_cur = request.POST['base_cur']
        except:
            return render(request, 'compare_multiple.html', {'bases': base_curs, 'msg': 'invalid base cur'})
        if base_cur not in base_curs:
            return render(request, 'compare_multiple.html', {'bases': base_curs, 'msg': 'invalid base cur'})
        currencies = [elm for elm in request.POST if elm != 'base_cur' and elm != 'csrfmiddlewaretoken'
                      and elm in base_curs and elm != request.POST['base_cur']]
        if len(currencies) == 0:
            return render(request, 'compare_multiple.html', {'bases': base_curs, 'msg': 'no currencies chosen'})
        values, x_values, title, min_val, max_val = get_mult_curs_with_dates(base_cur, currencies)
        return render(request, 'compare_multiple.html',
                      {'bases': base_curs,
                       'plot_div': make_plotly_plot_mult(values, x_values, title, min_val, max_val)})
    return render(request, 'compare_multiple.html', {'bases': base_curs})


def compare_mult_cur(request, base, others):
    base_curs = get_bascurs()
    if base not in base_curs:
        return HttpResponse("Error")
    candidates = others.split("_")
    valid_curs = []
    for elm in candidates:
        if elm == base or elm == "":
            continue
        if elm not in base_curs:
            return HttpResponse("Error")
        valid_curs.append(elm)
    if len(valid_curs) == 0:
        return HttpResponse("Error")
    values, x_values, title, min_val, max_val = get_mult_curs_with_dates(base, valid_curs)
    make_matplot_plot_mult(values, x_values, title, min_val, max_val)
    with open('response2.png', "rb") as image_file:
        base64string = base64.b64encode(image_file.read())
        return HttpResponse(base64string)


def get_latest_lazy(request):
    return HttpResponse(json.dumps(get_newest_for_all()))


@api_view(['POST'])
def store_rent_desc(request):
    return HttpResponse(insert_rent_desc(request.body))


@api_view(['POST'])
def store_rent_data(request):
    return HttpResponse(insert_rent_data(request.body))


def get_all_rent_data(request):
    return HttpResponse(get_all_rent_info())


def get_rent_ids(request):
    return HttpResponse(get_ids_rent())


def one_rent(request, name):
    return HttpResponse(get_one_rent(name))


def get_date_range(request):
    return HttpResponse(get_oldest_newest())


def get_date_range_rent(request):
    return HttpResponse(get_oldest_newest_rent())


def get_date_rent(request):
    return HttpResponse(json.dumps(get_dates_rent()))


def display_rents(request):
    rents = json.loads(get_ids_rent())
    if request.POST:
        wanted_rents = [elm for elm in request.POST if elm != 'csrfmiddlewaretoken' and elm in rents]
        if len(wanted_rents) == 0:
            return render(request, 'plot_rents.html', {'rent_ids': rents, 'msg': "no selected rents"})
        rent_info = json.loads(get_all_rent_info())
        desc_rent = [rent_info[key]['desc'] for key in rent_info if key in wanted_rents]
        rent_values = {key: rent_info[key]['values'] for key in rent_info if key in wanted_rents}
        return render(request, 'plot_rents.html', {'rent_ids': rents, 'rent_desc': desc_rent,
                                                   'plot_div': plot_rents(rent_values)})
    return render(request, 'plot_rents.html', {'rent_ids': rents})


def rent_vs_nok(request):
    y_val_cur, x_value_cur = compare_2_cur("NOK", "SEK")
    kpra_data = json.loads(get_one_rent("KPRA"))['values']
    return render(request, 'rent_and_nok.html', {'plot_div': plot_rent_vs_nok(x_value_cur, y_val_cur, kpra_data)})


def base_curs(request):
    return HttpResponse(json.dumps(get_bascurs()))
