"""
Draft code on wrangling NYPD stop frisk data; notes TK

- For all CSV files (previously downloaded) in /tmp/nypd-stopandfrisks:
    - create a new CSV file in which:
        - excess whitespace is trimmed
        - Y/N fields are 'Y' or 'N'
        - less-useful columns are omitted
        - datetime is cleaned via regex and formatted as UTC
        - use-of-force columns consolidated to a Y/N `was_force_used`
        - Convert X/Y to long/lat via "ESRI:102718"
"""

from pathlib import Path
import csv
import re
import pyproj

DERIVED_HEADERS = [ 'datetimestop', 'frisked', 'searched', 'arstmade', 'sumissue',
                    'gun_found', 'other_found','was_force_used', 'forceuse_reason',
                    'ac_ongoing_report', 'ac_miscellaneous', 'longitude', 'latitude',]

STOP_REASON_HEADERS = ['cs_objcs', 'cs_descr', 'cs_casng', 'cs_lkout', 'cs_cloth',
                       'cs_drgtr', 'cs_furtv', 'cs_vcrim', 'cs_bulge', 'cs_other',]

BOILERPLATE_HEADERS = ['race', 'age',  'sex', 'weight', 'year', 'ser_num', 'pct', 'beat', 'sector',
                        'xcoord', 'ycoord', 'addrpct', 'addrnum', 'stname', 'stinter', 'crossst',
                        'premname','arstoffn', 'sumoffen', 'crimsusp', 'detailcm',]

# these are all consolidated under was_force_used
FORCE_HEADERS = ['pf_hands', 'pf_wall', 'pf_grnd', 'pf_drwep', 'pf_ptwep', 'pf_baton', 'pf_hcuff', 'pf_pepsp', 'pf_other']
# consolidated under ac_miscellaneous
MISC_AC_HEADERS = ['ac_assoc', 'ac_cgdir', 'ac_evasv', 'ac_incid', 'ac_other', 'ac_proxm', 'ac_stsnd', 'ac_time']


ALL_HEADERS = DERIVED_HEADERS + STOP_REASON_HEADERS + BOILERPLATE_HEADERS

RAW_DATA_DIR = Path('/', 'tmp', 'nypd-stopandfrsks')
OUTPUT_DIR = Path('data', 'nypd', 'wrangled')
OUTPUT_DIR.mkdir(exist_ok=True, parents=True)

def yes_no(v): # helper method to normalize Y/N/'' columns
    return 'Y' if v == 'Y' else 'N'

# Set up the projection
# http://gis.stackexchange.com/a/181673/37839
NYSP1983_PROJ = pyproj.Proj(init="ESRI:102718", preserve_units=True)
# usage:
# long, lat = NYSP1983_PROJ(x, y, inverse=True)

### the main function
if __name__ == '__main__':

    for data_filename in RAW_DATA_DIR.glob('*.csv'):
        year = re.match(r'^\d{4}', data_filename.name).group()
        output_filename = OUTPUT_DIR.joinpath('stops-and-frisks--%s.csv' % year)
        print("Wrangling", data_filename, 'into', output_filename)
        wf = output_filename.open('w')
        wcsv = csv.DictWriter(wf, fieldnames=ALL_HEADERS)
        wcsv.writeheader()

        # only 2011.csv has windows-1252 instead of ascii encoding,
        # but we open all files as windows-1252 just to be safe
        with data_filename.open("r", encoding='windows-1252') as rf:
            for i, row in enumerate(csv.DictReader(rf)):
                if i % 10000 == 0:
                    print("...row", i)

                row = {k.lower(): v.strip() for k, v in row.items()} # downcase headers,  strip whitespace
                x = {h: row[h] for h in BOILERPLATE_HEADERS}
                x['frisked'] = yes_no(row['frisked'])
                x['searched'] = yes_no(row['searched'])
                x['arstmade'] = yes_no(row['arstmade'])
                x['sumissue'] = yes_no(row['sumissue'])
                # only later report years have 'force_use' column
                x['forceuse_reason'] = row.get('forceuse')

                # Weapon found?
                x['gun_found'] = next((row[c] for c in ['asltweap', 'machgun', 'pistol', 'riflshot'] if row[c] == 'Y'), 'N')
                x['other_found'] = next((row[c] for c in ['contrabn', 'knifcuti', 'othrweap'] if row[c] == 'Y'), 'N')
                # additional circumstances
                # "ac_ongoing_report"
                # - ac_inves - ADDITIONAL CIRCUMSTANCES - ONGOING INVESTIGATION
                # - ac_rept - ADDITIONAL CIRCUMSTANCES - REPORT BY VICTIM/WITNESS/OFFICER
                x['ac_ongoing_report'] = next((row[c] for c in ['ac_inves', 'ac_rept'] if row[c] == 'Y'), 'N')

                # "ac_miscellaneous"
                x['ac_miscellaneous'] = next((row[c] for c in MISC_AC_HEADERS if row[c] == 'Y'), 'N')

                # Reason for stop - let's record all of them
                for c in STOP_REASON_HEADERS:
                    x[c] = yes_no(row[c])

                # Was force used
                x['was_force_used'] = next((row[c] for c in FORCE_HEADERS if row[c] == 'Y'), 'N')

                # Fix time, which can come as:
                # 5 (00:05)
                # 14 (00:14)
                # 318 (03:18)
                # 15:12 (15:12)
                _time = row['timestop']
                if len(_time) >= 3:
                    timestop = "{hrs}:{min}".format(hrs=_time[0:2].rjust(2, '0'), min=_time[2:].rjust(2, '0'))
                else:
                    # just pad the string and prepend 00 as the hours value
                    timestop = "{hrs}:{min}".format(hrs='00', min=_time.rjust(2, '0'))

                # Fix date
                # 7042014 - 2014-07-04
                # 12012011 - 2011-12-01
                datestop = row['datestop'].rjust(8, '0')
                x['datetimestop'] = '{yr}-{mth}-{day} {time}'.format(yr=datestop[-4:], mth=datestop[0:2], day=datestop[2:4], time=timestop)

                # Project X, Y to longitude, latitude
                if row['xcoord'] and row['ycoord']:
                    lnglat = NYSP1983_PROJ(int(row['xcoord']), int(row['ycoord']), inverse=True)
                    x['longitude'], x['latitude'] = [round(c, 5) for c in lnglat]
                # finally, write the row
                wcsv.writerow(x)
