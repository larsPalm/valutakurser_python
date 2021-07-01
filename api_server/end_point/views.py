from django.shortcuts import render

from django.http import HttpResponse,JsonResponse
from rest_framework.decorators import api_view
from rest_framework import generics
from .models import Currency_value
from django.core.serializers import serialize
import pandas as pd
from pandas import DataFrame
import json


def index(request):
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