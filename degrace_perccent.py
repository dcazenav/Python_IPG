#import libraries
import pandas as pd

#read files
df1 = pd.read_csv('Classeur_Damien_Degrace.csv')
#df2 = pd.read_csv('Second_week.csv')

#Create new file and save results
column_names = ["Genus", "name"]
df3 = pd.DataFrame(columns = column_names)
#df3[['id', 'name']] = df1[['id', 'name']]
df3['%difference_week1vsweek2'] = (df1['total_orderCount']-df2['total_orderCount'])/df2['total_orderCount']*100
print(df3)

df3.to_csv("output.csv")

# CRL	GRL	FH	ALL
# 522977	1238530	5227332	2288839
