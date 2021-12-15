from django.http import HttpResponse,JsonResponse
from django.shortcuts import render
from rest_framework.decorators import api_view
from pandas import DataFrame
import json
from .get_stored import *
from .validate_input import *
from .make_plot import *


def index(request):
    return render(request, "home.html")


@api_view(['GET'])
def get_info(request):
    try:
        qs = Currency_value.objects.all()
        currency_data = {}
        #cur2 ={}
        dates = []
        for info in qs:
            if info.cur_name not in currency_data.keys():
                currency_data[info.cur_name] = {}
                #cur2[info.cur_name] = []
            if info.dato not in dates:
                dates.append(info.dato)
            currency_data[info.cur_name][info.dato] = info.value
            #cur2[info.cur_name].append(info.value)
        df = DataFrame(currency_data,index=dates)
        df = df.sort_index()
        df.index.name = 'dates'
        """alterative måte å lage api-et på
        data = {}
        data['currencies'] = cur2
        data['dates'] =dates
        json_data = json.dumps(data)"""
        #return HttpResponse(df.to_json(orient='columns'),content_type='application/json')
        return HttpResponse(df.to_json(orient='index'), content_type='application/json')
        #return HttpResponse(json_data,content_type='application/json')
    except:
        print('something wrong happened')
        return HttpResponse("you should be provided with info")


@api_view(['POST'])
def insert_data(request):
    try:
        data = json.loads(request.body)
        print(data,type(data))
        Currency_value.objects.update_or_create(
            cur_name=data['cur_name'], dato=data['dato'],
            defaults=data
        )
        return HttpResponse("success")
    except:
        return HttpResponse("something bad happened")


@api_view(['GET'])
def get_currency(request):
    base_curs = get_bascurs()
    return HttpResponse(json.dumps({'created by':{'name':'Lars Palm',
                                                  'Gtihub':'https://github.com/larsPalm',
                                                  'Country':'Kolbotn,Norway',
                                                  'When':'Summer 2021'},
                                    'info':['list of our supported currencies',
                                            'made just for fun, not professional'],
                                    'url for data':'http://127.0.0.1:8080/get_info/',
                                    'supported currencies': base_curs}))


def convert(request):
    base_curs = get_bascurs()
    #print(base_curs)
    if request.POST:
        #print(request.POST)
        finnes = True
        er_nummer = True
        from_cur = request.POST['from_cur']
        to_cur = request.POST['to_cur']
        ammount_string = request.POST['quantity']
        if not validate_a_basecur(from_cur) or not validate_a_basecur(to_cur):
            finnes = False
            return render(request, 'convert.html', {'bases': base_curs, 'message': 'invalid input'})
        try:
            ammount = float(ammount_string)
        except:
            ammount = 0
            er_nummer = False
            return render(request, 'convert.html', {'bases': base_curs, 'message': 'invalid input'})
        if from_cur == to_cur:
            msg = f'{ammount} {from_cur} = {ammount} {to_cur}'
            return render(request, 'convert.html', {'bases': base_curs, 'message': msg, 'extra': 'same currency!!'})
        msg = f'{ammount} {from_cur} = {convert_between(from_cur, to_cur, ammount)} {to_cur}'
        return render(request, 'convert.html', {'bases': base_curs, 'message': msg})
    return render(request, 'convert.html', {'bases': base_curs})


def compare(request):
    base_curs = get_bascurs()
    #return HttpResponse('Fuck')
    if request.POST:
        #print(request.POST)
        to_cur = request.POST['to_cur']
        from_cur = request.POST['from_cur']
        if not validate_a_basecur(request.POST['to_cur']) or not validate_a_basecur(request.POST['from_cur']):
            return render(request, 'compare.html', {'bases': base_curs,'msg':'invalid input'})
        else:
            return render(request, 'compare.html', {'bases': base_curs,
                                                    'plot_div': plot_compare_2_cur(from_cur,to_cur),
                                                    'cur_from':from_cur,
                                                    'cur_to':to_cur})
    return render(request, 'compare.html', {'bases': base_curs})


def get_latest(request):
    response = {}
    response[newest_date()] = get_newest_for_all()
    return HttpResponse(json.dumps(response))


def base_64_compare(request,from_cur,to_cur):
    base_curs = get_bascurs()
    if to_cur not in base_curs or from_cur not in base_curs:
        return HttpResponse('invalid input')
    else:
        get_mult__with_dates(from_cur,to_cur)
        with open('response.png', "rb") as image_file:
            base64string = base64.b64encode(image_file.read())
            return HttpResponse(base64string)


def get_all_dates(request):
    return HttpResponse(json.dumps({'dates':list(get_dates())}))


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
                      and elm in base_curs and elm !=request.POST['base_cur']]
        if len(currencies) == 0:
            return render(request, 'compare_multiple.html', {'bases': base_curs,'msg':'no currencies chosen'})
        values,x_values,title,min_val,max_val = get_mult_curs_with_dates(base_cur,currencies)
        plot_div = make_plotly_plot_mult(values,x_values,title,min_val,max_val)
        return render(request, 'compare_multiple.html', {'bases': base_curs, 'plot_div': plot_div})
    return render(request, 'compare_multiple.html', {'bases': base_curs})


def compare_mult_cur(request,base,others):
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
    values,x_values,title,min_val,max_val = get_mult_curs_with_dates(base,valid_curs)
    make_matplot_plot_mult(values,x_values,title,min_val,max_val)
    with open('response2.png', "rb") as image_file:
        base64string = base64.b64encode(image_file.read())
        return HttpResponse(base64string)


def get_latest_lazy(request):
    return HttpResponse(json.dumps(get_newest_for_all()))