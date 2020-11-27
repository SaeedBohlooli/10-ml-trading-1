#!/usr/bin/env python

try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen

import json
import numpy as np
import pandas as pd
import argparse
import os
from utils import stock_list_util
import datetime

def getMarketCap(stock):
    base_url = 'https://financialmodelingprep.com/api/v3/market-capitalization/'
    url = base_url + stock + '?apikey=' + api_key
    response = urlopen(url)
    data = response.read().decode("utf-8")
    return json.loads(data)

def getStockProfile(stock):
    base_url = 'https://financialmodelingprep.com/api/v3/profile/'
    url = base_url + stock + '?apikey=' + api_key
    response = urlopen(url)
    data = response.read().decode("utf-8")
    return json.loads(data)

parser = argparse.ArgumentParser()
parser.add_argument('--env', '--env', help="current Env (local | qa | prod)", default='local')
args = parser.parse_args()

env = args.env
if env == 'local':
    data_dir = '../data/14-modeling-prep-fundamental'
else:
    data_dir = f'/home/p372-ml-algo-data/14-modeling-prep-fundamental'

if not os.path.exists(data_dir):
    os.mkdir(data_dir)

stocks = stock_list_util.getListOfSandP500()
print(stocks)
api_key='d27aedcb3e73e196af83533987c39bdf'

fundamental_file = data_dir + '/fundamental-modeling-prep.csv'
if os.path.exists(fundamental_file):
    df = pd.read_csv(fundamental_file, parse_dates=True)
else:
    df = pd.DataFrame(columns=['Stock', 'MarketCap','companyName','sector', 'industry','country','exchangeShortName'])
i=0
try:
    for stock in stocks[0:]:
        i += 1
        print(f'{i} - {stock}')
        # if has downloaded before, we ignore for now ...

        try:
            if stock in df['Stock'].values:
                max_price = df[df['Stock'] == stock].iloc[0]['MarketCap']
                print(f'{i} - {stock} - mp:{max_price}')

                if pd.isnull(max_price):
                    print(f'{i} - {stock} - mp:{max_price} is nan')
                    x = getMarketCap(stock)
                    print(f'Date: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}, {x}')
                    marketCap = x[0]['marketCap']
                    df.loc[(df['Stock'] == stock), 'MarketCap'] = marketCap

                companyName = df[df['Stock'] == stock].iloc[0]['companyName']

                if pd.isnull(companyName):
                    print(f'{i} - {stock} - companyName:{companyName} is nan')
                    x = getStockProfile(stock)

                    companyName = x[0]['companyName']
                    df.loc[(df['Stock'] == stock), 'companyName'] = companyName

                    sector = x[0]['sector']
                    df.loc[(df['Stock'] == stock), 'sector'] = sector

                    industry = x[0]['industry']
                    df.loc[(df['Stock'] == stock), 'industry'] = industry

                    country = x[0]['country']
                    df.loc[(df['Stock'] == stock), 'country'] = country

                    exchangeShortName = x[0]['exchangeShortName']
                    df.loc[(df['Stock'] == stock), 'exchangeShortName'] = exchangeShortName

            else:
                x = getStockProfile(stock)
                print(f'{i}) Date: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}, {x}')
                marketCap = x[0]['mktCap']
                companyName = x[0]['companyName']
                sector = x[0]['sector']
                industry = x[0]['industry']
                country = x[0]['country']
                exchangeShortName = x[0]['exchangeShortName']
                df.loc[df.shape[0]] = {'Stock': stock, 'MarketCap': marketCap, 'companyName': companyName,
                                       'sector': sector, 'industry': industry, 'country': country,
                                       'exchangeShortName': exchangeShortName}

        except Exception as exception:
            print('Error is here1')
            print(exception)
except Exception as exception:
    print('Error is here2')
    print(exception)


df.to_csv(fundamental_file, index=False, header=True)
