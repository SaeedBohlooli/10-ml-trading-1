from yahoo_fin import stock_info as si

def getListOfSandP500():
  stocklist = si.tickers_sp500()
  return stocklist

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