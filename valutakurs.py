#!/usr/bin/env python3
import datetime
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from PIL import Image


def plot_kurs(dates,value,kurs = None):
    x_values = [datetime.datetime.strptime(d, "%Y-%m-%d").date() for d in dates]
    plt.plot(x_values,value)
    if kurs != None:
        plt.title('{} vs NOK'.format(kurs))
        plt.savefig('{}.png'.format(kurs))
    plt.show()


def plot_compare(dates,v1,v2,k1,k2):
    x_values = [datetime.datetime.strptime(d, "%Y-%m-%d").date() for d in dates]
    y = [v1[i]/v2[i] for i in range(len(v1))]
    title = '{} vs {}'.format(k1,k2)
    pic_name = '{}_vs_{}.png'.format(k1,k2)
    plt.plot(x_values, y)
    plt.title(title)
    plt.savefig(pic_name)
    plt.show()


def les_inn_data(kurser,kurssvigning):
    filnavn = ['dkk.csv','dollar.csv','euro.csv','pund.csv','sek.csv']
    lengde = 0
    dato = None
    for file in filnavn:
        frame = pd.read_csv(file, sep=';')
        frame = frame[['BASE_CUR','Unit Multiplier', 'TIME_PERIOD', 'OBS_VALUE']]
        if file == filnavn[0]:
            dato = frame['TIME_PERIOD']
            lengde = len(dato)
        name = frame.BASE_CUR.unique()[0]
        if frame['Unit Multiplier'].unique()[0] == 'Hundreds':
            kurser[name] = list(frame['OBS_VALUE'])[-1] / 100
            v = list(frame['OBS_VALUE'])
            kurssvigning[name] = [v[i] / 100 for i in range(len(v))]
        else:
            kurser[name] = list(frame['OBS_VALUE'])[-1]
            kurssvigning[name] = list(frame['OBS_VALUE'])
    kurser['NOK'] = 1
    kurssvigning['NOK'] = [1 for _ in range(lengde)]
    return dato


if __name__ == '__main__':
    kurser = {}
    kurssvigning = {}
    dates = les_inn_data(kurser,kurssvigning)
    valutaer = list(kurser.keys())
    while True:
        inn = -1
        try:
            inn = int(input('1 for sjekking av valutakurs, 2 for kursendringer av valuta og 0 for å avslutte: '))
        except:
            print('ugyldig input')
            inn = -1
        if inn == 0:
            break
        elif inn == 1:
            print(valutaer)
            v1 = input('velg ønsket valuta(forkortelsen): ').upper()
            v2 = input('velg ønsket valuta(forkortelsen): ').upper()
            if v1 in valutaer and v2 in valutaer:
                belop = int(input('ønsket beløp: '))
                orginal = belop
                if v1 == v2:
                    print('{:1.2f} {} er {:1.2f} {}'.format(orginal, v1, belop, v2))
                else:
                    belop = belop * kurser[v1] / kurser[v2]
                    print('{:1.2f} {} er {:1.2f} {}'.format(orginal, v1, belop, v2))
            else:
                print('en eller flere valg var ikke gyldig')
        elif inn == 2:
            valg = int(input('1:sammenligne NOK med en annen valuta,2:sammenligne 2 andre valutaer: '))
            if valg == 1:
                print(valutaer)
                v1 = input('velg ønsket valuta(forkortelsen): ').upper()
                if v1 in valutaer:
                    try:
                        name = '{}.png'.format(v1)
                        Image.show(name)
                    except:
                        plot_kurs(dates, kurssvigning[v1], v1)
                else:
                    print('ugyldig valg')
            if valg == 2:
                print(valutaer)
                v1 = input('velg ønsket valuta(forkortelsen): ').upper()
                v2 = input('velg ønsket valuta(forkortelsen): ').upper()
                if v1 in valutaer and v2 in valutaer:
                    if v1 != v2:
                        try:
                            name = '{}_vs_{}.png'.format(v1, v2)
                            Image.show(name)
                        except:
                            plot_compare(dates, kurssvigning[v1], kurssvigning[v2], v1, v2)
                    elif v2 == 'NOK':
                        try:
                            name = '{}.png'.format(v1)
                            Image.show(name)
                        except:
                            plot_kurs(dates, kurssvigning[v1], v1)
                    else:
                        print('du skrev in {} som både alt1 og alt2, ingen vits å plote grafen'.format(v1))
                else:
                    print('en eller flere valg var ikke gyldig')

