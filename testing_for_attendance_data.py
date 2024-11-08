# %%
import os, sys, json, datetime, re  # Provides OS-dependent functionality, system-specific parameters, JSON handling, and date/time manipulation
import pandas as pd             # Provides data structures and data analysis tools
import numpy as np              # Supports large, multi-dimensional arrays and matrices
import requests
import time
from tqdm import tqdm
import glob

# %%

os.chdir(r'C:\Users\clutz\OneDrive - THE HUNT INSTITUTE\Documents\Data\attendance data')
attendance_files = glob.glob('*.xlsx')

# %%
type_lst = []
for att in attendance_files:
    print('working on ' + str(att))
    df = pd.read_excel(att)
    for name, values in df.items():
        if re.search(r'title', str(name)):
            col = name
            print('found column')
            break
    
    try:
        type_vals = df.loc[:,col]
        type_lst.extend(type_vals)
    except:
        print('error with ' + str(att))
        print(df.columns)
        continue


print(type_lst)

type_lst = set(type_lst)
# %%
for t in type_lst:
    print('#################')
    print(str(t))
    print('\n')