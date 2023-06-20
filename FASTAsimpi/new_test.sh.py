# launch tb-profiler env
import os
import sys
import subprocess
import string
import random
import csv
import pandas as pd
import json
from Bio import SeqIO
import time

pd.options.mode.chained_assignment = None
# parser.add_argument('-i', '--in', nargs='+', default=[])
if not os.path.exists("sitvit_geno/"):
    os.makedirs("sitvit_geno/")
else:
    for filename in os.listdir("sitvit_geno/"):
        os.remove("sitvit_geno/" + filename)

if os.path.exists("./sitvit_geno_final.tsv"):
    os.remove("./sitvit_geno_final.tsv")
    g = open("./sitvit_geno_final.tsv", 'w')
    g.write('')
    g.write('FilePath\tFlags\tRunName\tSpoligoType(MiruHero)\tMiruType\tLineage(MiruHero)\n')
    g.close()
else:
    g = open("./sitvit_geno_final.tsv", 'w')
    g.write('')
    g.write('FilePath\tFlags\tRunName\tSpoligoType(MiruHero)\tMiruType\tLineage(MiruHero)\n')
    g.close()

bashfile = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
bashfile = '/tmp/' + bashfile + '.sh'

miru_Order = ['miru02', 'miru04', 'miru10', 'miru16', 'miru20', 'miru23', 'miru24', 'miru26', 'miru27', 'miru31',
              'miru39', 'miru40', 'Mtub04', 'ETRC', 'Mtub21', 'Qub11b', 'ETRA', 'Mtub29', 'Mtub30', 'ETRB', 'Mtub34',
              'Mtub39', 'QUB26', 'QUB4156']

ancien = 'Mtub04', 'ETRC', 'Mtub21', 'Qub11b', 'ETRA', 'Mtub29', 'Mtub30', 'ETRB', 'Mtub34', 'Mtub39', 'QUB26', 'QUB4156'
new = 'ETR-A', 'ETRB', 'ETR-C', 'QUB-11b', 'QUB-26', 'QUB-4156', 'Mtub04', 'Mtub21', 'Mtub29', 'Mtub30', 'Mtub34', 'Mtub39'

# folder path
dir_path_sum_tsv = r'sitvit_geno/'

dir_path_fasta = r'./'

# list to store files
res_sum_tsv = []
res_fasta = []
lineages = []
resistance = []
spol_mirureader = []

debut = time.perf_counter()
# Iterate directory
for file in os.listdir(dir_path_fasta):
    # check only text files
    if file.endswith(('.fasta', '.fna')):
        res_fasta.append(file)
print(res_fasta)

f = open(bashfile, 'w')
s = """
for i in *.fasta;
    do
        MiruHero -m24 $i -o ./sitvit_geno;
done
"""

# ~/miniconda3/pkgs/miru-hero-0.10.0-pyh5e36f6f_0/python-scripts/MiruHero -m24 $i -o ./sitvit_geno;


# launch mirureader
# s = os.popen("cat ~/Documents/simpyTB/fasta_files/FASTAsimpi/sitvit_geno/GCA*.summary.tsv").read()
# print(s)
f.write(s)
f.close()
os.chmod(bashfile, 0o755)
bashcmd = bashfile
for arg in sys.argv[1:]:
    bashcmd += ' ' + arg
subprocess.call(bashcmd, shell=True)

for file in os.listdir(dir_path_sum_tsv):
    # check only text files
    if file.endswith('.summary.tsv'):
        res_sum_tsv.append(file)
print(res_sum_tsv)

# g = open("./sitvit_geno_final.tsv", 'r+')


for i in range(len(res_sum_tsv)):
    with open("./sitvit_geno/" + res_sum_tsv[i] + "", "r+") as myfile:
        content = myfile.readlines()
        with open("./sitvit_geno_final.tsv", "a") as outfile:
            if len(content) == 2:
                outfile.write(content[1])
            else:
                continue
    outfile.close()

pd.set_option('display.max_columns', None)

df = pd.read_table('sitvit_geno_final.tsv', index_col=False, dtype={'SpoligoType(MiruHero)': 'string'},
                   usecols=['FilePath', 'RunName', 'SpoligoType(MiruHero)', 'MiruType', 'Lineage(MiruHero)'])

if os.path.exists("spo_gca.out"):
    os.remove("spo_gca.out")

g = open("./spo_gca.out", 'w')
g.write('')
g.write('FilePath\tSpoligoType\tSpoligoType(Spotyping)\n')
g.close()

for i in range(len(df)):
    print(res_fasta[i])
    # check only text files
    os.system('python3 MIRUReader/MIRUReader.py -p mirus -r ' + df.loc[i, 'FilePath'] + '> miru.txt')
    os.system('tb-profiler profile -f' + df.loc[i, 'FilePath'] + '')
    os.system('python3 SpoTyping/SpoTyping-v3.0-commandLine/SpoTyping.py --noQuery --seq ' + df.loc[
        i, 'FilePath'] + ' -o spo_gca.out')

    df3 = pd.read_table('miru.txt', index_col=False)

    print(df3)

    spol_mirureader.append(df3.iloc[0][1:].to_numpy())

    # f = open('./results/tbprofiler.results.json')
    # data = json.load(f)
    # time.sleep(2)

    with open("./results/tbprofiler.results.json", "r") as f:
        data = json.load(f)

        if len(data['sublin']) == 0:
            lineages.append('ND')
        else:
            lineages.append(data['sublin'])

        if len(data['dr_variants']) == 0:
            resistance.append('ND')

        elif len(data['dr_variants']) > 0 and data['drtype'] == 'Sensitive':
            resistance.append("" + data['dr_variants'][0]['annotation'][0]['drug'] + "(S)")

        elif len(data['dr_variants']) > 0 and data['drtype'] == 'Resistant':
            resistance.append("" + data['dr_variants'][0]['annotation'][0]['drug'] + "(R)")

        elif len(data['dr_variants']) > 0 and data['drtype'] == 'Other':
            resistance.append("" + data['dr_variants'][0]['annotation'][0]['drug'] + "(O)")

        elif len(data['dr_variants']) > 0 and len(data['drtype']) == 0:
            resistance.append(data['dr_variants'][0]['annotation'][0]['drug'])

        f.close()
    os.remove('./results/tbprofiler.results.json')

df2 = pd.read_table('spo_gca.out', index_col=False, dtype={'SpoligoType(Spotyping)': 'string'}, )
# pd.merge(df, df2[["SpoligoType(Spotyping)"]])
df.insert(loc=3, column='SpoligoType(Spotyping)', value=df2["SpoligoType(Spotyping)"])
df['Lineages'] = lineages
df['Resistance'] = resistance

for i in range(len(df)):
    mylist = df['MiruType'][i]
    myorder = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 16, 19, 13, 15, 22, 23, 12, 14, 17, 18, 20, 21]
    orderMIRUREader = [1, 4, 6, 7, 9, 15, 16, 17, 18, 20, 24, 5, 11, 14, 3, 10, 22, 23, 2, 8, 12, 13, 19, 21]
    mylist = [mylist[i] for i in myorder]
    s = ''.join(mylist)
    df['MiruType'][i] = s

print(df)

fin = time.perf_counter()
print(f" Le script à tourné durant {fin - debut:0.4f} secondes")
print(df2)
print(spol_mirureader)

for x in range(len(spol_mirureader)):
    for y in range(len(spol_mirureader[x])):
        if spol_mirureader[x][y] == 'ND':
            spol_mirureader[x][y] = '-'
        elif spol_mirureader[x][y] == 10:
            spol_mirureader[x][y] = 'A'
        elif spol_mirureader[x][y] == 11:
            spol_mirureader[x][y] = 'B'
        elif spol_mirureader[x][y] == 12:
            spol_mirureader[x][y] = 'C'
        elif spol_mirureader[x][y] == 13:
            spol_mirureader[x][y] = 'D'
        elif spol_mirureader[x][y] == 14:
            spol_mirureader[x][y] = 'E'
        elif spol_mirureader[x][y] == 15:
            spol_mirureader[x][y] = 'F'
        elif str(spol_mirureader[x][y]).count('s') > 0:
            # string.__contains__('s')
            index = str(spol_mirureader[x][y]).find('s')
            spol_mirureader[x][y] = spol_mirureader[x][y][:index]

        # else:
        #     print(spol_mirureader[x][y])
        #     print(spol_mirureader[x][y].dtype)
        #     print(spol_mirureader[x][y].replace('s', ''))

print(type(spol_mirureader))

values = ''.join([str(v) for v in spol_mirureader])
values2 = values.replace("'", '')
values2 = values2.replace(" ", "")
df["new_col"] = pd.Series(values2)
print(type(values2))

testy = values2.split("]")
print("testy", testy)
# print("value:", values)
# print("value2:", values2)

# df.insert(loc=4, column='SpoligoType(mirureader)', value=values2.strip())
print(df)
