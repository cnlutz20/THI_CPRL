
# %% 
import os, sys, json, datetime, re # Provides OS-dependent functionality, system-specific parameters, JSON handling, and date/time manipulation
import pandas as pd             # Provides data structures and data analysis tools
import numpy as np              # Supports large, multi-dimensional arrays and matrices
import ast
import requests
import urllib3
from tqdm import tqdm
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


from bs4 import BeautifulSoup

# %%

file = r"C:\Users\clutz\OneDrive - THE HUNT INSTITUTE\Documents\Data\imports\quorum\bill data downloads\bills-data-pull_v2 (1).csv"
all_bills = pd.read_csv(file)
print(all_bills.columns)
# %%

all_bills.columns = ['bill', 'state','bill_label','title', 'bill_sum_ai', 'bill_sum','sponsors','status','last_action','source_link']
# %% early ed bills
# ec_subs =  [
#     "Child Care Comn",
#     "Day Care",
#     "Early Childhood Education",
#     "Newborns & Infants",
#     "Partnership For Children",
#     "Social Services"
# ]



ec_subs = ['child\s{0,1}care', 'early\s{0,1}childhood', 'preschool']
ec_pat = "|".join(ec_subs)
print(ec_pat)


# %%
print(all_bills.columns)
for bill in all_bills['bill_sum']:
    if re.search(f'{ec_pat}', str(bill).lower()):
        matches = re.findall(ec_pat, str(bill).lower())
        print('############################')
        print('***********')
        print(*matches)
        print('***********')
        print(bill)
        print('\n')
# %%


ec_ed_bills = all_bills[all_bills.subjects.str.contains(ec_pat, regex = True, case=False)]



ec_ed_bills.reset_index(inplace=True, drop=True)

#%% Higher Ed

he_keywords = [
    "post-secondary transition",
    "equity gaps",
    "college-going rates",
    "workforce readiness",
    "certificate programs",
    "wraparound services",
    "stackable credentials",
    "student persistence",
    "retention strategies",
    "lifelong learning",
    "postsecondary barriers",
    "alternative pathways",
    "higher education institutions",
    "higher education",
    "legislative support for education",
    "student success metrics",
    "high quality credential",
    "vocational training",
    "attainment",
    "persistence",
    "resistance",
    "graduation"
]


he_pat = r'\b(' + '|'.join(map(re.escape, he_keywords)) + r')\b'

# he_pat = "|".join(he_keywords)
print(he_pat)

all_bills['bill_sum'].fillna('nan',inplace=True)

he_ed_bills = all_bills[all_bills.bill_sum.str.contains(he_pat, regex = True, case=False)]
he_ed_bills.reset_index(inplace=True, drop=True)

os.chdir(r'C:\Users\clutz\OneDrive - THE HUNT INSTITUTE\Documents\Data\bill_data\Higher Ed')
he_ed_bills.to_csv('higher_ed_bills.csv', index=False)
# %%
# print(all_bills.columns)
for i,bill in enumerate(he_ed_bills['bill_sum']):
    # matches = re.findall(he_pat, str(bill).lower())
    matches = re.findall(r'graduation', str(bill).lower())
    if matches:
        grad_match = re.findall(r'higher ed|post-{0,1}secondary', str(bill).lower())
        if grad_match:
            continue
        
        else:
            print('############################')
            print(he_ed_bills.loc[i,'state'])
            print(he_ed_bills.loc[i,'bill'])
            print('############################')
            print('***********')
            print(*grad_match)
            print('***********')
            print(bill)
            print('\n')
    

        print('############################')
        print(he_ed_bills.loc[i,'bill'])
        print('############################')
        print('***********')
        print(*matches)
        print('***********')
        print(bill)
        print('\n')
# %%
