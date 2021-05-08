#!/usr/bin/env python3
import json
import requests
from datetime import date
from dateutil.relativedelta import relativedelta
import pandas as pd
import datetime
import matplotlib.pyplot as plt
from PIL import Image

#plan to make sure it only calls the api once per day
def les_info():
    date_string = open("dates.txt","r").readline().strip()
    old_date = datetime.datetime.strptime(date_string, formating).date()
    end_l = date.today()
    start_l = date.today() + relativedelta(months=-6)
    new_url = "https://data.norges-bank.no/api/data/EXR/B.USD+AUD+BDT+BRL+GBP+BGN+DKK+EUR+PHP+HKD+XDR+I44+INR+IDR+TWI+ISK+JPY+CAD+CNY+HRK+MXN+MMK+NZD+ILS+RON+BYN+TWD+PKR+PLN+RUB+SGD+CHF+SEK+ZAR+KRW+THB+CZK+TRY+HUF.NOK.SP?format=sdmx-json&startPeriod={}&endPeriod={}&locale=no".format(start_l,end_l)
    #some code
    history_l = requests.get(new_url)
    info = history_l.json()
    #base for currencies
    print(info["data"]["dataSets"][0]["series"])
    currencies = []
    #extracting the values per currency per day
    for key in info["data"]["dataSets"][0]["series"]:
        cur_dict = info["data"]["dataSets"][0]["series"][key]["observations"]
        currencies.append([round(float(cur_dict[key][0]),2) for key in cur_dict])
    #base for base_url
    print([elm["id"] for elm in info["data"]["structure"]["dimensions"]["series"][1]["values"]])
    base_curs =[elm["id"] for elm in info["data"]["structure"]["dimensions"]["series"][1]["values"]]
    #datoer
    print([elm["id"] for elm in info["data"]["structure"]["dimensions"]["observation"][0]["values"]])
    dates =[elm["id"] for elm in info["data"]["structure"]["dimensions"]["observation"][0]["values"]]
    map_cur_values = {cur:values for cur,values in zip(base_curs,currencies)}
    print(map_cur_values)
    print(pd.DataFrame(map_cur_values))
    return make_dataFrame(map_cur_values,dates)

def get_info():
    #try to see if any information is already stored
   try:
       date_string = open("dates.txt", "r").readline().strip()
       old_date = datetime.datetime.strptime(date_string, formating).date()
       end_l = date.today()
       start_l = date.today() + relativedelta(months=-6)
       #checks whether or not the data is "old", if the data is old, the program will fetch data from the api
       #else, it will read the information from a csv-file
       if old_date < end_l:
           new_url = "https://data.norges-bank.no/api/data/EXR/B.USD+AUD+BDT+BRL+GBP+BGN+DKK+EUR+PHP+HKD+XDR+INR+IDR+TWI+ISK+JPY+CAD+CNY+HRK+MXN+MMK+NZD+ILS+RON+BYN+TWD+PKR+PLN+RUB+SGD+CHF+SEK+ZAR+KRW+THB+CZK+TRY+HUF.NOK.SP?format=sdmx-json&startPeriod={}&endPeriod={}&locale=no".format(
               start_l, end_l)
           api_info = requests.get(new_url)
           info = api_info.json()
           cur_dict = find_curencies(info)
           dates = find_dates(info)
           return make_dataFrame(cur_dict, dates)
       else:
           print(pd.read_csv("currency.csv", sep=";"))
           df = pd.read_csv("currency.csv", sep=";", index_col=0)
           df = df.rename_axis("dates")
           df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
           return df
    #if there is no data stored, the program will fetch data from the api
   except:
       end_l = date.today()
       start_l = date.today() + relativedelta(months=-6)
       new_url = "https://data.norges-bank.no/api/data/EXR/B.USD+AUD+BDT+BRL+GBP+BGN+DKK+EUR+PHP+HKD+XDR+INR+IDR+TWI+ISK+JPY+CAD+CNY+HRK+MXN+MMK+NZD+ILS+RON+BYN+TWD+PKR+PLN+RUB+SGD+CHF+SEK+ZAR+KRW+THB+CZK+TRY+HUF.NOK.SP?format=sdmx-json&startPeriod={}&endPeriod={}&locale=no".format(start_l, end_l)
       api_info = requests.get(new_url)
       info = api_info.json()
       cur_dict = find_curencies(info)
       dates = find_dates(info)
       return make_dataFrame(cur_dict, dates)


def make_dataFrame(cur_values,dates):
    df = pd.DataFrame(cur_values, index=dates)
    df.index.name="dates"
    return df


#finding the string value of the base_cur
def find_bas_cur(json_data):
    return [elm["id"] for elm in json_data["data"]["structure"]["dimensions"]["series"][1]["values"]]


#for finding and maping base_cur to the right currency
def find_curencies(json_data):
    currencies = []
    # extracting the values per currency per day
    #makes an nested list/matrix for handling the data
    for key in json_data["data"]["dataSets"][0]["series"]:
        attributes = json_data["data"]["dataSets"][0]["series"][key]["attributes"]
        cur_dict = json_data["data"]["dataSets"][0]["series"][key]["observations"]
        if (attributes[0] == 1 or attributes[0] == 2 or attributes[0] == 0) and attributes[2] ==1:
            currencies.append([round(float(cur_dict[key][0]), 4)/100.0 for key in cur_dict])
        else:
            currencies.append([round(float(cur_dict[key][0]),4) for key in cur_dict])
    base_curs = find_bas_cur(json_data)
    # mapping each list in the nested list to a string value which represent the base_cur
    map_cur_values = {cur: values for cur, values in zip(base_curs, currencies)}
    map_cur_values["NOK"]= [1.0000 for _ in range(len(currencies[0]))]
    return map_cur_values


#finding the dates
def find_dates(json_data):
    #finds and returns the dates as string values
    return [elm["id"] for elm in json_data["data"]["structure"]["dimensions"]["observation"][0]["values"]]


#plan to save data to csv to minimize api usage
def store_data(df):
    df.to_csv("currency.csv",sep=";")
    file =open("dates.txt","w")
    file.write(str(date.today())+"\n")
    file.close()

def store_data_json(df):
    df.to_json("currency.json")
    file =open("dates.txt","w")
    file.write(str(date.today())+"\n")
    file.close()


def convert_currency(df,base_from,base_to,amount):
    dates =list(df.index)
    c1_val = df.at[dates[-1],base_from]
    c2_val = df.at[dates[-1], base_to]
    new_val = round((c1_val/c2_val)*amount,2)
    print("{} {} = {} {}".format(amount,base_from,new_val,base_to))


def plot_compare(dates, v1, v2, k1, k2):
    x_values = [datetime.datetime.strptime(d, "%Y-%m-%d").date() for d in dates]
    y = [v1[i] / v2[i] for i in range(len(v1))]
    title = '{} vs {}'.format(k1, k2)
    pic_name = '{}_vs_{}.png'.format(k1, k2)
    plt.plot(x_values, y)
    plt.fill_between(x_values, y,alpha=0.5)
    plt.title(title)
    plt.ylim(min(y),max(y))
    plt.xlim([x_values[0], x_values[-1]])
    plt.show()


def plot_currencies(df,wanted_currencies=["EUR","USD","CAD","GBP","SEK"]):
    currencies = {key:list(df.loc[:,key]) for key in wanted_currencies}
    dates = list(df.index)
    x_values = [datetime.datetime.strptime(d, "%Y-%m-%d").date() for d in dates]
    for key in currencies:
        plt.plot(x_values, currencies[key], label=key)
    plt.title('some currencies compared to NOK')
    plt.legend()
    plt.xlim([x_values[0], x_values[-1]])
    plt.show()




if __name__ == '__main__':
    usd_url = "https://data.norges-bank.no/api/data/EXR/B.USD.NOK.SP?format=sdmx-json&startPeriod=2019-12-05&endPeriod=2021-05-05&locale=no"
    new_url = "https://data.norges-bank.no/api/data/EXR/B.USD+AUD+BDT+BRL+GBP+BGN+DKK+EUR+PHP+HKD+XDR+I44+INR+IDR+TWI+ISK+JPY+CAD+CNY+HRK+MXN+MMK+NZD+ILS+RON+BYN+TWD+PKR+PLN+RUB+SGD+CHF+SEK+ZAR+KRW+THB+CZK+TRY+HUF.NOK.SP?format=sdmx-json&startPeriod=2019-12-05&endPeriod=2021-05-05&locale=no"
    ####
    formating = "%Y-%m-%d"
    min_df = get_info()
    store_data(min_df)
    print(date.today(),datetime.datetime.strptime("2021-05-05", formating).date())
    print(date.today()> datetime.datetime.strptime("2021-05-05", formating).date())
    #start of the functionality


    currency_list = list(min_df.columns)
    valg = -1
    while valg != 0:
        print("type 0 for exit\ntype 1 for converting between to currencies\ntype 2 for plot compare of 2 currencies")
        print("type 3 for comparing multiple currencies")
        try:
            valg = int(input("skriv inn ønske: "))
        except:
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
                except:
                    belop = 1.0
                convert_currency(min_df, v1, v2, belop)
            else:
                print("en eller begge valutaene var ikke gyldige")
        elif valg == 2:
            print(currency_list)
            v1 = input("skriv inn forkortelse på valuta nr1: ").upper()
            v2 = input("skriv inn forkortelse på valuta nr2: ").upper()
            if v1 in currency_list and v2 in currency_list:
                cur1 = min_df.loc[:,v1]
                cur2 = min_df.loc[:, v2]
                datoer = min_df.index
                plot_compare(datoer, cur1, cur2, v1, v2)
            else:
                print("en eller begge valutaene var ikke gyldige")

        elif valg ==3:
            print(currency_list)
            navn ="--"
            mine_valg = []
            while navn != '':
                navn = input("skriv inn forkortelsen du vil ha med: ").upper()
                if navn in currency_list:
                    mine_valg.append(navn)
            if len(mine_valg)>0:
                plot_currencies(min_df,mine_valg)
            else:
                print("ingen valutaer valgt")
        #to be implemented
        elif valg == 4:
            pass