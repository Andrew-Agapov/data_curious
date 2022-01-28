import requests
import pandas as pd
import datetime

dti = pd.date_range(start="2010-01-01", end="2022-01-01", freq="M")

dates_list = list(dti.strftime('%d.%m.%Y'))

all_dates = []

url = "https://api.privatbank.ua/p24api/exchange_rates"

for i in range(len(dates_list)):
    querystring = {"json":"","date":dates_list[i]}
    payload = ""
    response = requests.request("GET", url, data=payload, params=querystring).json()
    dict_day=response['exchangeRate']
    for j in range(len(dict_day)):
        dict_day[j]['date']=dates_list[i]
    print(f"Addding data from {dates_list[i]}")
    all_dates += dict_day


df = pd.DataFrame(all_dates)

df.to_csv('liqpay_monthly_2010_to_2021.csv')
