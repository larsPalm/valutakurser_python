from django.shortcuts import render

from django.http import HttpResponse,JsonResponse,Http404
from rest_framework.decorators import api_view
from rest_framework import generics
from .models import CurrencyValue
from django.core.serializers import serialize
import pandas as pd
from pandas import DataFrame
import json


def index(request):
    return HttpResponse("Hello, world. You're at the currencyapiserver index.")

@api_view(['GET'])
def get_info(request):
    try:
        print('1')
        qs = CurrencyValue.objects.all()
        currency_data = {}
        #cur2 ={}
        dates = []
        print('2')
        for info in qs:
            print('gs')
            if info.cur_name not in currency_data.keys():
                currency_data[info.cur_name] = {}
                #cur2[info.cur_name] = []
            if info.dato not in dates:
                dates.append(info.dato)
            currency_data[info.cur_name][info.dato] = info.value
            #cur2[info.cur_name].append(info.value)
        print('m3')
        df = DataFrame(currency_data,index=dates)
        df = df.sort_index()
        df.index.name = 'dates'
        print('success')
        print('3')
        #return HttpResponse(df.to_json(orient='columns'),content_type='application/json')
        return HttpResponse(df.to_json(orient='index'), content_type='application/json')
        #return HttpResponse(json_data,content_type='application/json')
    except:
        print('something wrong happened')
        return HttpResponse("you should be provided with info, an error has occurred")

@api_view(['POST'])
def insert_data(request):
    try:
        data = json.loads(request.body)
        print(data,type(data))
        CurrencyValue.objects.update_or_create(
            cur_name=data['cur_name'], dato=data['dato'],
            defaults=data
        )
        return HttpResponse("success")
    except:
        return HttpResponse("something bad happened")