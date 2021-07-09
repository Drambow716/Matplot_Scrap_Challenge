import pandas as pd
from tabulate import tabulate as tlb

df = pd.read_csv("IMDB_Crime_100.csv")

# Transofrming Ratings to Float
df['Ratings'] = pd.to_numeric(df['Ratings'])

# Transofrming Durations to Float
df['Durations'] = df['Durations'].str.replace(" min","")
df['Durations'] = pd.to_numeric(df['Durations'],downcast="float")

# Normalized_max_min
df['R/D'] = df['Ratings'] / df['Durations']
df['normalized_max_min'] = (df['R/D']-df['R/D'].min())/(df['R/D'].max()-df['R/D'].min())

# Normalized_mean