import requests
from pathlib import Path
DATA_DIR = Path('/', 'tmp', 'nypd-stopandfrsks')
DATA_DIR.mkdir(exist_ok=True, parents=True)



ZIP_URL = 'http://www.nyc.gov/html/nypd/downloads/zip/analysis_and_planning/{year}_sqf_csv.zip'
for year in range(2010, 2016):
    url = ZIP_URL.format(year=year)
    print("Downloading", url)
    resp = requests.get(url)
    fname = DATA_DIR.joinpath('{y}.zip'.format(y=year))
    with fname.open('wb') as wf:
        wf.write(resp.content)
