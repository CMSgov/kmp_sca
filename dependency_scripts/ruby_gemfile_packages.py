from dataclasses import dataclass
import subprocess
from turtle import onclick
import pandas as pd
import streamlit as st


def get_ruby(content,g, project_name):
    # create a dataframe with the package name and version
    #df = pd.DataFrame(columns=['package_name', 'package_version', 'latest_version', 'project_name'])
    data = {"package_name": [],
           'package_version': [],
           'latest_version': [],
           'proj_name': []}
    
    st.write("Starting to crawl the project: " + project_name)
    i = project_name
    text = content
    text = text.partition('specs:')[2]

    # remove everything from Platforms:
    text = text.partition('PLATFORMS')[0]
    # split into list
    text = text.split('\n')
    # remove empty lines
    text = [x for x in text if x]
    # trim whitespace
    text = [x.strip() for x in text]
    st.write("gemfile cleaned")


    for a in text:   
    # fine anything in brackets sand append to package_version
        if '(' in a:
            data['proj_name'].append(i) 
            data['package_version'].append(a.partition('(')[2].partition(')')[0])
            data['package_name'].append(a.partition('(')[0])
    
    for v in data['package_name']:
        s = str(v.strip())
        ab = subprocess.check_output(['gem', 'search', s])
        ab = ab.decode('utf-8')
        # put ab into a df
        if '(' in ab:
            data['latest_version'].append(ab.partition('(')[2].partition(')')[0])
    #df['pkh'] = pkh
    st.success(f"for Project {i} gemfile lock file found")
   
           
        #n = pd.DataFrame.from_dict(data,orient='index')
        #n = n.transpose()
    #st.write(data)
    return data

def getgemFile(b,g,project_name):
    n = get_ruby(b,g,project_name)
    n = pd.DataFrame.from_dict(n,orient='index')
    n = n.transpose()
    
    # if successful, display the dataframe in a table
    if n.empty == False:
        # create a new column called recommendation, if the latest version is greater than the package version, recommend to update
        fin = n.assign(recommendation = n.apply(lambda x: 'Upgrade' if x['package_version'] < x['latest_version'] else 'No Upgrade Needed', axis=1))

        #st.dataframe(fin)
        st.success("Gemfile found for project: " + project_name + " and parsed successfully")
    else:
        print("Gemfile found for project: " + project_name + " but could not be parsed")
    
    # onclick, let the user download the dataframe as a csv
    #st.download_button("Download Gemfile", format="csv", dataframe=n,onclick=lambda: st.write("Downloading Gemfile"))
    return n