import json
import os
import sys

import pandas as pd

country = []
df_csv_spol = pd.read_table('fastasimpi1000.csv', index_col=False, sep=",")

for i in range(len(df_csv_spol["RunName"])):
    print(df_csv_spol["RunName"][i][:13])
    os.system('datasets summary genome accession ' + df_csv_spol["RunName"][i][:13] + '>> test.json')
    with open("test.json", "r") as f:
        data = json.load(f)
        try:
            if data["reports"][0]["assembly_info"]["biosample"]["attributes"][13]["name"] == 'geo_loc_name':
                country.append(data["reports"][0]["assembly_info"]["biosample"]["attributes"][13]["value"])
            elif data["reports"][0]["assembly_info"]["biosample"]["attributes"][12]["name"] == 'geo_loc_name':
                country.append(data["reports"][0]["assembly_info"]["biosample"]["attributes"][12]["value"])
            elif data["reports"][0]["assembly_info"]["biosample"]["attributes"][11]["name"] == 'geo_loc_name':
                country.append(data["reports"][0]["assembly_info"]["biosample"]["attributes"][11]["value"])
            elif data["reports"][0]["assembly_info"]["biosample"]["attributes"][10]["name"] == 'geo_loc_name':
                country.append(data["reports"][0]["assembly_info"]["biosample"]["attributes"][10]["value"])
            else:
                country.append("NF")
        except:
            country.append('ND')

        f.close()
    os.remove("test.json")

df_csv_spol['Country'] = country

print(df_csv_spol['Country'])

df_csv_spol.to_csv("newsitvitgenoentry.csv", index=False)