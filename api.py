#!/usr/bin/env python3
import json
import requests
from datetime import date
from dateutil.relativedelta import relativedelta
import pandas as pd
import datetime
import matplotlib.pyplot as plt
from PIL import Image


def plot_kurs(dates,value,kurs):
    x_values = [datetime.datetime.strptime(d, "%Y-%m-%d").date() for d in dates]
    plt.plot(x_values,value)
    plt.title('{} vs EUR'.format(kurs))
    plt.xlim([x_values[0], x_values[-1]])
    plt.show()


def plot_compare(dates,v1,v2,k1,k2):
    x_values = [datetime.datetime.strptime(d, "%Y-%m-%d").date() for d in dates]
    y = [v2[i]/v1[i] for i in range(len(v1))]
    title = '{} vs {}'.format(k1,k2)
    pic_name = '{}_vs_{}.png'.format(k1,k2)
    plt.plot(x_values, y)
    plt.title(title)
    plt.xlim([x_values[0], x_values[-1]])
    plt.show()


def lagre_info(df):
    f = open("dato.txt", "w+")
    f.write(str(date.today()))
    f.close()
    df.to_csv("kurser.csv")


def les_inn():
    formating = "%Y-%m-%d"
    dato = ""
    try:
        f = open("dato.txt", "r+")
        dato = f.readline()
        f.close()
        dato = datetime.datetime.strptime(dato, formating).date()
    except:
        pass
    if dato != "" or dato > date.today() - datetime.timedelta(days=7):
        end_l = date.today()
        start_l = date.today() + relativedelta(months=-6)
        https_l = "https://api.exchangeratesapi.io/history?start_at={}&end_at={}".format(start_l, end_l)
        history_l = requests.get(https_l)
        x_l = history_l.json()
        df_l = pd.DataFrame(x_l["rates"])
        df_l = df_l.reindex(sorted(df_l.columns), axis=1)
        dato = list(df_l.columns)
        euro = {d: 1 for d in dato}
        df_l.loc['EUR'] = euro
        df_l.index.name = "Currency"
        return df_l
    else:
        currency_date = dict()
        df_l = pd.read_csv('kurser.csv', sep=',')#, index_col=[0])  # .drop(['unnamed 0'],axis=1)
        if dato != date.today():
            res = requests.get("https://api.exchangeratesapi.io/latest")
            currency_date = json.loads(res.content.decode('utf-8'))["rates"]
            currency_date['EUR'] = 1.0
            df_l[str(date.today())] = currency_date
        df_l.index.name = "Currency"
        return df_l


def endring_dag(df):
    currency = list(df.index)
    last_two_days = list(list(df.columns)[-3:-1])
    endringer = {cur: float("{:.2f}".format(df.loc[cur, last_two_days[0]] - df.loc[cur, last_two_days[1]])) for cur in currency}
    print(endringer)


def endring_dag_valuta(df,cur):
    last_two_days = list(list(df.columns)[-3:-1])
    endring = float("{:.2f}".format(df.loc[cur, last_two_days[0]] - df.loc[cur, last_two_days[1]]))
    print(cur,endring)


def endring_uke(df):
    currency = list(df.index)
    last_week = list(list(df.columns)[-8:-1])
    endringer = {cur: float("{:.2f}".format(df.loc[cur, last_week[0]] - df.loc[cur, last_week[-1]])) for cur in currency}
    print(endringer)


def endring_uke_valuta(df,cur):
    last_week = list(list(df.columns)[-8:-1])
    endring = float("{:.2f}".format(df.loc[cur, last_week[0]] - df.loc[cur, last_week[-1]]))
    print(cur,endring)


def storste_endring_dag(df):
    dager = list(df.columns)
    currency = list(df.index)[:len(list(df.index))-1]
    endringer = {cur: (float("{:.2f}".format(df.loc[cur, dager[0]] - df.loc[cur, dager[1]])),dager[0],dager[1]) for cur in currency}
    for cur in currency:
        for i in range(1,len(dager)-1):
            dags_endring = float("{:.2f}".format(df.loc[cur, dager[i]] - df.loc[cur, dager[i+1]]))
            if endringer[cur][0] < dags_endring:
                endringer[cur] = (dags_endring,dager[i],dager[i+1])
    return endringer


def storste_endring_periode(df,antDager=7):
    dager = list(df.columns)
    currency = list(df.index)[:len(list(df.index)) - 1]
    endringer = {cur: (float("{:.2f}".format(df.loc[cur, dager[0]] - df.loc[cur, dager[6]])), dager[0], dager[1]) for
                 cur in currency}
    for cur in currency:
        for i in range(1, len(dager) - antDager):
            periode_endring = float("{:.2f}".format(df.loc[cur, dager[i]] - df.loc[cur, dager[i + antDager-1]]))
            if endringer[cur][0] < periode_endring:
                endringer[cur] = (periode_endring, dager[i], dager[i + antDager-1])
    return endringer


def ant_dager_med_oking_cur(cur_inn,dato,cur):
    dager = dato
    endringer = {cur: [0,[]]}
    cur_value = cur_inn
    d = 1
    while d < len(dager):
        i = d
        cntDager = 0
        dagene = []
        dagene.append(dager[i - 1])
        while i < len(dager) and cur_value[i]-cur_value[i-1] > 0:
            cntDager += 1
            dagene.append(dager[i])
            i += 1
        if cntDager > endringer[cur][0]:
            endringer[cur][0] = cntDager
            endringer[cur][1] = dagene
        d = i + 1
    return endringer[cur]


if __name__ == '__main__':
    """response = requests.get("https://api.exchangeratesapi.io/latest")
    print(response)
    currency_date = json.loads(response.content.decode('utf-8'))["rates"]"""
    """end = date.today()
    start = date.today() + relativedelta(months=-6)
    print(start,end)
    https = "https://api.exchangeratesapi.io/history?start_at={}&end_at={}".format(start,end)
    history = requests.get(https)
    hr =json.loads(history.content.decode('utf-8'))["rates"]
    curAllDates = {}
    dates = []
    teller = 0
    for h in hr:
        #print(hr[h])
        dates.append(h)
        test = []
        curDate = {}
        for key in hr[h]:
            test.append(key)
            #print(key,hr[h][key])
            curDate[key] = hr[h][key]
        curAllDates[h] = curDate

    dates = sorted(list(curAllDates.keys()))
    x = history.json()
    df = pd.DataFrame(x["rates"])
    print(df)
    df = df.reindex(sorted(df.columns), axis=1)
    print(df)
    dato = list(df.columns)
    valutaer = list(df.index)
    euro = {d:1 for d in dato}
    print(euro)
    df.loc['EUR'] = euro
    print(df)"""
    df = les_inn()
    """print(list(df.columns))
    print(df)
    lagre_info(df)
    df = les_inn()
    print(list(df.columns))
    print(df)"""
    while True:
        svar = -1
        try:
            svar = int(input('-1 for å avslutte,1 for sammenligning av valuta,2 for plot av sammenligning,'
                             '3 for endring siste dag, \n4 for endring siste uken,5 endring av enkel valuta siste dag, '
                             '6 for endring enkel valuta siste uken \n, 7 for endring i løpet av en periode,'
                             '8 for data mining for dager og perioder eller 9 for å plotte sammenligning mot EUR: '))
        except:
            svar = 0
        if svar == -1:
            lagre_info(df)
            break
        elif svar == 0:
            print('du skrev inn noe som ikke var ett tall')
        elif svar == 1:
            print(list(df.index))
            v1 = input('velg ønsket valuta(forkortelsen): ').upper()
            v2 = input('velg ønsket valuta(forkortelsen): ').upper()
            if v1 != v2 and v1 in list(df.index) and v2 in list(df.index):
                belop = input('ønsket beløp: ')
                try:
                    if ',' in belop:
                        belop = belop.replace(',', '.')
                        belop = float(belop)
                    else:
                        belop = int(belop)
                except:
                    belop = 0
                orginal = belop
                belop = belop * df.loc[v2,list(df.columns)[-1]] / df.loc[v1,list(df.columns)[-1]]
                print('{:1.2f} {} er {:1.2f} {}'.format(orginal, v1, belop, v2))
        elif svar == 2:
            print(list(df.index))
            v1 = input('velg ønsket valuta(forkortelsen): ').upper()
            v2 = input('velg ønsket valuta(forkortelsen): ').upper()
            if v1 != v2 and v1 in list(df.index) and v2 in list(df.index):
                cur1 = list(df.loc[v1,:])
                cur2 = list(df.loc[v2, :])
                dato = list(df.columns)
                plot_compare(dato,cur1,cur2,v1,v2)
        elif svar == 3:
            endring_dag(df)
        elif svar == 4:
            endring_uke(df)
        elif svar == 5:
            print(list(df.index))
            v1 = input('velg ønsket valuta(forkortelsen): ').upper()
            if v1 in df.index:
                endring_dag_valuta(df, v1)
            else:
                print('valutaen du skrev inn var ikke gyldig')
        elif svar == 6:
            print(list(df.index))
            v1 = input('velg ønsket valuta(forkortelsen): ').upper()
            if v1 in df.index:
                endring_uke_valuta(df,v1)
            else:
                print('valutaen du skrev inn var ikke gyldig')
        elif svar == 7:
            d1 = input('velg dato(yyyy-mm-dd)(ikke før {}): '.format(list(df.columns)[0])).upper()
            d2 = input('velg dato en senere dato(yyyy-mm-dd)(senest i dag:{}): '.format(date.today())).upper()
        elif svar == 8:
            sd = storste_endring_dag(df)
            for key in sd:
                print(key,sd[key])
            try:
                antDager = int(input("antall dager i perioden for valutaendringer: "))
                sep = storste_endring_periode(df,antDager)
            except:
                print("du skrev inn noe som ikke var et heltall, antall dager settes derfor default til 7")
                sep = storste_endring_periode(df)
            for key in sep:
                print(key,sep[key])
            dager_med_okning = {}
            dato = list(df.columns)
            for cur in list(df.index)[:-1]:
                cur_values = list(df.loc[cur,:])
                dager_med_okning[cur] = ant_dager_med_oking_cur(cur_values,dato,cur)
            #dager_med_okning = ant_dager_med_oking(df)
            for key in dager_med_okning:
                print(key,dager_med_okning[key])
        elif svar == 9:
            print(list(df.index))
            v1 = input('velg ønsket valuta(forkortelsen): ').upper()
            if v1 in df.index:
                plot_kurs(list(df.columns),list(df.loc[v1,:]),v1)
            else:
                print('valutaen du skrev inn var ikke gyldig')

