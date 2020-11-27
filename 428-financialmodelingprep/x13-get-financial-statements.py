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

def getFinancialStatements(stock):
    url = base_url + stock + '?period=quarter&limit=400&apikey=' + api_key
    response = urlopen(url)
    data = response.read().decode("utf-8")
    return json.loads(data)



parser = argparse.ArgumentParser()
parser.add_argument('--env', '--env', help="current Env (local | qa | prod)", default='local')
args = parser.parse_args()

env = args.env
if env == 'local':
    data_dir = '../data/15-modeling-prep-statements'
else:
    data_dir = f'/home/p372-ml-algo-data/15-modeling-prep-statements'

if not os.path.exists(data_dir):
    os.makedirs(data_dir)

stocks = stock_list_util.getListOfSandP500()
print(stocks)

base_url='https://financialmodelingprep.com/api/v3/income-statement/'
api_key='d27aedcb3e73e196af83533987c39bdf'

i=0
try:
    for stock in stocks[0:]:
        i += 1
        print(f'{i} - {stock}')
        file = data_dir + f'/{stock}.csv'
        if os.path.exists(file):
            print(f'{i} - {stock} already downloaded, so ignore it.')
            continue
        try:
            df_final = pd.DataFrame()

            statements = getFinancialStatements(stock)
            for s in statements:
                df = pd.DataFrame([s])
                df_final = df_final.append(df)

            print(f'Date: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}, len: {len(df_final)}')

            df_final.to_csv(file, index=False, header=True)

        except Exception as exception:
            print('Error is here1')
            print(exception)
except Exception as exception:
    print('Error is here2')
    print(exception)
