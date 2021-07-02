#!/usr/bin/env python3
import requests
from datetime import date
from dateutil.relativedelta import relativedelta
import pandas as pd
import datetime
import matplotlib.pyplot as plt
from random import randint
import os

# egne funksjoner:

"""
bruk denne linken for tips:
https://dev.to/coderasha/implement-real-time-updates-with-django-rest-framework-building-cryptocurrency-api-1kld
"""

def les_info():
    response =requests.get("http://127.0.0.1:8080/get_info/")
    json_response = response.json()
    df = pd.DataFrame(json_response)
    print(df.index)
    return df
"""
The next three methods had tp be rewritten do to the fact that the data format is not the
same ass for api_20"""
def convert_currency(df, base_from, base_to, amount):
    dates = list(df.columns)
    c1_val = df.at[base_from,dates[-1]]
    c2_val = df.at[base_to,dates[-1]]
    new_val = round((c1_val / c2_val) * amount, 2)
    print("{} {} = {} {}".format(amount, base_from, new_val, base_to))


def plot_compare(dates, y1, y2, k1, k2):
    x_values = [datetime.datetime.strptime(d, "%Y-%m-%d").date() for d in dates]
    y = [y1[i] / y2[i] for i in range(len(y1))]
    title = '{} vs {}'.format(k1, k2)
    colors1 = ['b', "g", 'r', 'c', "m", "y", 'k']
    colors2 = ["blue", "green", 'red', "cyan", "magenta", 'yellow', 'black']
    index = randint(0, len(colors1)-1)
    #index2 = randint(0, len(colors1) - 1)
    plt.plot(x_values, y, colors1[index])
    plt.fill_between(x_values, y, color=colors2[index], alpha=0.5)
    plt.title(title)
    plt.ylim(min(y), max(y))
    plt.xlim([x_values[0], x_values[-1]])
    plt.show()


def plot_currencies(df, wanted_currencies=None):
    if wanted_currencies is None:
        wanted_currencies = ["EUR", "USD", "CAD", "GBP", "SEK"]
    currencies = {key: list(df.loc[key,:]) for key in wanted_currencies}
    dates = list(df.columns)
    x_values = [datetime.datetime.strptime(d, "%Y-%m-%d").date() for d in dates]
    for key in currencies:
        plt.plot(x_values, currencies[key], label=key)
    plt.title('some currencies compared to NOK')
    plt.legend()
    plt.xlim([x_values[0], x_values[-1]])
    plt.show()



if __name__ == '__main__':
    print(date.today())
    print(os.getenv('API_SERVER_SECRET_KEY'))
    """Note:
    kjør serveren i terminal-appen og ikke i pycharm ettersom pycharm ikke kan se environment variables
    """
    min_df = les_info()
    currency_list = list(min_df.index)
    valg = -1
    while valg != 0:
        print("type 0 for exit\ntype 1 for converting between to currencies\ntype 2 for plot compare of 2 currencies")
        print("type 3 for comparing multiple currencies")
        try:
            valg = int(input("skriv inn ønske: "))
        except ValueError:
            valg = -1
        if valg == -1:
            print("ugyldig valg")

        elif valg == 1:
            print(currency_list)
            v1 = input("skriv inn forkortelse på valuta nr1: ").upper()
            v2 = input("skriv inn forkortelse på valuta nr2: ").upper()
            if v1 in currency_list and v2 in currency_list:
                belop = 1.0
                try:
                    belop = float(input("skriv inn ønsket beløp: "))
                except ValueError:
                    belop = 1.0
                convert_currency(min_df, v1, v2, belop)
            else:
                print("en eller begge valutaene var ikke gyldige")
        elif valg == 2:
            print(currency_list)
            v1 = input("skriv inn forkortelse på valuta nr1: ").upper()
            v2 = input("skriv inn forkortelse på valuta nr2: ").upper()
            if v1 in currency_list and v2 in currency_list:
                cur1 = min_df.loc[v1,:]
                cur2 = min_df.loc[v2,:]
                datoer = min_df.columns
                plot_compare(datoer, cur1, cur2, v1, v2)
            else:
                print("en eller begge valutaene var ikke gyldige")

        elif valg == 3:
            print(currency_list)
            navn = "--"
            mine_valg = []
            while navn != '':
                navn = input("skriv inn forkortelsen du vil ha med: ").upper()
                if navn in currency_list:
                    mine_valg.append(navn)
            if len(mine_valg) > 0:
                plot_currencies(min_df, mine_valg)
            else:
                print("ingen valutaer valgt")
        # to be implemented
        elif valg == 4:
            pass
