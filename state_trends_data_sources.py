# %%
# Importing basic Python modules

import os, sys, json, datetime  # Provides OS-dependent functionality, system-specific parameters, JSON handling, and date/time manipulation
import pandas as pd             # Provides data structures and data analysis tools
import numpy as np              # Supports large, multi-dimensional arrays and matrices
import requests
import time
from tqdm import tqdm

# %%
file = r"C:\Users\clutz\OneDrive - THE HUNT INSTITUTE\Documents\Data\data sources\data_sources.xlsx"

data_sources_raw = pd.read_excel(file)


col_list = list(data_sources_raw)
juri_list = col_list[3:]
print(juri_list)

# %%

# data_sources_raw.loc['indicator', 'trend', 'description']
print(data_sources_raw.index)  # Check index levels
print(data_sources_raw.columns)  # Check column levels
# %%
# nc_data_sources =  

dfs = []
for j in juri_list:
    # print(j)
    data_sources = data_sources_raw.loc[:,['indicator', 'trend', 'description', j]]
    # print(data_sources)
    data_sources['juri'] = f'{j}'.upper()
    print(data_sources)
    # continue
    data_sources.columns = ['indicator', 'trend', 'description', 'data', 'juri']

    data_sources = data_sources.loc[:,['juri', 'indicator', 'trend', 'description', 'data']]
    dfs.append(data_sources)

data_sources_reorg = pd.concat(dfs)

# %%

os.chdir(r"C:\Users\clutz\OneDrive - THE HUNT INSTITUTE\Documents\Data\data sources")  
print(type(data_sources_reorg))
data_sources_reorg.to_csv('state_trends_clean.csv', index = False)
    
