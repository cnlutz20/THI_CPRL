# %%
import os, sys, json, datetime, re  # Provides OS-dependent functionality, system-specific parameters, JSON handling, and date/time manipulation
import pandas as pd             # Provides data structures and data analysis tools
import numpy as np              # Supports large, multi-dimensional arrays and matrices
import requests
import time
from tqdm import tqdm
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


from bs4 import BeautifulSoup

# %%

file = r"C:\Users\clutz\OneDrive - THE HUNT INSTITUTE\Documents\Data\legislator data\committees_data.xlsx"

coms = pd.read_excel(file)

ct_coms = coms[coms['state'] == "CT"]
ct_coms = ct_coms.drop_duplicates(subset=['committee', 'url'], keep='first')
ct_coms.reset_index(inplace=True, drop=True)



# %%

com_dfs = {}
for i,url in enumerate(ct_coms['url']):
    # session = requests.Session()
    # session.verify = certifi.where()  # Use certifi's certificates
    # response = session.get(url)

    
    response = requests.get(url, verify = False).content
    df_list = pd.read_html(response)
    # print(len(df_list))
    # print(type(df_list[0]))
    df = df_list[0]
    com_dfs[str(ct_coms['committee'].iloc[i])] = df


for k,v in com_dfs.items():
    print("#####################")
    print(k)
    print(v)

