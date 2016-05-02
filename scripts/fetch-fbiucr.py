from os import makedirs
from os.path import join
import requests
DATA_DIR = join('data', 'fbi', 'raw', 'ucr-cius')

# https://www.fbi.gov/about-us/cjis/ucr/crime-in-the-u.s/1995/95sec2.pdf
# https://www.fbi.gov/about-us/cjis/ucr/crime-in-the-u.s/1995/95sec6.pdf

# https://www.fbi.gov/about-us/cjis/ucr/crime-in-the-u.s/1996/96sec2.pdf
# https://www.fbi.gov/about-us/cjis/ucr/crime-in-the-u.s/1996/96sec6.pdf

# https://www.fbi.gov/about-us/cjis/ucr/crime-in-the-u.s/1997/97sec2.pdf
# https://www.fbi.gov/about-us/cjis/ucr/crime-in-the-u.s/1997/97sec6.pdf

# https://www.fbi.gov/about-us/cjis/ucr/crime-in-the-u.s/1998/98sec2.pdf
# https://www.fbi.gov/about-us/cjis/ucr/crime-in-the-u.s/1998/98sec6.pdf

# https://www.fbi.gov/about-us/cjis/ucr/crime-in-the-u.s/1999/table8_leos_pop.over99.xls
# https://www.fbi.gov/about-us/cjis/ucr/crime-in-the-u.s/1999/99sec6.pdf

# https://www.fbi.gov/about-us/cjis/ucr/crime-in-the-u.s/2000/table8_leos_pop.-over00.xls
# https://www.fbi.gov/about-us/cjis/ucr/crime-in-the-u.s/2000/00sec6.pdf


# https://www.fbi.gov/about-us/cjis/ucr/crime-in-the-u.s/2001/01sec6.pdf
# https://www.fbi.gov/about-us/cjis/ucr/crime-in-the-u.s/2001/table8apop.under01.xls
# https://www.fbi.gov/about-us/cjis/ucr/crime-in-the-u.s/2001/table11a_leosrural01.xls
# https://www.fbi.gov/about-us/cjis/ucr/crime-in-the-u.s/2001/table8_leospop.over01.xls


# https://www.fbi.gov/about-us/cjis/ucr/crime-in-the-u.s/2002/table8_offenses_pop.over02.xls
# https://www.fbi.gov/about-us/cjis/ucr/crime-in-the-u.s/2002/table8a_pop.under02.xls
# https://www.fbi.gov/about-us/cjis/ucr/crime-in-the-u.s/2002/table11b_leos_agency02.xls
# https://www.fbi.gov/about-us/cjis/ucr/crime-in-the-u.s/2002/table11a_leos_rural02.xls


# https://www.fbi.gov/about-us/cjis/ucr/crime-in-the-u.s/2003/table8_known_leos03.xls
# https://www.fbi.gov/about-us/cjis/ucr/crime-in-the-u.s/2003/table8A_03.xls
# https://www.fbi.gov/about-us/cjis/ucr/crime-in-the-u.s/2003/table10A_03.xls
# https://www.fbi.gov/about-us/cjis/ucr/crime-in-the-u.s/2003/table11A_agency03.xls


# https://www2.fbi.gov/ucr/cius_04/documents/04tbl08a.xls
# https://www2.fbi.gov/ucr/cius_04/xl/04tbl08aux.xls
# https://www2.fbi.gov/ucr/cius_04/documents/04tbl10a.xls
# https://www2.fbi.gov/ucr/cius_04/documents/04tbl11a.xls


# {
#     '',
#     'https://www2.fbi.gov/ucr/cius_04/xl/04tbl08aux.xls'
# }

# {
#     'url': 'https://www2.fbi.gov/ucr/cius{year}/documents/cius{year}downloadablefiles.zip',
#     'start_year': 2006,
#     'end_year': 2009
# },

# {
#     'url': 'https://www.fbi.gov/about-us/cjis/ucr/crime-in-the-u.s/{year}/crime-in-the-u.s.-{year}/CIUS{year}downloadablefiles.zip',
#     'start_year': 2010,
#     'end_year': 2011
# }

# {
#     'url': 'https://www.fbi.gov/about-us/cjis/ucr/crime-in-the-u.s/{year}/crime-in-the-u.s.-{year}/resource-pages/cius{year}downloadablefiles.zip',
#     'start_year': 2012,
#     'end_year': 2012
# },
# {
#     'url': 'https://www.fbi.gov/about-us/cjis/ucr/crime-in-the-u.s/{year}/crime-in-the-u.s.-{year}/resource-pages/downloads/cius{year}downloadablefiles.zip',
#     'start_year': 2013,
#     'end_year': 2014
# }




# https://www.fbi.gov/about-us/cjis/ucr/crime-in-the-u.s/2012/crime-in-the-u.s.-2012/resource-pages/cius2012downloadablefiles.zip


# https://www.fbi.gov/about-us/cjis/ucr/crime-in-the-u.s/2010/crime-in-the-u.s.-2010/CIUS2010downloadablefiles.zip




f = FORMAT_A

for year in range(f['start_year'], f['end_year'] + 1):
    url = f['url'].format(year=year)
    print("Downloading", url)
    resp = requests.get(url)
    output_dir = join(DATA_DIR, str(year))
    makedirs(output_dir, exist_ok=True)
    output_name = join(output_dir, '{yr}.zip'.format(yr=year))
    with open(output_name, 'wb') as wf:
        wf.write(resp.content)
        print("Saved", output_name)
