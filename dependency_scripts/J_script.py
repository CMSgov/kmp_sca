import streamlit as st
import subprocess
import pandas as pd
import re




def get_js_content(content,project_name):
    df = pd.DataFrame(columns=['project_name', 'software_package', 'current_version', 'latest_version'])
    data = {
        'project_name': [],
        'package_name': [],
        'current_version': [],
        'latest_version': [],
    }

    package_json = content.split('\n')
    
    # turn list into string
    package_json = '\n'.join(package_json)
    # remove all quotes from string
    package_json = package_json.replace('"', '')

    # check if the term devDependencies or dependencies exist in the string and make sure it is not {}
    if 'devDependencies' in package_json and 'dev':
        dev_dep = package_json.split('devDependencies:')[1]
    elif 'dependencies' in package_json:
        dev_dep = package_json.split('dependencies:')[1]

    # check if dev_dep is empty or not
    if dev_dep is None or dev_dep == '':
        print("No dependencies found in package.json for project: " + i)
    else:
        # use regex to extract everthing in a {} 
        regex = r"\{(.*?)\}"
        cont = re.findall(regex, dev_dep,re.MULTILINE | re.DOTALL)

        # remove all the white space
        cont = ''.join(cont)
        #st.write(cont) 

        # remove ^ from string
        cont = cont.replace('^', '')

        # replace : with ==
        cont = cont.replace(':', '==')
        # split the string into a list
        #cont = cont.split(',')
        #print(cont)

        # remove /n from the list
        cont = cont.split('\n')
        
        # remove all the white space from the list
        cont = [x.strip() for x in cont]

        # remove all the empty strings from the list
        cont = [x for x in cont if x]

        # split cont to get the package name and version
        cont = [x.split('==') for x in cont]
        #st.write(cont)
        # get only the first 2 elements of the list
        cont = [x[0:2] for x in cont]
        

    for at in cont:
        p_n = at[0]
        # if indexerror list index out of range, skip it
        try:
            v_n = at[1]
            ab = subprocess.check_output(['npm', 'view', p_n, 'dist-tags.latest'])
            ab = ab.decode('utf-8')
            
            # add the latest version to the dataframe
            # append the data to the dataframe
            data['project_name'].append(project_name)
            data['package_name'].append(p_n)
            data['current_version'].append(v_n)
            data['latest_version'].append(ab)
            #data['latest_version'].append(ab)
        except:
            print("Package not found in npm for package " + p_n)
    
    #st.write(data)
    df = pd.DataFrame(data)
    df = df.assign(recommendation = df.apply(lambda x: 'Upgrade' if x['current_version'] < x['latest_version'] else 'N/A', axis=1))
    st.dataframe(df)
    return df
