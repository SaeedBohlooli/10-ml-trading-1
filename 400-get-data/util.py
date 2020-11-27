from yahoo_fin import stock_info as si

def place_value(number):
    return ("{:,.2f}".format(number))

def time_convert(sec):
  mins = sec // 60
  sec = sec % 60
  hours = mins // 60
  mins = mins % 60
  print("Time Lapsed = {0}:{1}:{2}".format(int(hours),int(mins),sec))

def getListOfStocks():
  tickersList = []

  filename = 'nasdaqlisted.txt'
  with open(filename) as f:
    lines = f.readlines()
  for line in lines:
    tickersList.append(line.split('|')[0])

  filename2 = 'otherlisted.txt'
  with open(filename2) as f:
    lines2 = f.readlines()
  for line in lines2:
    tickersList.append(line.split('|')[0])

  return tickersList


# Don't use this, the s and 5 gets updated frequently - may use for backtesting ....
def getListOfSandP500FromCSV():
  filename = 'tickers_s_and_p_500.csv'
  with open(filename) as f:
      tickers = f.readlines()

  tickers = [x.strip() for x in tickers]
  return tickers

def getListOfSandP500():
  stocklist = si.tickers_sp500()
  return stocklist
