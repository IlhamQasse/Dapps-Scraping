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
import sys


#get the input from the command line
project_Tocken = sys.argv[1] 
url = sys.argv[2] 

#Prepare Project to run

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
params = {
  "api_key": "t6F8DkOTJP-N",
  "format": "csv" #The format can be changed to JSON, change also the fileName veriable to JSON
}
#get the results
r = requests.get('https://www.parsehub.com/api/v2/runs/'+token+'/data', params=params)
while r.status_code == 404: #While the data is not ready
    print('Please wait the data still not ready')
    time.sleep(30) #The waiting time can be increased, it takes 40 minutes to scrape 200 pages
    r = requests.get('https://www.parsehub.com/api/v2/runs/'+token+'/data', params=params)
print(r.text)

f = open('file.txt', 'w')
f.write(r.text)
f.close ()
#Save the extracted data to a CSV file 
fileName=sys.argv[3] #get the file name
with open('file.txt', 'r') as in_file:
    stripped = (line.strip() for line in in_file)
    lines = (line.split(",") for line in stripped if line)
    with open(fileName, 'w') as out_file:
        writer = csv.writer(out_file)
        writer.writerows(lines)

#Compare the extracted data with the previous Data (both in excel sheets)
fileCompare = input("\n \033[1m Please enter the file you want to compare with: ex. (Iost.csv) \033[0m ") 
f1 = pd.read_csv(fileCompare,encoding = "ISO-8859-1",error_bad_lines=False)
f2 = pd.read_csv(fileName,encoding = "ISO-8859-1",error_bad_lines=False)
f2.columns.values[0]='name'
f1.columns.values[0]='name'

xf1=f2[~f2.name.isin(f1.name)] # returns the new dapps to the list
xf2=f1[~f1.name.isin(f2.name)] # returns the removed dapps from the list
if xf1.name.count() > 0: # check if there are any new dapps
    print("\n \033[1m The new dapps added: "+str(xf1.name.count())+" Dapps\033[0m \n")
    print(xf1)
else :
     print("\n \033[1m There are no new Dapps\033[0m \n")
if xf2.name.count() > 0:  # check if there are any removed dapps
    print("\n \033[1m The removed dapps: "+str(xf2.name.count())+" Dapps \033[0m \n")
    print(xf2)
else :
     print("\n \033[1m There are no removed Dapps\033[0m \n")
'''
# Plot the data based on the date
# Note that DappRader doesnt have Date feature, so you can't plot the extracted data based on time (Month)
import matplotlib.pyplot as plt
fileName='Steemx.csv'
df = pd.read_csv(fileName)
df['date'] = pd.to_datetime(df.name_Date)
df['count']=1
agg = df.resample('M', on='date').sum()
agg.plot( y='count',title='New Dapps (monthly totals)', figsize=(16, 9))
'''
