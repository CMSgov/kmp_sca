import os
import pandas as pd

poetry  = []
poetry_data = {
'package_name': [],
'package_version': [],
'description': [],
'latest_version': [],
'timestamp': [],
'github_url': [],
'language': [],
'Source_type': [],
    }

def get_poetry_data(content):
    poetrylock = content.split('\n')
    poetry.extend(poetrylock)

    for i in poetrylock:
        if 'name' in i:
            #data['package_name'].append(i.partition('name:')[2])
            poetry_data['package_name'].append(i)
        if 'version' in i:
            poetry_data['package_version'].append(i)
        if 'description' in i:
            poetry_data['description'].append(i)
    df = pd.DataFrame.from_dict(poetry_data, orient='index')
    df = df.transpose()
    
    return df


    

