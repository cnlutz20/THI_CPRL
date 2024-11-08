
# %%
# Importing basic Python modules

import os, sys, json, datetime  # Provides OS-dependent functionality, system-specific parameters, JSON handling, and date/time manipulation
import pandas as pd             # Provides data structures and data analysis tools
import numpy as np              # Supports large, multi-dimensional arrays and matrices
import requests
import time
import glob
import re
from tqdm import tqdm
import shutil

# &&



os.chdir(r'C:\Users\clutz\OneDrive - THE HUNT INSTITUTE\Documents\Data\surveys\survey files to clean up\edited')
edited_files = glob.glob('*')


file = r"C:\Users\clutz\OneDrive - THE HUNT INSTITUTE\Documents\Data\state_trends_data_sources.xlsx"

data_sources = pd.read_excel(file)

print(data_sources.columns)

# %%

n = len(data_sources)
print(n)
dfs = []
for name, value in data_sources.items():
    # print(name)
    # print(value)
    if "indicator" in str(name).lower() or "trend" in str(name).lower() or "notes" in str(name).lower():
        continue

    juri = str(name)
    juri_list = [juri] * n

    values = value.to_list()

    to_append = pd.DataFrame({'juri': juri_list, 'indicator': data_sources['Indicator'], "trend": data_sources['Trend'], "links": values})
    dfs.append(to_append)
    # print(juri_list)

data_sources_df = pd.concat(dfs)

data_sources_df.reset_index(inplace=True, drop=True)

data_sources_df = data_sources_df.loc[:,[ 'links', 'juri', 'indicator', 'trend']]

os.chdir(r'C:\Users\clutz\OneDrive - THE HUNT INSTITUTE\Documents\Data\data sources')
data_sources_df.to_csv('data_sources_v2.csv')

# %%

# function to get unique values
def unique(list1):
    unique_list = pd.Series(list1).drop_duplicates().tolist()
    for x in unique_list:
        print(x)

indicators = unique(data_sources_df['indicator'])

[v for k, v in data_sources_df.groupby('indicator')]


for k, v in data_sources_df.groupby('indicator'):
    

# %%



