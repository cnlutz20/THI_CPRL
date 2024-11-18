# %% 
import os, sys, json, datetime, re # Provides OS-dependent functionality, system-specific parameters, JSON handling, and date/time manipulation
import pandas as pd             # Provides data structures and data analysis tools
import numpy as np              # Supports large, multi-dimensional arrays and matrices
import ast
import requests
import urllib3
from tqdm import tqdm
import glob
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


from bs4 import BeautifulSoup

# %%

os.chdir(r'C:\Users\clutz\OneDrive - THE HUNT INSTITUTE\Documents\Data\attendance data')
files = glob.glob('*')



keys = ['slr', 'hlr', 'leg_ed']


se_pat = "|".join(keys)
state_eng_events = []
for file in files:
    if re.search(se_pat, str(file).lower()):
        df = pd.read_excel(file)
        df['event'] = str(file)

        state_eng_events.append(df)

SE_23_24_events = pd.concat(state_eng_events)
SE_23_24_events.reset_index(drop=True, inplace=True)

# %%
se_legs = SE_23_24_events.loc[:,['honorific', 'role','first_name', 'last_name','title','event']]
# se_legs = se_legs.drop_duplicates(subset=['first_name', 'last_name'])
se_legs['state'] = se_legs['event'].str.split("_").str[0]
se_legs['event'] = se_legs['event'].str.replace("_", ' ').str.replace('.xlsx', '')
se_legs['first_name'] = se_legs['first_name'].str.strip()
se_legs['last_name'] = se_legs['last_name'].str.strip()
se_legs = se_legs.groupby(['first_name','last_name']).agg(
    state = ('state','first'), 
    honorific = ('honorific','first'),
    title = ('title', 'first'),  

    Combined=('role', lambda x: '; '.join([
        f"{se_legs.loc[i, 'event']} ({v})" if pd.notna(v) and 'Legislator' not in str(v) else se_legs.loc[i, 'event']
        for i, v in zip(x.index, x)
    ]))
).reset_index()
    

# %%

se_legs['honorific'] = se_legs['honorific'].fillna('nan')
se_legs['title'] = se_legs['title'].fillna('nan')
se_legs = se_legs[(se_legs['honorific'].str.lower().str.contains(r'representative|delegate|senator')|se_legs['title'].str.lower().str.contains(r'representative|delegate|senator'))]
se_legs = se_legs.loc[:,['state', 'honorific', 'first_name', 'last_name','title', 'Combined']]
se_legs['title'] = se_legs['title'].replace('nan', np.nan)
se_legs['honorific'] = se_legs['honorific'].replace('nan', np.nan)
se_legs = se_legs.loc[:, ['state','honorific', 'first_name', 'last_name', 'title', 'Combined']]
se_legs = se_legs.rename(columns={'Combined': 'events'})

se_legs = se_legs.drop_duplicates(subset=['first_name', 'last_name'])

os.chdir(r'C:\Users\clutz\OneDrive - THE HUNT INSTITUTE\Documents\Data\attendance data\exports')
se_legs.to_csv('legs_state_engagement_events.csv', index=False)

# %%

for event in state_eng_events:
    df = pd.read_excel(event)


# %%