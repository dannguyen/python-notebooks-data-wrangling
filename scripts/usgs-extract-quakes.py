from pathlib import Path
from copy import copy
import requests
# Example URL
# http://earthquake.usgs.gov/fdsnws/event/1/query.csv?starttime=2000-01-01%2000:00:00
#  &endtime=2015-12-31%2023:59:59&maxlatitude=50&minlatitude=24.6&maxlongitude=-65
#  &minlongitude=-125&minmagnitude=3&eventtype=earthquake&orderby=time-asc
START_YEAR = 2012
END_YEAR = 2015

# via USGS
# http://earthquake.usgs.gov/earthquakes/search/

BASE_ENDPOINT = 'http://earthquake.usgs.gov/fdsnws/event/1/query.csv'
BASE_PARAMS = {
    'eventtype'   : 'earthquake',
    'orderby'     : 'time-asc',
    'starttime'   : '{}-01-01 00:00:00'.format(START_YEAR),
    'endtime'     : '{}-12-31 23:59:59'.format(END_YEAR),
    'minmagnitude': 3,
    'maxlatitude' : 50,
    'minlatitude' : 24.6,
    'maxlongitude': -65,
    'minlongitude': -125
}

DATA_DIR = Path('data', 'usgs', 'raw')
DATA_DIR.mkdir(exist_ok=True, parents=True)


print("Contacting", BASE_ENDPOINT)
# url is not resolved until we get the response...
resp = requests.get(BASE_ENDPOINT, params=BASE_PARAMS)
print("Received response", resp.status_code)
print('from:', resp.url)

if resp.status_code == 200:
    fname = DATA_DIR.joinpath('us-earthquakes-{yra}-{yrb}.csv'.format(yra=START_YEAR, yrb=END_YEAR))
    with fname.open('w') as wf:
        print("Saving:", fname)
        wf.write(resp.text)
else:
    print("Error", resp.url)
    print(resp.text)

