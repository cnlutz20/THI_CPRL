# %%
# Importing basic Python modules

import os, sys, json, datetime  # Provides OS-dependent functionality, system-specific parameters, JSON handling, and date/time manipulation
import pandas as pd             # Provides data structures and data analysis tools
import numpy as np              # Supports large, multi-dimensional arrays and matrices
import requests
import time
from tqdm import tqdm


# %%

file = r"C:\Users\clutz\OneDrive - THE HUNT INSTITUTE\Documents\Data\legislator data\nc\quorum downloads\nc_officials.xlsx"

nc_legs = pd.read_excel(file)
# %%

legs_columns = ['name', 'first name', 'last name', 'party', 'district', 'years in chamber', 'leadership position']
nc_officials = pd.DataFrame(columns=legs_columns)


{'name': nc_legs['Full Name'],
 'first name': nc_legs['First Name'],
 'last name': nc_legs['Last Name'],
 'party': nc_legs['Party'],
 'district': nc_legs['District'],
 
 }

