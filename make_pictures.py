#!/usr/bin/env python3
from valutakurs import plot_compare
from valutakurs import plot_kurs
from valutakurs import les_inn_data

if __name__ == '__main__':
    kurser = {}
    kurssvigning = {}
    dates = les_inn_data(kurser, kurssvigning)
    valutaer = list(kurser.keys())
    for v1 in valutaer:
        for v2 in valutaer:
            if v1 != v2:
                if v2 == 'NOK':
                    plot_kurs(dates, kurssvigning[v1], v1)
                else:
                    plot_compare(dates, kurssvigning[v1], kurssvigning[v2],v1,v2)