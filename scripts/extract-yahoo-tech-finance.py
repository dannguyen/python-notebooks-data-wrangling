from pathlib import Path
import requests
BASE_URL='http://real-chart.finance.yahoo.com/table.csv?s={ticker_symbol}&a=00&b=1&c=1900&d=04&e=30&f=2016&g=d&ignore=.csv'
TICKERS = ['AAPL', 'AMZN', 'BABA', 'BIDU', 'BOX', 'CRM', 'CSCO', 'DATA',
           'EBAY', 'EXPE', 'FB', 'FIT', 'GOOG', 'GPRO', 'GRPN', 'GRUB',
           'HPQ', 'HUBS', 'IBM', 'LNKD', 'MSFT', 'NFLX', 'ORCL', 'P', 'PCLN',
           'PYPL', 'RENN', 'SQ', 'TWTR', 'YELP', 'YHOO', 'YNDX', 'ZEN', 'ZNGA']

DATA_DIR = Path('data', 'financial', 'raw', 'companies')
DATA_DIR.mkdir(exist_ok=True)

for t in TICKERS:
    print("Downloading ticker:", t)
    url = BASE_URL.format(ticker_symbol=t)
    resp = requests.get(url)
    fpath = DATA_DIR.joinpath(t + '.csv')
    fpath.write_text(resp.text)
    print("...Downloaded to", fpath)
