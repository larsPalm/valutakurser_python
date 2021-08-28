from django.shortcuts import render

from django.http import HttpResponse,JsonResponse
from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from rest_framework import generics
from .models import Currency_value, CustomUser
from django.db.models import Max
from django.core.serializers import serialize
import pandas as pd
from pandas import DataFrame
import json
from django.conf import settings
import datetime
from random import randint
import matplotlib.pyplot as plt
import io, base64
from plotly.offline import plot,plot_mpl
import plotly.graph_objects as go
from django.http import FileResponse
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from .forms import SignUpForm
from django.contrib.auth import login, logout
#from rest_framework_api_key.models import APIKey


def index(request):
    return render(request,"home.html")
    #return HttpResponse("Hello, world. You're at the polls index.")

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
    sql_response = Currency_value.objects.values('cur_name').distinct()
    base_curs = []
    for elm in sql_response:
        base_curs.append(elm['cur_name'])
    return HttpResponse(json.dumps({'created by':{'name':'Lars Palm',
                                                  'Gtihub':'https://github.com/larsPalm',
                                                  'Country':'Kolbotn,Norway',
                                                  'When':'Summer 2021'},
                                    'info':['list of our supported currencies',
                                            'made just for fun, not professional'],
                                    'url for data':'http://127.0.0.1:8080/get_info/',
                                    'supported currencies': base_curs}))


def convert(request):
    sql_response = Currency_value.objects.values('cur_name').distinct()
    base_curs = []
    for elm in sql_response:
        base_curs.append(elm['cur_name'])
    #print(base_curs)
    if request.POST:
        #print(request.POST)
        finnes = True
        er_nummer = True
        #print(request.POST['from_cur'],request.POST['to_cur'],request.POST['quantity'])
        from_cur = request.POST['from_cur']
        to_cur = request.POST['to_cur']
        ammount_string = request.POST['quantity']
        if from_cur not in base_curs or to_cur not in base_curs:
            finnes = False
        try:
            ammount = float(ammount_string)
        except:
            ammount = 0
            er_nummer = False
        if finnes == False or er_nummer == False:
            return render(request, 'convert.html', {'bases': base_curs,'message':'invalid input'})
        if finnes and er_nummer:
            if from_cur == to_cur:
                msg = f'{ammount} {from_cur} = {ammount} {to_cur}'
                return render(request, 'convert.html', {'bases': base_curs, 'message':msg,'extra':'same currency!!'})
            max_year = Currency_value.objects.all().aggregate(Max('dato'))['dato__max']
            cur1 = Currency_value.objects.get(dato=max_year,cur_name=from_cur).value
            cur2 = Currency_value.objects.get(dato=max_year, cur_name=to_cur).value
            the_value = round((cur1/cur2)*ammount, 2)
            #print(cur1,cur2,ammount,the_value)
            msg =f'{ammount} {from_cur} = {the_value} {to_cur}'
            return render(request, 'convert.html', {'bases': base_curs, 'message': msg})
    return render(request, 'convert.html', {'bases': base_curs})


def compare(request):
    sql_response = Currency_value.objects.values('cur_name').distinct()
    base_curs = []
    for elm in sql_response:
        base_curs.append(elm['cur_name'])
    #return HttpResponse('Fuck')
    if request.POST:
        print(request.POST)
        to_cur = request.POST['to_cur']
        from_cur = request.POST['from_cur']
        if to_cur not in base_curs or from_cur not in base_curs:
            return render(request, 'compare.html', {'bases': base_curs,'msg':'invalid input'})
        else:
            date_dict = Currency_value.objects.values('dato').distinct()
            datoer = [elm['dato'] for elm in date_dict]
            cur1_values = [Currency_value.objects.get(dato=date, cur_name=from_cur).value for date in datoer]
            cur2_values = [Currency_value.objects.get(dato=date, cur_name=to_cur).value for date in datoer]
            graph_value = [round(v1 / v2, 4) for v1, v2 in zip(cur1_values, cur2_values)]
            x_values = [datetime.datetime.strptime(d, "%Y-%m-%d").date() for d in datoer]
            graphs = []
            fig = go.Scatter(x=x_values,y=graph_value,mode='lines',fill='tozeroy')
            graphs.append(fig)
            layout = go.Layout(title='{} vs {}'.format(from_cur, to_cur),
                               yaxis=dict(range=[min(graph_value), max(graph_value)]))
            plot_div = plot({'data': graphs, 'layout': layout},
                            output_type='div')
            return render(request, 'compare.html', {'bases': base_curs,
                                                    'plot_div': plot_div,
                                                    'cur_from':from_cur,
                                                    'cur_to':to_cur})
    return render(request, 'compare.html', {'bases': base_curs})

def get_latest(request):
    sql_response = Currency_value.objects.values('cur_name').distinct()
    base_curs = []
    for elm in sql_response:
        base_curs.append(elm['cur_name'])
    max_year = Currency_value.objects.all().aggregate(Max('dato'))['dato__max']
    data = {}
    for base in base_curs:
        data[base] = Currency_value.objects.get(dato=max_year, cur_name=base).value
    response = {}
    response[max_year] = data
    return HttpResponse(json.dumps(response))


#@api_view(['POST'])
def compare_img(request):
    sql_response = Currency_value.objects.values('cur_name').distinct()
    base_curs = []
    for elm in sql_response:
        base_curs.append(elm['cur_name'])
    #return HttpResponse('Fuck')
    if request.POST or True:
        print(request.POST)
        #to_cur = request.POST['to_cur']
        #from_cur = request.POST['from_cur']
        to_cur = 'EUR'
        from_cur = 'USD'
        if to_cur not in base_curs or from_cur not in base_curs:
            return HttpResponse('invalid input')
        else:
            date_dict = Currency_value.objects.values('dato').distinct()
            datoer = [elm['dato'] for elm in date_dict]
            cur1_values = [Currency_value.objects.get(dato=date, cur_name=from_cur).value for date in datoer]
            cur2_values = [Currency_value.objects.get(dato=date, cur_name=to_cur).value for date in datoer]
            graph_value = [round(v1 / v2, 4) for v1, v2 in zip(cur1_values, cur2_values)]
            x_values = [datetime.datetime.strptime(d, "%Y-%m-%d").date() for d in datoer]
            graphs = []
            fig = go.Scatter(x=x_values,y=graph_value,mode='lines',fill='tozeroy')
            graphs.append(fig)
            layout = go.Layout(title='{} vs {}'.format(from_cur, to_cur),
                               yaxis=dict(range=[min(graph_value), max(graph_value)]))
            plot_div = plot({'data': graphs, 'layout': layout},
                            output_type='div')
            print(type(plot_div))
            return HttpResponse(plot_div)
    return render(request, 'compare.html', {'bases': base_curs})


@api_view(['GET'])
def compare_img2(request,from_cur,to_cur):
    sql_response = Currency_value.objects.values('cur_name').distinct()
    base_curs = []
    print(from_cur,to_cur)
    for elm in sql_response:
        base_curs.append(elm['cur_name'])
    if to_cur not in base_curs or from_cur not in base_curs:
        return HttpResponse('invalid input')
    else:
        date_dict = Currency_value.objects.values('dato').distinct()
        datoer = [elm['dato'] for elm in date_dict]
        cur1_values = [Currency_value.objects.get(dato=date, cur_name=from_cur).value for date in datoer]
        cur2_values = [Currency_value.objects.get(dato=date, cur_name=to_cur).value for date in datoer]
        graph_value = [round(v1 / v2, 4) for v1, v2 in zip(cur1_values, cur2_values)]
        x_values = [datetime.datetime.strptime(d, "%Y-%m-%d").date() for d in datoer]
        graphs = []
        fig = go.Scatter(x=x_values, y=graph_value, mode='lines', fill='tozeroy')
        graphs.append(fig)
        layout = go.Layout(title='{} vs {}'.format(from_cur, to_cur),
                           yaxis=dict(range=[min(graph_value), max(graph_value)]))
        plot_div = plot({'data': graphs, 'layout': layout},
                        output_type='div')

        #plot_mpl(fig2)
        print(type(plot_div))
        return HttpResponse(plot_div)

def base_64_compare(request,from_cur,to_cur):
    sql_response = Currency_value.objects.values('cur_name').distinct()
    base_curs = []
    print(from_cur, to_cur)
    for elm in sql_response:
        base_curs.append(elm['cur_name'])
    if to_cur not in base_curs or from_cur not in base_curs:
        return HttpResponse('invalid input')
    else:
        date_dict = Currency_value.objects.values('dato').distinct()
        datoer = [elm['dato'] for elm in date_dict]
        cur1_values = [Currency_value.objects.get(dato=date, cur_name=from_cur).value for date in datoer]
        cur2_values = [Currency_value.objects.get(dato=date, cur_name=to_cur).value for date in datoer]
        graph_value = [round(v1 / v2, 4) for v1, v2 in zip(cur1_values, cur2_values)]
        x_values = [datetime.datetime.strptime(d, "%Y-%m-%d").date() for d in datoer]
        title = '{} vs {}'.format(from_cur, to_cur)
        colors1 = ['b', "g", 'r', 'c', "m", "y", 'k']
        colors2 = ["blue", "green", 'red', "cyan", "magenta", 'yellow', 'black']
        index = randint(0, len(colors1) - 1)
        fig2 = plt.figure()
        plt.plot(x_values, graph_value, colors1[index])
        plt.fill_between(x_values, graph_value, color=colors2[index], alpha=0.5)
        plt.title(title)
        plt.ylim(min(graph_value), max(graph_value))
        plt.xlim([x_values[0], x_values[-1]])
        fig2.savefig('response.png')
        with open('response.png', "rb") as image_file:
            base64string = base64.b64encode(image_file.read())
            return HttpResponse(base64string)


def logout_view(request):
    logout(request)
    return redirect('home')


def login_view(request):
    return redirect('login')


def signup_view(request):
    form = SignUpForm(request.POST)
    if form.is_valid():
        user = form.save()
        user.refresh_from_db()
        login(request, user)
        #api_key, key = APIKey.objects.create_key(name="my-remote-service")
        #print(api_key,key,APIKey.objects.count())
        print(user.email)
    return render(request, 'signup.html', {'form': form})

def get_all_dates(request):
    sql_response = Currency_value.objects.values('dato').distinct()
    dates = []
    for elm in sql_response:
        dates.append(elm['dato'])
    return HttpResponse(json.dumps({'dates':list(dates)}))


def multiple_compare(request):
    sql_response = Currency_value.objects.values('cur_name').distinct()
    base_curs = []
    for elm in sql_response:
        base_curs.append(elm['cur_name'])
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
        date_dict = Currency_value.objects.values('dato').distinct()
        datoer = [elm['dato'] for elm in date_dict]
        base_cur_value = [Currency_value.objects.get(dato=date, cur_name=base_cur).value for date in datoer]
        values = {}
        x_values = [datetime.datetime.strptime(d, "%Y-%m-%d").date() for d in datoer]
        for elm in currencies:
            cur_val = [Currency_value.objects.get(dato=date, cur_name=elm).value for date in datoer]
            values[elm] = [round(y1/y2,4) for y1,y2 in zip(cur_val,base_cur_value)]
        graphs = []
        for elm in values:
            fig = go.Scatter(x=x_values, y=values[elm], mode='lines',name=elm)
            graphs.append(fig)
        title = f'{base_cur} vs '
        for elm in values:
            title += elm
            if elm != currencies[-1]:
                title += ', '
        max_val,min_val = -100,-100
        for key in values:
            for elm in values[key]:
                if max_val < elm:
                    max_val = elm
                if min_val<0:
                    min_val = elm
                elif min_val>0 and min_val>elm:
                    min_val = elm
        layout = go.Layout(title=title,
                           yaxis=dict(range=[min_val, max_val]))
        plot_div = plot({'data': graphs, 'layout': layout},
                        output_type='div')
        return render(request, 'compare_multiple.html', {'bases': base_curs, 'plot_div': plot_div})
    return render(request, 'compare_multiple.html', {'bases': base_curs})

def compare_mult_cur(request,base,others):
    sql_response = Currency_value.objects.values('cur_name').distinct()
    base_curs = []
    for elm in sql_response:
        base_curs.append(elm['cur_name'])
    if base not in base_curs:
        return HttpResponse("Error")
    candidates = others.split("_")
    print(candidates)
    valid_curs = []
    for elm in candidates:
        if elm == base or elm == "":
            continue
        if elm not in base_curs:
            return HttpResponse("Error")
        valid_curs.append(elm)
    print(valid_curs)
    date_dict = Currency_value.objects.values('dato').distinct()
    datoer = [elm['dato'] for elm in date_dict]
    base_cur_value = [Currency_value.objects.get(dato=date, cur_name=base).value for date in datoer]
    values = {}
    x_values = [datetime.datetime.strptime(d, "%Y-%m-%d").date() for d in datoer]
    for elm in valid_curs:
        cur_val = [Currency_value.objects.get(dato=date, cur_name=elm).value for date in datoer]
        values[elm] = [round(y1 / y2, 4) for y1, y2 in zip(cur_val, base_cur_value)]
    print()
    title = f'{base} vs '
    for elm in values:
        title += elm
        if elm != valid_curs[-1]:
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
    fig2 = plt.figure()
    for key in values:
        plt.plot(x_values, values[key], label=key)
    plt.title(title)
    plt.legend()
    plt.ylim(min_val, max_val)
    plt.xlim([x_values[0], x_values[-1]])
    fig2.savefig('response2.png')
    with open('response2.png', "rb") as image_file:
        base64string = base64.b64encode(image_file.read())
        return HttpResponse(base64string)

def get_latest_lazy(request):
    sql_response = Currency_value.objects.values('cur_name').distinct()
    base_curs = []
    for elm in sql_response:
        base_curs.append(elm['cur_name'])
    max_year = Currency_value.objects.all().aggregate(Max('dato'))['dato__max']
    data = {}
    for base in base_curs:
        data[base] = Currency_value.objects.get(dato=max_year, cur_name=base).value
    response = {}
    response[max_year] = data
    return HttpResponse(json.dumps(data))