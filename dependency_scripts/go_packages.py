from asyncio import subprocess
import os
import subprocess
import pandas as pd
import streamlit as st
import re
import requests
from bs4 import BeautifulSoup


def get_go_content(file_content, project_name):
    dat = {
            'project_name': [],
            'package_name': [],
            'current_version': [],
            'latest_version': [],
        }
    results = []
    match = re.search('\(([^)]+)', file_content)
    if match:
        m =  match.group(1)
        results.append(m)
    r = ' '.join(results)
    r = r.split( )
    for ac in r:
        print(ac)
        dat['package_name'].append(ac)
        dat['project_name'].append(project_name)
        r = ' '.join(results)
        r = r.split()
        url = "https://pkg.go.dev/{}".format(r)
        st.write(url)
        # grab the html from the url and parse it with BeautifulSoup
        html = requests.get(url)
        soup = BeautifulSoup(html.text, 'html.parser')
        ab = soup.find_all("a", href="?tab=versions")
        # get the versions from the html using beautifulsoup
        versions = [a.text for a in ab]
        # append the versions to the dataframe
        dat['latest_version'].append(versions[0])

    df = pd.DataFrame.from_dict(dat, orient='index')
    df = df.transpose()
    #st.dataframe(df)
    return df
   


