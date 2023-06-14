import os
import sys
import subprocess
import string
import random
import csv
import pandas as pd
import json

pd.set_option('display.max_columns', None)

df = pd.read_table('sitvit_geno_final.tsv', index_col=False, dtype={'SpoligoType': 'string'},
                   usecols=['FilePath','RunName', 'SpoligoType', 'MiruType', 'Lineage'])

spol = df["SpoligoType"]

print(df['FilePath'])

for i in range(len(spol)):
    print(spol[i])

f = open('./results/tbprofiler.results.json')
# returns JSON object as
# a dictionary
data = json.load(f)
dir_path = r'../../'
res = []
# Iterating through the json
# list
for file in os.listdir(dir_path):
    # check only text files
    if file.endswith('.json'):
    #if file.endswith(('.fasta', '.fna')):
        res.append(file)
print(res)

print(len(data['dr_variants']))
print(data['drtype'])

# Closing file
f.close()
