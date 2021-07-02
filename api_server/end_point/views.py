from django.shortcuts import render

from django.http import HttpResponse,JsonResponse
from rest_framework.decorators import api_view
from rest_framework import generics
from .models import Currency_value
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
from plotly.offline import plot
import plotly.graph_objects as go


def index(request):
    #return render(request,"home.html")
    return HttpResponse("Hello, world. You're at the polls index.")

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
        print(request.POST)
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
            return render(request, 'compare.html', {'bases': base_curs,'plot_div': plot_div})
    return render(request, 'compare.html', {'bases': base_curs})
