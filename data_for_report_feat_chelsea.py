# %%
import os, sys, json, datetime, re  # Provides OS-dependent functionality, system-specific parameters, JSON handling, and date/time manipulation
import pandas as pd             # Provides data structures and data analysis tools
import numpy as np              # Supports large, multi-dimensional arrays and matrices
import requests
import time
from tqdm import tqdm

# %%




# %%
file =r"C:\Users\clutz\OneDrive - THE HUNT INSTITUTE\Documents\Data\state_legislators_data.xlsx"


leg_data = pd.read_excel(file)
# %%
legs_current_thi = leg_data[leg_data["Relationship Score"] >= 10]


# %%

event_attenders = leg_data[leg_data['Attended any event?'] == "Yes"]

num_eventers = len(event_attenders['Attended any event?'])
num_all = len(leg_data['Attended any event?'])

 
event_attenders.shape[0]

leg_data.shape

# %%

thi_relation = leg_data[leg_data["Relationship Score"] >= 10]
no_thi_relation = leg_data[leg_data["Relationship Score"] < 10]

legs_thi_proportion = len(thi_relation)/len(leg_data)
print(legs_thi_proportion)



sum(thi_relation['Number of Ed Bills Introduced'])/sum(leg_data['Number of Ed Bills Introduced'])
#%%


sum(thi_relation['Number of Ed Bills Introduced'])/sum(leg_data['Number of Ed Bills Introduced'])

leg_bills_introduced = leg_data.groupby('State')['Number of Ed Bills Introduced'].sum().reset_index()
thi_leg_bills_introduced = thi_relation.groupby('State')['Number of Ed Bills Introduced'].sum().reset_index()

thi_leg_bills_introduced/leg_bills_introduced
intro_merge = leg_bills_introduced.merge(thi_leg_bills_introduced, on='State', how='left', suffixes=('_all', '_thi'))

intro_merge['prob'] = (intro_merge['Number of Ed Bills Introduced_thi'] / intro_merge['Number of Ed Bills Introduced_all']) * 100
intro_merge['prob'].mean()




os.chdir(r'C:\Users\clutz\OneDrive - THE HUNT INSTITUTE\Documents\Data')
intro_merge.to_csv('introduced_bills_data.csv')

billssum_thi_relation = sum(thi_relation['Number of Ed Bills Introduced'])
billssum = sum(leg_data['Number of Ed Bills Introduced'])

probability = (billssum_thi_relation/billssum)
print(probability)


print(billssum_thi_relation)
print(billssum)




Number of Ed Bills Introduced'])

no_relation = leg_data[leg_data["Relationship Score"] < 10]

