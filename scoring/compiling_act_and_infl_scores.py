# %%
import os, sys, json, datetime, re, xlrd  # Provides OS-dependent functionality, system-specific parameters, JSON handling, and date/time manipulation
import pandas as pd             # Provides data structures and data analysis tools
from openpyxl import Workbook
import numpy as np              # Supports large, multi-dimensional arrays and matrices
import requests
import glob
import time
from tqdm import tqdm
from functools import reduce

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
pd.options.mode.chained_assignment = None  # default='warn'
from IPython.display import display_markdown
# %%
os.chdir(r'C:\Users\clutz\THE HUNT INSTITUTE\The Hunt Institute Team Site - Documents\Development (formerly Grants Management)\!Administrative\Christian\Legislators Data\leg_data_update_10_2024\build files')

legislators_df = pd.read_csv('list_of_legislators_11_15_2024.csv')
activities_df = pd.read_csv('relationship_scores.csv')
influence_df = pd.read_csv('leg_infl_df.csv')

activities_df = activities_df.loc[:,['helper', 'activities_score']]
influence_df = influence_df.loc[:,['helper', 'influence_score']]


first_merge = pd.merge(legislators_df, activities_df, how="outer", on='helper')
# print(first_merge.to_string())
second_merge = pd.merge(first_merge, influence_df, how="outer", on='helper')
# print(first_merge.to_string())



print(legislators_df.columns)
print(activities_df.columns)
print(influence_df.columns)
final_df = second_merge
final_df.to_csv(r'C:\Users\clutz\THE HUNT INSTITUTE\The Hunt Institute Team Site - Documents\Development (formerly Grants Management)\!Administrative\Christian\Legislators Data\leg_data_update_10_2024\build files\compiled scores\compiled_scores.csv', index=False)


# print(legislators_df.to_string())
# print(activities_df.to_string())
# print(influence_df.to_string())





