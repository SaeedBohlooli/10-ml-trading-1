import json
import numpy as np
import pandas as pd
import argparse
import os
from utils import stock_list_util
import datetime

def addColumns(stock, df_metrics):
    file_history = data_dir_historical + f'/{stock}.csv'
    df_history = pd.read_csv(file_history)
    df_metrics['Price'] = np.nan
    df_metrics['Price High'] = np.nan
    df_metrics['Price Low'] = np.nan

    for index, row in df_metrics.iterrows():
        if index == len(df_metrics) - 1:
            print('y')
            continue
        print(f'row: {row}')
        end_date = row['date']
        start_date = df_metrics.iloc[index + 1]['date']

        df_history_quarter = df_history[(df_history['Date'] >= start_date) & (df_history['Date'] <= end_date)]

        max_price = df_history_quarter.High.max()
        low_price = df_history_quarter.Low.min()
        avg_price = (max_price + low_price) / 2

        df_metrics.at[index, 'Price'] = avg_price
        df_metrics.at[index, 'Price High'] = max_price
        df_metrics.at[index, 'Price Low'] = low_price

    df_metrics['Price Pct Change'] = df_metrics['Price'].pct_change(periods=1).apply(lambda x: x * 100)
    df_metrics['Price High Pct Change'] = df_metrics['Price High'].pct_change(periods=1).apply(lambda x: x * 100)
    df_metrics['Price Low Pct Change'] = df_metrics['Price Low'].pct_change(periods=1).apply(lambda x: x * 100)

    df_metrics['Price High Pct Change'] = df_metrics['Price High Pct Change'].fillna(0)
    df_metrics['Price Low Pct Change'] = df_metrics['Price Low Pct Change'].fillna(0)

    threshold = 3
    df_metrics['Decision'] = np.where( (df_metrics['Price High Pct Change'] >= threshold) & (df_metrics['Price Low Pct Change'] >= threshold ), 'Buy', 'Hold')
    df_metrics['Decision'] = np.where( (df_metrics['Price High Pct Change'] <= -threshold) & (df_metrics['Price Low Pct Change'] <= -threshold ), 'Sell', df_metrics['Decision'])

# df['Price high'] <= -thres and df['Price low'] <= -thres

    return df_metrics

parser = argparse.ArgumentParser()
parser.add_argument('--env', '--env', help="current Env (local | qa | prod)", default='local')
args = parser.parse_args()

env = args.env
if env == 'local':
    data_dir_key_metrics = '../data/17-modeling-prep-key-metrics'
    data_dir_historical = '../data/10-history'
    data_dir_key_metrics_modified = '../data/17.1-modeling-prep-key-metrics'

else:
    data_dir_key_metrics = f'/home/p372-ml-algo-data/17-modeling-prep-financial-growth'
    data_dir_historical = '../data/10-history'
    data_dir_key_metrics_modified = '/home/p372-ml-algo-data/17.1-modeling-prep-key-metrics'


if not os.path.exists(data_dir_key_metrics):
    os.makedirs(data_dir_key_metrics)

if not os.path.exists(data_dir_key_metrics_modified):
    os.makedirs(data_dir_key_metrics_modified)

stocks = stock_list_util.getListOfSandP500()
print(stocks)

i=0

for stock in stocks[0:]:
    i += 1
    print(f'{i}) - {stock}')
    file = data_dir_key_metrics + f'/{stock}.csv'
    df_metrics = pd.read_csv(file)
    #TODO drop unncessary ones
    df_metrics = addColumns(stock, df_metrics)
    file_modified = data_dir_key_metrics_modified + f'/{stock}.csv'
    df_metrics.to_csv(file_modified)


