from pathlib import Path
from datetime import datetime
import re
import csv
import requests

DATA_URL = 'https://data.cityofnewyork.us/api/views/hyij-8hr7/rows.csv?accessType=DOWNLOAD'
DATA_DIR = Path('data', 'nypd', 'extracted')
DATA_DIR.mkdir(exist_ok=True, parents=True)

OUTPUT_HEADERS = ['occurrence_date', 'object_id', 'identifier', 'compstat_date',
                  'offense', 'sector', 'precinct', 'borough', 'jurisdiction',
                  'xcoord', 'ycoord', 'latitude', 'longitude']
OUTPUT_FILENAME = DATA_DIR.joinpath('bulk-data-nypd-7-major-felonies.csv')


print("Downloading", DATA_URL)
resp = requests.get(DATA_URL)
datarows = list(csv.DictReader(resp.text.splitlines()))

wf = OUTPUT_FILENAME.open('w')
outcsv = csv.DictWriter(wf, fieldnames=OUTPUT_HEADERS)
outcsv.writeheader()

for d in datarows:
    x = {}
    # fill in the boilerplate
    x['borough'] = d['Borough']
    x['identifier'] = d['Identifier']
    x['jurisdiction'] = d['Jurisdiction']
    x['object_id'] = d['OBJECTID']
    x['offense'] = d['Offense']
    x['precinct'] = d['Precinct']
    x['sector'] = d['Sector']
    x['xcoord'] = d['XCoordinate']
    x['ycoord'] = d['YCoordinate']

    # now fill in the derived values
    # some Occurrence Date values are blank
    try:
        x['occurrence_date'] = datetime.strptime(d['Occurrence Date'],
                                            '%m/%d/%Y %I:%M:%S %p').strftime('%Y-%m-%d %H:%M:%S')
    except ValueError as err:
        x['occurrence_date'] = None


    # Some Compstat values are blank
    # apparently compstat date is different than occurence date...
    try:
        x['compstat_date'] = datetime(int(d['CompStat Year']),
                                      int(d['CompStat Month']),
                                      int(d['CompStat Day']) ).strftime('%Y-%m-%d')
    except ValueError as err:
        x['compstat_date'] = None

    # Now try to split the Location 1 value into latitude/longitude
    _mtch = re.search(r'\((.+?), (.+?)\)', d['Location 1'])
    if _mtch:
        x['latitude'], x['longitude'] = _mtch.groups()
    else:
        x['latitude'] = x['longitude'] = None

    # finally, write it to the csv
    outcsv.writerow(x)

wf.close()
