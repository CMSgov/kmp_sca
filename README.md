# CMS System Composition Analysis - Code Scanner

## Description
As part of the Knowledge Managament Platform (KMP) initiative spear-headed by the Office of Information Technology, a proof of concept was worked on to scan agency-wide github repositories to create a machine-readable understanding of the composition of CMS repositories. 

Traditionally CMS has documented the technical composition of systems through manual inquiries in the form of an annual system census. This Proof of Concept aims to show an alternate path of determining composition in a more continous and automated manner by scanning the code of FISMA systems. 



## Run Instructions

# Install Dependencies
```
pip install -r requirements.txt
```
# Github Token 

This tool requires the use of a Github token to authenticate with the Github API. Follow the instructions below to create a Github token.

```
https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token
```

# Run Code Scanner

```
This proof of concept leverages streamlit to run on a local machine. To run the proof of concept, simply run the following command:

```
streamlit run main.py
```
The subfolder dependency script contains the functions to mine data from github for specific languages. 


