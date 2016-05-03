
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
