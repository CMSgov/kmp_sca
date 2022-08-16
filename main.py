from ast import parse
import streamlit as st
import pandas as pd
import time
import xmltodict
import subprocess
from bs4 import BeautifulSoup
import config
import re 
from github import Github

# dependency_scripts
from dependency_scripts.Java_pom_packages import *
from dependency_scripts.ruby_gemfile_packages import *
from dependency_scripts.J_script import *
from dependency_scripts.go_packages import *
from dependency_scripts.requirements_packages import *
from dependency_scripts.poetry_lock_proj import *


html_temp = """
<div style="background-color:teal;;padding:10px">
    <h2 style="color:white;text-align:center;">Charon GitCrawler</h2>
</div>
"""
# route html to the streamlit app
st.markdown(html_temp, unsafe_allow_html=True)
st.empty()

# key for public github api
key = config.key
private_key = config.private_api_key
g = Github(key, per_page=5000)


# get the remaining rate limit for the api
@st.cache(allow_output_mutation=True, show_spinner=True, suppress_st_warning=True)
def get_rate_limit():
    rate_limit = g.get_rate_limit()
    rate_limit = str(rate_limit)
    return rate_limit


def get_data(project_name):
    # get the breakdown of public repositories by language for the organization
    all_projects = g.get_user(project_name).get_repos()
    all_prods_name = []
    all_prods_language = []

    for project in all_projects:
        all_prods_name.append(project.name)
        all_prods_language.append(project.language)
        # combine both list into a dataframe
        df = pd.DataFrame(list(zip(all_prods_name, all_prods_language)), columns = ['Project_Name', 'Language'])
        # Add a column to the dataframe with the languages minned and a check mark if the language is java, ruby, python, javascript, typescript, go 
    #st.dataframe(df)
    st.table(df['Language'].value_counts())
    with st.expander("Public {} Repositories".format(project_name)):
        st.dataframe(df)
    return df

@st.cache(allow_output_mutation=True, show_spinner=True, suppress_st_warning=True)
def get_private_data():
    repos = g.get_user().get_repos(type="private")
    all_prods_name = []
    all_prods_language = []
    for project in repos:
        all_prods_name.append(project.name)
        all_prods_language.append(project.language)
        # combine both list into a dataframe
        df = pd.DataFrame(list(zip(all_prods_name, all_prods_language)), columns = ['Project_Name', 'Language'])
    # display the dataframe in a table with the language count
    st.table(df['Language'].value_counts())
    with st.expander("Private Repos"):
        st.dataframe(df)
    return df


def get_repo_details(repo):
    with st.expander("Repository Details"):
        st.write(f"Repository Name: ", repo.name)
        st.write(f"Repository Description: ", repo.description)
        st.write(f"Repository URL: ", repo.html_url)
        st.write(f"Repository Language: ", repo.language)
        st.write(f"Repository Open Issues: ", repo.open_issues_count)
        st.write(f"Repository Private: ", repo.private)
        st.write(f"Repository Permissions: ", repo.permissions)


# manage the tokens left and pause the code if tokens are less than number allowed
# program will continue if tokens are greater than number allowed
def token_limit_check(tokens_left):
    if int(tokens_left) < 400:
        # display timer waiting for 1800 seconds with a progress bar
        st.warning("Token limit reached, waiting for 1800 seconds.")
        with st.spinner('Wait for it...' + get_rate_limit() + " tokens left"):
            time.sleep(1800)
            # refresh the tokens after 300 seconds
            g.get_rate_limit() 
            st.info(get_rate_limit())
        st.success('Token limit refreshed.')


# loop through the projects and mine the software libraries from them
def loop_through_projects(df,project_name,g):
    for a in df['Project_Name']:
        # keep track of the api rate limit
        rate_limit = get_rate_limit()
        tokens_left = rate_limit.split('=')[3].split(',')[0]
        st.info("Remaining tokens: " + str(g.rate_limiting))
        token_limit_check(tokens_left)

        # dataframe to store the software libraries
        gemfile_df = pd.DataFrame()

        repo_name = project_name + '/' + a

        # try except block to catch any errors
        try:
            repository_details = g.get_repo(repo_name)
            st.title(repo_name)
            get_repo_details(repository_details)
            

            # try except block to find empty repos
            try:
                contents = repository_details.get_contents("")
            except:
                st.warning("Repository Empty for project " + repo_name)
                continue

            # loop through the contents of the repository: including all nested directories, if its not empty
            while contents:
                file_content = contents.pop(0)
                if file_content.type == 'dir':
                    contents.extend(repository_details.get_contents(file_content.path))

                # list of files or file extensions searched for in every repository
                list_of_files = ['pom.xml','Gemfile.lock', 'yarn.lock','package.json', 'package-lock.json','requirements.txt','.go','poetry.lock']


                # Java Projects
                if file_content.name in list_of_files:
                    if file_content.name == 'pom.xml':
                        parsed_results =[]
                        # get the content of the file
                        pom_content = repository_details.get_contents(file_content.path).decoded_content.decode('utf-8')
                        # parse the xml file into a dictionary
                        result = xmltodict.parse(pom_content)
                        parsed_results.append(result)
                        dep_results_a, dep_results_b = pomParse(parsed_results)
                        df_man = pd.DataFrame.from_dict(dep_results_a, orient='index')
                        df_man = df_man.transpose()
                        df_dep = pd.DataFrame.from_dict(dep_results_b,orient='index')
                        df_dep = df_dep.transpose()

                        with st.expander("Java Pom Packages"):
                            print("Here")
                            st.dataframe(df_man)
                            st.dataframe(df_dep)
                            

                # Ruby projects
                    if file_content.name == 'Gemfile.lock' or file_content.name == 'yarn.lock':
                        
                        st.success("Gemfile Found in  " + file_content.path + " for project: " + repo_name)
                        with st.expander("Gemfile.lock"):
                            st.write("Gemfile found for project: " )
                            content = repository_details.get_contents(file_content.path).decoded_content
                            #st.text(content.decode('utf-8'))
                            content = content.decode('utf-8')
                            gem_file = getgemFile(content,g,a)
                            gemfile_df.append(gem_file)
                            st.dataframe(gemfile_df)

                    else:
                        print("No Gemfile found for project: " + repo_name)

                    # javascript projects
                    if file_content.name == 'package.json' or file_content.name == 'package-lock.json':
                        with st.expander("package.json"):
                            content = repository_details.get_contents(file_content.path).decoded_content
                            content = content.decode('utf-8')
                            package_file = get_js_content(content,repo_name)
                            st.write(package_file)
                            print('package.json found for project: ' + repo_name)
                    else:
                        print("No package.json found for project: " + repo_name)

                    if file_content.name.endswith('.go'):
                        with st.expander("Go Mined Packages"):
                            file_content = repository_details.get_contents(file_content.path)
                            file_content = file_content.decoded_content
                            file_content = file_content.decode('utf-8')
                            file_content = file_content.strip()
                            go_file = get_go_content(file_content,repo_name)
                            st.dataframe(go_file)
                    else:
                        print("No Go file found for project: " + str(repo_name))
                    
                    # python projects

                    if file_content.name == 'requirements.txt':
                        with st.expander("Python Mined Packages"):
                            content = repository_details.get_contents(file_content.path).decoded_content
                            cont =  content.decode('utf-8')
                            cont =  str(cont)
                            cont = cont.split('\n')
                            st.write(cont)
                            df = get_requirements(cont,repo_name)
                            st.dataframe(df)

                    else:
                        print("No requirements.txt found for project: " + repo_name)
                    
                    if file_content.name == 'poetry.lock':
                        with st.expander('Poetry Mined Packages'):
                            content = repository_details.get_contents(file_content.path).decoded_content.decode('utf-8')
                            poetrylock = poetrylock.split('\n')
                            # append to poetry 
                            poetry.extend(poetrylock)

                    else:
                        print("No poetry.lock found for project: " + repo_name)


        except Exception as e:
            st.error(e)
            st.error("Error with " + repo_name)
            st.error("Skipping this project")
            continue




def main():
    project_name = st.text_input(key='project_name', label='Enter the organization repo name')
    # check rate limit
    rate_limit = g.rate_limiting
    st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
    st.info(f'You have {rate_limit[0]} requests left')

    tab1, tab2, tab3 = st.tabs(['Public_Repos','Private_Repos', 'CMS onPrem Repos'])

    with tab1:
        if st.button('Mine Public Repos'): 
            df = get_data(project_name)
            n = loop_through_projects(df, project_name,g)
            st.success(" projects mined")
            st.balloons()
            #st.table(n)
            
    with tab2:
        if st.button("Mine Private Repos"):
            df = get_private_data()
            mn = loop_through_projects(df, project_name,g)
            st.success(" projects mined")
            st.balloons()

            #st.info("Still in development")
            #st.table(n)

    with tab3:
        if st.button("Mine onPrem CMS Repos"):
            st.info("Still in development")


    st.sidebar.subheader("Languages Minned")
    # make an interactive list of languages minned
    st.sidebar.markdown(f"The following languages will be mined under the {project_name} repository:")
    # create a table of languages minned

    st.sidebar.text("Java, Ruby, Python, Javascript, Typescript, Go, HTML, C++, XSLT")




if __name__ == '__main__':
    main()
    
    st.write("Created by: @calebaryee3")
    