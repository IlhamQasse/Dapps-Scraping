#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 29 12:26:27 2019

@author: elyhabaro
"""

# import the libraries : Selenium, pandas, lxml
from lxml import html
from selenium import webdriver
import pandas as pd
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import matplotlib.pyplot as plt
import datetime 
import os
import os.path
from datetime import date, timedelta
import sys
#Start chrome driver and load the page
driverPath=os.path.dirname(os.path.abspath(__file__))
#please make sure that you have installed the driver and its in the same file as the python code, otherwise change the specified path 
driver = webdriver.Chrome(driverPath+'/chromedriver')
driver.get('https://www.dapp.com')
actions = ActionChains(driver)
eachdapp= pd.DataFrame(columns=['Txn7d','Volume7d','Balance', 'smartContracts'])
currenturl=driver.current_url
#Below function check if a certin element is in the page or not (it used for social media links)
def is_element_present(driver, what):
    try:
        driver.find_element(By.XPATH, value=what)
    except NoSuchElementException as e:
        return False
    return True
#Access the source page of the loaded page and extrct the required data based on the xpath
tree = html.fromstring(driver.page_source)
'''
if len(sys.argv) < 2:
    x=True
    while x:
      nextp=driver.find_element_by_xpath(".//div[@class='viewmore']").click()
      tree = html.fromstring(driver.page_source)
      if is_element_present(driver, './/div[@class="viewmore"]'):
         x=True
      else:
         x=False
else:
    pagen=int(sys.argv[1])
    y=1
    x=True
    while x:
      nextp=driver.find_element_by_xpath(".//div[@class='viewmore']").click()
      tree = html.fromstring(driver.page_source)
      y=y+1
      if y == pagen
         x=False
'''
#Access each Dapp and extract more data
time.sleep(5)
tree = html.fromstring(driver.page_source)
dappNAme = tree.xpath('.//div[@class="column dapp-name"]/div/text()')
category = tree.xpath('.//div[@class="column dapp-category"]/text()')
users = tree.xpath('.//div[@class="column dapp-user"]/div/div[1]/text()')
Platform = tree.xpath('.//div[@class="column dapp-blockchain"]/span/text()')
Txn = tree.xpath('.//div[@class="column dapp-transactions"]/div/div[1]/text()')
Volume = tree.xpath('.//div[@class="column dapp-volumn"]/div/div/div[1]/span[1]/text()')
df = pd.DataFrame(list(zip(dappNAme,category,users,Platform,Txn,Volume)), columns =['dappNAme','category','users','Platform','Txn','Volume'])       
links = [link.get_attribute('href') for link in driver.find_elements_by_xpath(".//div[@class='each-dapp-item']/a")]
time.sleep(5)
for link in links:
    driver.get(link)
    tree = html.fromstring(driver.page_source)
    Balance=tree.xpath('.//div[@class="balance"]/text()')
    smartContracts=tree.xpath('.//div[@class="contract"]/span[1]/text()')
    Txn7d=tree.xpath('.//div[@class="stats-bottom-sec"]/div[2]/div[5]/span[2]/text()')
    Volume7d=tree.xpath('.//div[@class="stats-bottom-sec"]/div[3]/div[5]/span[2]/text()')
    eachdapp = eachdapp.append(pd.DataFrame([[Txn7d,Volume7d,Balance,smartContracts]], columns=eachdapp.columns))
eachdapp['smartContracts']=eachdapp['smartContracts'].astype(str)
eachdapp['smartContracts'] = eachdapp['smartContracts'].map(lambda x: x.lstrip("['").rstrip("\\xa0']"))
eachdapp['Balance']=eachdapp['Balance'].astype(str)
eachdapp['Balance'] = eachdapp['Balance'].str.replace(r"\\n .*']","")
eachdapp['Balance'] = eachdapp['Balance'].str.replace(r"\['Dapp Contract Balance:\\xa0","")
eachdapp['Txn7d']=eachdapp['Txn7d'].astype(str)
eachdapp['Txn7d'] = eachdapp['Txn7d'].map(lambda x: x.lstrip("['").rstrip("']"))
eachdapp['Volume7d']=eachdapp['Volume7d'].astype(str)
eachdapp['Volume7d'] = eachdapp['Volume7d'].str.replace(r"\\n .*']","")
eachdapp['Volume7d'] = eachdapp['Volume7d'].str.replace(r"\['","")
#Assign the extracted data to one data frame
df.reset_index(inplace=True, drop=True)
eachdapp.reset_index(inplace=True, drop=True)
result = pd.concat([df, eachdapp], axis=1)
#Close and quit the chrome driver
driver.quit()
#Create folder to save figures and extracted data

today = datetime.datetime.now()
year = today.strftime("%Y")
month=today.strftime("%m")
day=today.strftime("%d")
path=os.path.dirname(os.path.abspath(__file__))
filename = path+"/dapp.com-"  + year +"-" + month + "-" + day
os.mkdir(filename)

# A general describe of the extracted data
print(result.describe(include=['object']))
fig1 = plt.figure(1)
result['Platform'].value_counts().plot(kind='bar',title='number of DApps in each platform')
fig1.tight_layout()
fig1.savefig(filename+'/dappsPlatform.png',dpi=1000)
# add plt.close() after you've saved the figure
plt.close(fig1)
#number of DApps in each category
fig2 = plt.figure(2)
result['category'].value_counts().plot(kind='bar',title='number of DApps in each category')
fig2.tight_layout()
fig2.savefig(filename+'/dappsCategory.png',dpi=1000)
plt.close(fig2)

#DApps Daily Volume
fig3 = plt.figure(3)
result.Volume = result.Volume.str.strip()
result.Volume = (result.Volume.replace(r'[KMB]+$', '', regex=True).astype(float) * result.Volume.str.extract(r'[\d\.]+([KMB]+)', expand=False).fillna(1).replace(['K','M', 'B'], [10**3, 10**6, 10**9]).astype(int))
df1=result.groupby('Platform', as_index=False)['Volume'].sum()
plot=df1.plot(x='Platform',kind='bar',title='Daily Volume for each blockchain platform')
fig3 = plot.get_figure()
fig3.tight_layout()
fig3.savefig(filename+'/dappsVolume.png',dpi=1000)
plt.close(fig3)

#Active users per blockchain platform
result.users = result.users.str.strip()
result.users = (result.users.replace(r'[KMB]+$', '', regex=True).astype(float) * result.users.str.extract(r'[\d\.]+([KMB]+)', expand=False).fillna(1).replace(['K','M', 'B'], [10**3, 10**6, 10**9]).astype(int))
df2=result.groupby('Platform', as_index=False)['users'].sum()
fig4 = plt.figure(4)
plot=df2.plot(x='Platform',kind='bar',title='Daily active users for each blockchain platform' )
fig4 = plot.get_figure()
fig4.tight_layout()
fig4.savefig(filename+'/dappsUsers.png',dpi=1000)
plt.close(fig4)

#Daily transactions of the DApps in each platform
result.Txn = result.Txn.str.strip()
result.Txn = (result.Txn.replace(r'[KMB]+$', '', regex=True).astype(float) * result.Txn.str.extract(r'[\d\.]+([KMB]+)', expand=False).fillna(1).replace(['K','M', 'B'], [10**3, 10**6, 10**9]).astype(int))
df3=result.groupby('Platform', as_index=False)['Txn'].sum()
fig5 = plt.figure(5)
plot=df3.plot(x='Platform',kind='bar',title='Daily Txns for each blockchain platform' )
fig5 = plot.get_figure()
fig5.tight_layout()
fig5.savefig(filename+'/dappsTxns.png',dpi=1000)
plt.close(fig5)

#Weekly transactions of the DApps in each platform
result.Txn7d = result.Txn7d.str.strip()
result.Txn7d = result.Txn7d.str.replace(r",","")
result.Txn7d = result.Txn7d.astype(int)
df4=result.groupby('Platform', as_index=False)['Txn7d'].sum()
fig6 = plt.figure(6)
plot=df4.plot(x='Platform',kind='bar',title='Weekly Txns for each blockchain platform' )
fig6 = plot.get_figure()
fig6.tight_layout()
fig6.savefig(filename+'/dappsTxnsWeekly.png',dpi=1000)
plt.close(fig6)

#Weekly Volume of the DApps in each platform
result.Volume7d = result.Volume7d.str.strip()
result.Volume7d = result.Volume7d.str.replace(r",","")
result.Volume7d = result.Volume7d.astype(float).astype(int)
df6=result.groupby('Platform', as_index=False)['Volume7d'].sum()
fig7 = plt.figure(7)
plot=df6.plot(x='Platform',kind='bar',title='Weekly Volume for each blockchain platform' )
fig7 = plot.get_figure()
fig7.tight_layout()
fig7.savefig(filename+'/dappsVolumeWeekly.png',dpi=1000)
plt.close(fig7)

#Number of smart contracts in each platform
result.smartContracts = result.smartContracts.astype(int)
df5=result.groupby('Platform', as_index=False)['smartContracts'].sum()
fig8 = plt.figure(8)
plot=df5.plot(x='Platform',kind='bar',title='Number of smart contracts in each platform' )
fig8 = plot.get_figure()
fig8.tight_layout()
fig8.savefig(filename+'/smartContracts.png',dpi=1000)
plt.close(fig8)

#Total Balance of DApps in each platform
result.Balance = result.Balance.str.strip()
result.Balance = result.Balance.str.replace(r",","")
result.Balance = result.Balance.astype(int)
df7=result.groupby('Platform', as_index=False)['Balance'].sum()
fig9 = plt.figure(9)
plot=df7.plot(x='Platform',kind='bar',title='Total Balance of DApps in each platform' )
fig9 = plot.get_figure()
fig9.tight_layout()
fig9.savefig(filename+'/dppsBalance.png',dpi=1000)
plt.close(fig9)


result.to_csv(filename+'/DappCom.csv', index=False)

#compare the file with the previous file
today = date.today()
yesterday = today - timedelta(days=1)

yesterday=yesterday.strftime('%Y-%m-%d')
filepathY='dapp.com-'+yesterday
if os.path.exists(filepathY): 
    f2=pd.read_csv(filepathY+'/DappCom.csv')
    f2.columns=['dappNAme', 'category', 'users', 'Platform', 'Txn', 'Volume', 'Txn7d','Volume7d', 'Balance', 'smartContracts']
    xf1=f2[~f2.dappNAme.isin(result.dappNAme)]
    xf2=result[~result.dappNAme.isin(f2.dappNAme)]
    if xf1.dappNAme.count() > 0:
        print("\n \033[1m The new dapps added: "+str(xf1.dappNAme.count())+" DApps\033[0m \n")
        print(xf1)
    else :
        print("\n \033[1m There is no new DApps\033[0m \n")
    if xf2.dappNAme.count() > 0:
        print("\n \033[1m The removed dapps: "+str(xf2.dappNAme.count())+" DApps \033[0m \n")
        print(xf2)
    else :
        print("\n \033[1m There is no removed DApps\033[0m \n")
else :
    print("There is no file to compare with")    
