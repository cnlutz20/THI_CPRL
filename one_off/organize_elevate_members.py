# %%
import pandas as pd
import pyperclip
import numpy as np
import re

from cprl_functions.defined_functions import extract_title_and_name

# %% Elevate
#link to elevate members
#https://huntinstitute.sharepoint.com/:w:/g/EfKqws-V5KRIuY6ufT3o5GABPSAremTNW0d6UctoJyl48w?e=KtioDA

elevate_members = pyperclip.paste()
# %%
elevate_members_l = elevate_members.replace('•	', '').replace('\r', '').split('\n')
print(elevate_members_l)
elevate_members_df = pd.DataFrame({'raw_data': elevate_members_l})


elevate_members_df['name'] = np.nan
elevate_members_df['year'] = np.nan

for i,j in enumerate(elevate_members_df['raw_data']):
    if re.search(r'\d{4}-\d{4}', str(j)):
        elevate_members_df.loc[i,'year'] = j
    elif re.search(r'\s\|\s', str(j)):
        elevate_members_df.loc[i,'name'] = j

        elevate_members_df

elevate_members_df = elevate_members_df.dropna(subset=['name', 'year'], how = 'all')
elevate_members_df['year'] = elevate_members_df['year'].ffill()
print(*elevate_members_df.columns, sep = ', ')

elevate_members_df = elevate_members_df.loc[:,['name', 'year']]
elevate_members_df = elevate_members_df.dropna(subset=['name'], how = 'all')


elevate_members_df['title'] = elevate_members_df['name'].str.split('|').str[-1].str.strip() 
elevate_members_df['name'] = elevate_members_df['name'].str.split('|').str[0].str.strip() 
print(elevate_members_df['name'].head())  # Check first few values

print(elevate_members_df['name'].dtype)  # Ensure dtype is object or string



elevate_members_df['clean name'] = elevate_members_df['name'].apply(
    lambda x: pd.Series(extract_title_and_name(x))
)

elevate_members_df = elevate_members_df.loc[:,['clean name', 'name', 'title', 'year']].reset_index(drop=True)


# Split the 'name' column into two parts based on '|', take the second part, and strip it
# elevate_members_df['title'] = elevate_members_df['name'].str.split('|', 1).str[-1].str.strip()



# %%
