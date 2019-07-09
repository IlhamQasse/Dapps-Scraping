#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  9 15:05:43 2019

@author: elyhabaro
"""
import time
import requests
import csv
import pandas as pd


# Input request from the user to enter the project token and the starting URL
project_Tocken = input("Please enter project Token: ")
url = input("Please enter the start url: ")

#project_Tocken="twxoLgsMeSCc"
#url="https://www.stateofthedapps.com/rankings/platform/steem"

params = {
  "api_key": "t6F8DkOTJP-N", # you can change the api key and use your api provided by the parsehub
  "start_url": url,
}

#run the project

r = requests.post("https://www.parsehub.com/api/v2/projects/"+project_Tocken+"/run", data=params) 
data = r.json()

#extract the run token
token = data['run_token']
print(token)

#Get the results of the running Project
#It takes sometime to fetch the results, thats why there sleep request

time.sleep(30) #The waiting time can be increased, it takes 40 minutes to scrape 200 pages
params = {
  "api_key": "t6F8DkOTJP-N",
  "format": "csv" #The format can be changed to JSON, change also the fileName veriable to JSON
}
#get the results
r = requests.get('https://www.parsehub.com/api/v2/runs/'+token+'/data', params=params)
print(r.text)
f = open('file.txt', 'w')
f.write(r.text)

#Save the extracted data to a CSV file 
fileName = input("Please enter the file name: ")
fileName=fileName+'.csv'
with open('file.txt', 'r') as in_file:
    stripped = (line.strip() for line in in_file)
    lines = (line.split(",") for line in stripped if line)
    with open(fileName, 'w') as out_file:
        writer = csv.writer(out_file)
        writer.writerows(lines)
#Compare the extracted data with the previous Data (both in excel sheets)
""" 
fileCompare = input("Please enter the file you want to compare with: ")       
df1 = pd.read_excel(fileName)
df2 = pd.read_excel(fileCompare)
C = pd.merge(left=df1,right=df2, how='outer', left_index=True, right_index=True, suffixes=['_df1', '_df2'])
not_in_df1 = C.drop(df1.index)
not_in_df2 = C.drop(df2.index)
print(not_in_df2.name_name_df1)
"""
