

# %%
#importing modules
import os, sys, json, datetime, re, xlrd  # Provides OS-dependent functionality, system-specific parameters, JSON handling, and date/time manipulation
import pandas as pd             # Provides data structures and data analysis tools
from openpyxl import Workbook
import numpy as np              # Supports large, multi-dimensional arrays and matrices
import requests
import glob
import time
from tqdm import tqdm
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
pd.options.mode.chained_assignment = None  # default='warn'
from IPython.display import display_markdown


# %%
state_list = [
    "Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", 
    "Connecticut", "Delaware", "Florida", "Georgia", "Hawaii", "Idaho", 
    "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", 
    "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota", 
    "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", 
    "New Hampshire", "New Jersey", "New Mexico", "New York", 
    "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon", 
    "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota", 
    "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington", 
    "West Virginia", "Wisconsin", "Wyoming", "District of Columbia"
]

state_abbreviations = [
    "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA", 
    "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", 
    "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", 
    "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", 
    "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY", "DC"
]

state_abbreviations_reg = []
for abv in state_abbreviations:
    for_regex = f'^{abv}'
    state_abbreviations_reg.append(for_regex)

state_pat = re.compile("|".join(state_list))
state_abv_pat = re.compile("|".join(state_abbreviations_reg))
#dictionary creation for future reference in later cells
state_ref = dict(zip(state_list, state_abbreviations))
codes = list(range(10,61,1))
state_coding = dict(zip(state_abbreviations, codes))
thi_states = ['ND', 'NM', 'OH', 'OK', 'VA', 'WV', 'AL', 'CT', 'IL', 'IN', 'KS', 'MO', 'NC']