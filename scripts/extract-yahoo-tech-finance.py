from pathlib import Path
import requests
BASE_URL='http://real-chart.finance.yahoo.com/table.csv?s={ticker_symbol}&a=00&b=1&c=1900&d=04&e=1&f=2016&g=d&ignore=.csv'
TICKERS = ['FB', 'YHOO', 'MSFT', 'GOOG', 'YELP', 'DATA', 'LNKD', 'BOX', 'CRM',
           'TWTR', 'SQ', 'AMZN', 'GRPN', 'ZNGA', 'P', 'EBAY', 'PYPL', 'NFLX']
DATA_DIR = Path('data', 'financial', 'raw')
DATA_DIR.mkdir(exist_ok=True)


for t in TICKERS:
    print("Downloading ticker:", t)
    url = BASE_URL.format(ticker_symbol=t)
    resp = requests.get(url)
    fpath = DATA_DIR.joinpath(t + '.csv')
    fpath.write_text(resp.text)
    print("...Downloaded to", fpath)
