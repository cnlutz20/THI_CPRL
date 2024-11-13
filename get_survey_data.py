# %%
import os, sys, json, datetime  # Provides OS-dependent functionality, system-specific parameters, JSON handling, and date/time manipulation
import pandas as pd             # Provides data structures and data analysis tools
import numpy as np              # Supports large, multi-dimensional arrays and matrices
import requests
import glob
import time
from tqdm import tqdm

# %%
os.chdir(r'C:\Users\clutz\OneDrive - THE HUNT INSTITUTE\Documents\Data\surveys')
eval_tracking = pd.read_excel('evals_tracking.xlsx')
# %%

print(eval_tracking)
# %%

a_dict = pd.Series(
    eval_tracking['file path'].values,
    index=eval_tracking['Name']
).to_dict()

eval_tracking.columns = ['event', 'filepath']

# %%
dfs = []
for k,v in a_dict.items():

    # new_value = '"'+str(v)+'"'
    # a_dict[k] = new_value

    os.chdir(f'{v}')
    files = glob.glob("*")
    event_list = [k] * len(files)
    df = pd.DataFrame({"event": event_list, "files": files})
    dfs.append(df)

survey_files = pd.concat(dfs)
survey_files.reset_index(inplace=True, drop = True)

# %%

eval_sub = survey_files.groupby('event', as_index=False)['files'].apply(list)
eval_sub.reset_index(inplace=True, drop = True)


# %%
eval_sub["excel_present"] = ""
for i,j_list in enumerate(eval_sub["files"]):
    print(j_list)
    for j in j_list:
        if '.xlsx' in str(j):
            eval_sub.loc[i,"excel_present"] = "yes"
        else:
            continue

evals_no_excel = eval_sub[~eval_sub.excel_present.str.contains('yes')]
# %%
print(list(evals_no_excel))
print(list(eval_tracking))
no_data = evals_no_excel.merge(eval_tracking, left_on='event', right_on='event')

os.chdir(r'C:\Users\clutz\OneDrive - THE HUNT INSTITUTE\Documents\Data\surveys')
no_data.to_csv('no_data.csv')
# %%




# %%
