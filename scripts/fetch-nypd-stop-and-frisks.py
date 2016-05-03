from pathlib import Path
from shutil import unpack_archive
import requests
START_YEAR = 2010
END_YEAR = 2015
RAW_DATA_DIR = Path('/', 'tmp', 'nypd-stopandfrsks')
RAW_DATA_DIR.mkdir(exist_ok=True, parents=True)

ZIP_URL = 'http://www.nyc.gov/html/nypd/downloads/zip/analysis_and_planning/{year}_sqf_csv.zip'
for year in range(2010, END_YEAR + 1):
    url = ZIP_URL.format(year=year)
    print("Downloading", url)
    resp = requests.get(url)
    fname = RAW_DATA_DIR.joinpath('{y}.zip'.format(y=year))
    with fname.open('wb') as wf:
        wf.write(resp.content)
    # unzip to the RAW_DATA_DIR
    unpack_archive(str(fname), extract_dir=str(RAW_DATA_DIR))
