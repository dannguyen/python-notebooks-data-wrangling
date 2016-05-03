from pathlib import Path
import csv
HEADERS_TO_OMIT = ["recstat", "inout", "trhsloc", "perobs", "typeofid","explnstp",
"othpers","compyear", "comppct", "adtlrept", "radio", "repcmd",
"revcmd", "offverb", "offshld", "dob","othfeatr", "addrtyp", "rescode",
"premtype", "state", "zip", "dettypcm", "linecm"]

data_file = Path('2010.csv')
out_file = Path('2010-cleaned.csv')
with data_file.open("r") as rf:
    datarows = list(csv.DictReader(rf))


newheaders = list(set(datarows[0].keys()) - set(HEADERS_TO_OMIT))

with out_file.open('w') as wf:
    wcsv = csv.DictWriter(wf, fieldnames=newheaders, extrasaction='ignore')
    wcsv.writeheader()
    wcsv.writerows(datarows)



