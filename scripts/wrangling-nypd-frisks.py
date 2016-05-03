"""
Draft code on trimming/cleaning up NYPD stop frisk data
"""


from pathlib import Path
import csv
import re

DERIVED_HEADERS = [
    'datetimestop',
    'frisked', 'searched', 'arstmade', 'sumissue',
    'gun_found', 'other_found',
    'was_force_used', 'forceuse_reason',
    'ac_ongoing_report', 'ac_miscellaneous']

STOP_REASON_HEADERS = ['cs_objcs', 'cs_descr', 'cs_casng', 'cs_lkout', 'cs_cloth', 'cs_drgtr',
                       'cs_furtv', 'cs_vcrim', 'cs_bulge', 'cs_other']

BOILERPLATE_HEADERS = ['race', 'age',  'sex', 'weight',
    'year', 'ser_num', 'pct', 'beat', 'sector',
    'xcoord', 'ycoord',
    'addrpct', 'addrnum', 'stname', 'stinter', 'crossst', 'premname',
    'arstoffn', 'sumoffen', 'crimsusp', 'detailcm',
    ]

ALL_HEADERS = DERIVED_HEADERS + STOP_REASON_HEADERS + BOILERPLATE_HEADERS

# these are all consolidated under was_force_used
FORCE_HEADERS = ['pf_hands', 'pf_wall', 'pf_grnd', 'pf_drwep', 'pf_ptwep', 'pf_baton', 'pf_hcuff', 'pf_pepsp', 'pf_other']
# consolidated under ac_miscellaneous
MISC_AC_HEADERS = ['ac_assoc', 'ac_cgdir', 'ac_evasv', 'ac_incid', 'ac_other', 'ac_proxm', 'ac_stsnd', 'ac_time']

DATA_DIR = Path('raw')
OUTPUT_DIR = Path('wrangled')
OUTPUT_DIR.mkdir(exist_ok=True, parents=True)

def yes_no(v):
    return 'Y' if v == 'Y' else 'N'

for data_filename in DATA_DIR.glob('*.csv'):
    year = re.match(r'^\d{4}', data_filename.name).group()
    output_filename = OUTPUT_DIR.joinpath('%s.csv' % year)
    print("Wrangling", data_filename, 'into', output_filename)
    wf = output_filename.open('w')
    wcsv = csv.DictWriter(wf, fieldnames=ALL_HEADERS)
    wcsv.writeheader()

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

            # ac_ongoing_report
            # - ac_inves - ADDITIONAL CIRCUMSTANCES - ONGOING INVESTIGATION
            # - ac_rept - ADDITIONAL CIRCUMSTANCES - REPORT BY VICTIM/WITNESS/OFFICER
            x['ac_ongoing_report'] = next((row[c] for c in ['ac_inves', 'ac_rept'] if row[c] == 'Y'), 'N')

            # ac_miscellaneous
            x['ac_miscellaneous'] = next((row[c] for c in MISC_AC_HEADERS if row[c] == 'Y'), 'N')

            # Reason for stop
            for c in STOP_REASON_HEADERS:
                x[c] = yes_no(row[c])

            # Was force used
            x['was_force_used'] = next((row[c] for c in FORCE_HEADERS if row[c] == 'Y'), 'N')

            # Fix time
            _time = row['timestop']
            if len(_time) >= 3:
                timestop = "{hrs}:{min}".format(hrs=_time[0:2].rjust(2, '0'), min=_time[2:].rjust(2, '0'))
            else:
                timestop = "{hrs}:{min}".format(hrs='00', min=_time[2:].rjust(2, '0'))

            # Fix date
            datestop = row['datestop'].rjust(8, '0')
            x['datetimestop'] = '{yr}-{mth}-{day} {time}'.format(yr=datestop[-4:], mth=datestop[0:2], day=datestop[2:4], time=timestop)


            # finally, write the row
            wcsv.writerow(x)






"""
Notes for further discussion

File 2011.csv
UnicodeDecodeError: 'utf-8' codec can't decode byte 0xb0 in position 1614: invalid start byte



for c in [x for x in df.columns if 'cs_' in x]:
   ....:     print(df[c].value_counts())
   ....:
N    586312
Y     14973
Name: cs_objcs, dtype: int64
N    504924
Y     96361
Name: cs_descr, dtype: int64
N    421058
Y    180227
Name: cs_casng, dtype: int64
N    495454
Y    105831
Name: cs_lkout, dtype: int64
N    572881
Y     28404
Name: cs_cloth, dtype: int64
N    551471
Y     49814
Name: cs_drgtr, dtype: int64
N    302716
Y    298569
Name: cs_furtv, dtype: int64
N    542702
Y     58583
Name: cs_vcrim, dtype: int64
N    549191
Y     52094
Name: cs_bulge, dtype: int64
N    490692
Y    110593
Name: cs_other, dtype: int64
"""
