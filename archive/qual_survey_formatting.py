# %%
# Importing basic Python modules

import os, sys, json, datetime  # Provides OS-dependent functionality, system-specific parameters, JSON handling, and date/time manipulation
import pandas as pd             # Provides data structures and data analysis tools
import numpy as np              # Supports large, multi-dimensional arrays and matrices   
import glob         
# %%
def get_user_inputs():
    """Prompt the user for input variables."""
    event = input("Enter event name: ")
    session_date = input("Enter session date (mm/dd/yyyy): ")
    file_path = input("Enter the path to the input CSV file: ")
    output_file_path = input("Enter the path for the output CSV file: ")
    
    return event, session_date, file_path, output_file_path

# %%
event, session_date, file_path, output_file_path = get_user_inputs()
# %%
print(file_path)
# file = file_path
file = f'r"{file_path}"'

df  = pd.read_csv(file)

# %%

quant = df[df['type'] == 'quant']
quant = quant.loc[:,['question', 'avg', 'num_response']]


# %%

n = len(data)
data['event_name'] = 'ElevateNC'
data['state'] = 'North Carolina'
data = data.loc[:,['state', 'event_name', 'q1', 'q2', 'q3', 'q4', 'q5']]
#export file



# %%




