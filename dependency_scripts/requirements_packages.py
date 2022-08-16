import os
from unicodedata import name
from johnnydep.lib import JohnnyDist 
import streamlit as st
import pandas as pd


def latest_pkg(df):
    # add latest_version column to dataframe
    df['latest_version'] = ''
    for i in df['software_package']:
        try:
            dist = JohnnyDist(i)
            df.loc[df['software_package'] == i, 'latest_version'] = dist.version_latest
        except:
            print("No version found for {}".format(i))
    return df



def get_requirements(cont,repo_name):
    dat = {
            'project_name': [],
            'software_package': [],
            'current_version': [],
            'latest_version': [],
        }
    
    packages = []
    name = []

    for line in cont:
        packages.append(line)
    
    package = '\n'.join(packages)
    package = package.replace('"', '')
    # remove charachter b' from the string
    package = package.replace('b\'', '')
    # remove the charachter ' from the string
    package = package.replace("'", "") 

    # preprocess the package names by removing --hash= and anything after
    package = package.replace('--hash=', '')

    # split on --hash
    package = package.strip()
    data = package
    # turn the data into a list
    data = data.split('\n')

    # delete all items with a value beginnigs with '#'
    data = [x for x in data if not x.__contains__('    sha')]

    # remove all items the contain #
    data = [x for x in data if not x.__contains__('#')]

    data = '\n'.join(data)
    #st.write(data)
    software_list = list(set(data.split("\\")))

    # remove all empty strings from the list
    software_list = [x for x in software_list if x]

    # turn the list into a string 
    software_list = '\n'.join(software_list)
    #st.write(software_list)

    for fg in software_list.split('\n'):
        # splitting on the first space
        fg = fg.split(' ',1)
        # check for the latest version of a java package
    
        if fg[0]:
            # check using safety package to see if the package is safe
            # split i[0] on the == sign to get the package name and version
            dc = fg[0].split('==')
            # add dc to dat 
            dat['project_name'].append(repo_name)
            dat['software_package'].append(dc[0])
        try:
            dat['current_version'].append(dc[1])
        except:
            dat['current_version'].append('N/A')
    
    df = pd.DataFrame.from_dict(dat, orient='index')
    df = df.transpose()
    fin = latest_pkg(df)
    fin['current_version'] = fin['current_version'].str.replace(',', '')
    fin = fin.assign(recommendation = fin.apply(lambda x: 'Upgrade' if x['current_version'] < x['latest_version'] else 'N/A', axis=1))
    #st.dataframe(fin)
    return fin
    

