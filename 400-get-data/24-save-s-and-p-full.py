import pandas_datareader as web
import numpy as np

import os
import time
import datetime
import util
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('--env', '--env', help="current Env (local | qa | prod)", default='local')
args = parser.parse_args()

env = args.env

if env == 'local':
    output_path = os.path.join('..', 'data', '10-history')

else:
    output_path = "/home/p372-ml-algo-data/10-history"

try:
    os.makedirs(output_path)
except OSError:
    print("Creation of the directory %s failed" % output_path)


def save_in_files(tickers):
    i = 0
    for t in tickers:
        i += 1
        start_timer_1 = time.time()

        try:
            df = web.DataReader(t, data_source='yahoo', start=start_date, end=end_date)
            print(f'{i})  {t}  {start_date}, {end_date} spentTimeInSec: {time.time() - start_timer_1}, len= {len(df)}')
            if (len(df) > 200):
                # we save if there is enough data ...
                df.to_csv(f'{output_path}/{t}.csv')
            else:
                print(f'Not enough data for {t}, we dont save it, days: {len(df)}')
                not_saved.append(t)
        except Exception as exception:
            print(f'{i})  {t}  {end_date}  Error  ')
            print(exception)


# get data for last 16 yrs
if env =='local':
    start_date = datetime.datetime.now() - datetime.timedelta(days=365 * 40)
else:
    start_date = datetime.datetime.now() - datetime.timedelta(days=365 * 16)
end_date = datetime.date.today()

not_saved=[]
tickersList =[]

s_P_500 = util.getListOfSandP500()
tickersList = tickersList + s_P_500
#tickersList = ['^GSPC'] + tickersList
# debug tickersList=['JNJ']
i=0
for ticker in tickersList:
    i += 1
    print(f'{i} - {ticker}')

save_in_files(tickersList)

f = open(f'{output_path}/{end_date}-s-and-p-500.ok', "w")
f.write(str(end_date))
f.close()

print(f'INFO s and 500 saved for {end_date}')
