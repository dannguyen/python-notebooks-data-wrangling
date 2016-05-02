"""
for the dataextraction of the FBIUCR06 data xls spreadsheet
"""


from os import makedirs
from os.path import join
from xlrd import open_workbook
import csv
import re
INPUT_FNAME = join('data', 'fbi', 'raw', '06tbl08.xls')
OUTPUT_DIR = join('data', 'fbi', 'extracted')
makedirs(OUTPUT_DIR, exist_ok=True)
OUTPUT_NAME = join(OUTPUT_DIR, '06tbl08.csv')



book = open_workbook(INPUT_FNAME)
sheet = book.sheets()[0]

first_col = sheet.col_values(0)
# get position of headers row
headers_idx = first_col.index('State')
# get position of first numbered footnote
footnotes_idx = next(i for i, val in enumerate(first_col) if re.match('^\d', val))
# get only rows between headers and footnotes
datarows = [sheet.row_values(i) for i in range(sheet.nrows)][headers_idx+1:footnotes_idx]


wf = open(OUTPUT_NAME, 'w')
csvf = csv.writer(wf)
csvf.writerow(sheet.row_values(headers_idx))



statename = ""
for i, row in enumerate(datarows):
    if row[0] != '':
        statename = row[0]
    row[0] = statename
    csvf.writerow(row)

wf.close()
