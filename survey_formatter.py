# %%
# Importing basic Python modules

import os, sys, json, datetime  # Provides OS-dependent functionality, system-specific parameters, JSON handling, and date/time manipulation
import pandas as pd             # Provides data structures and data analysis tools
import numpy as np              # Supports large, multi-dimensional arrays and matrices
import requests
import time
from tqdm import tqdm

# %%

file = r'C:\Users\clutz\OneDrive - THE HUNT INSTITUTE\Documents\Data\surveys\wssu_transition_m2.xlsx'
survey_dat = pd.read_excel(file)


survey_dat = survey_dat.dropna(how = 'all', axis = 1)
survey_dat = survey_dat.fillna('')
# %% split qualitative and quantitative data

# print(survey_dat.dtypes)


qual = []
quant = []
for i,x in enumerate(survey_dat.dtypes):
    print(i)

    if i == 0:
        qual.append(i)
        quant.append(i)
        continue

    if str(x) == "object":
        print(x)
        qual.append(i)
    else:
        quant.append(i)



# %%
qual_data = survey_dat.iloc[:,qual]
quant_data = survey_dat.iloc[:,quant]

# %% Calculations for Quantitative Data

# quant_data.i


lists = []
for col_name, col_data in quant_data.items():
    if str(col_name) == "Committee Member":
        continue
    print(col_name)
    print(type(col_data))

    # average = values.mean()
    condition = col_data > 3
    positive_count = condition.sum()
    total = len(col_data)

    positive_ratio = (positive_count/total)*100
    average = col_data.mean()
    # print(col_data[col_data.iloc[:,0] > 3].count())
    # print(average)
    # print(type(average))
    print(positive_ratio)
    print(average)

    append_list = [col_name, average, positive_ratio]
    lists.append(append_list)

for l in lists:
    print(l)
# %%
df = pd.DataFrame(lists, columns=['headers', 'average value', 'positive response rate'])
print(df)

# os.chdir(r'C:\Users\clutz\OneDrive - THE HUNT INSTITUTE\Documents\Data\surveys\export files')
# df.to_csv('quant_data_wssu_transition.csv')


#%% Management of Qualitative data

print(qual_data)

# %%
testing = survey_dat.iloc[0,:]
print(type(testing))
print(testing)



tes
# %%
for test in testing:
    print(type(test))


# %%