import os, sys, json, re
import numpy as np
from cprl_functions.state_capture import state_coding

def create_pk(df,column):
    lengths = []
    df.loc[:,'state_code'] = np.nan
    df.loc[:,'chamber_code'] = np.nan
    df.loc[:,'district'] = np.nan
    df.loc[:,'primary_key'] = np.nan
    for i,j in enumerate(df[f'{column}']):
        # print(str(j))
        # print(row)
        district_raw = re.split(r'\s(?=District)', str(j))
        match = re.findall(r'\s\d+', str(district_raw))[0]
        match = match.strip()
        if len(match) == 2:
            district_code = '0' + str(match)
        elif len(match) == 1:
            district_code = '00'+str(match)
        else:
            district_code = str(match)
        district_len = len(match)
        lengths.append(district_len)
        ext_state = df.loc[i,'state_abbreviation']
        state_code = state_coding.get(ext_state)
        if 'house' in str(j).lower():
            chamber_code = '0'
        elif 'senate' in str(j).lower():
            chamber_code = '1'
        else:
            print(f'unknown chamber: {str(j)}')
            break
        
        # display_markdown(f'#### {ext_state} - {chamber_code} - {district_raw}', raw=True)
        key_code = f'{state_code}{chamber_code}{district_code}'
        
        
        df.loc[i,'state_code'] = state_code
        df.loc[i,'chamber_code'] = chamber_code
        df.loc[i,'district'] = match
        df.loc[i,'primary_key'] = key_code
    return df
create_pk(df, 'dis')