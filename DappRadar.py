#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 30 11:04:44 2019

@author: elyhabaro
"""

# import the libraries : Selenium, pandas, lxml
from lxml import html
from selenium import webdriver
import pandas as pd
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import matplotlib.pyplot as plt
import datetime 
import os

#Below function check if a certin element is in the page or not (it used for social media links)
def is_element_present(driver, what):
    try:
        driver.find_element(By.XPATH, value=what)
    except NoSuchElementException as e:
        return False
    return True
#Start chrome driver and load the page
driverPath=os.path.dirname(os.path.abspath(__file__))
#please make sure that you have installed the driver and its in the same file as the python code, otherwise change the specified path 
driver = webdriver.Chrome(driverPath+'/chromedriver') 
driver.get('https://dappradar.com/rankings')
actions = ActionChains(driver)
#Access the source page of the loaded page and extrct the required data based on the xpath
tree = html.fromstring(driver.page_source)
currenturl=driver.current_url
pnumber=tree.xpath('//ul[@class="pagination-list"]/li[last()]/a/text()')
pagen=int(pnumber[0])
links = [link.get_attribute('href') for link in driver.find_elements_by_xpath("//div[@class='column-flex column-name']/a")]
Name=['r']
Volume24=['r']

Name.extend(tree.xpath('.//div[@class="table-dapp-name"]/text()'))
Category= tree.xpath('.//div[@class="column-flex column-category"]/a/span/text()')
Balance= tree.xpath('.//div[@data-heading="Balance"]/div/span[2]/text()')
User= tree.xpath('.//div[@data-heading="Users 24h"]/span/text()')
Volume24.extend(tree.xpath('.//div[@data-heading="Volume 24h"]/div/div/div[1]/text()'))
Volume7d= tree.xpath('.//div[@data-heading="Volume 7d"]/div/div[1]/text()')
Txn24= tree.xpath('.//div[@data-heading="Txs 24h"]/div/span/text()')
Txn7d= tree.xpath('.//div[@data-heading="Txs 7d"]/div/span/text()')
protocol=driver.find_elements_by_xpath(".//div[@data-heading='Protocol']/div")
platform=[]
for x in protocol :
    platform.append(x.text)
df = pd.DataFrame(list(zip(Name,Category,Balance,User,Volume24,Volume7d,Txn24,Txn7d,platform)), columns =['Name','category','Balance','User','Volume24','Volume7d','Txn24','Txn7d','platform'])

#Access each Dapp and extract more data
for x in range(pagen-1):
  nextp=driver.find_element_by_xpath("//a[@class='pagination-next']").click()
  element_present = EC.presence_of_element_located((By.XPATH, '//a[@class="pagination-next"]'))
  WebDriverWait(driver, 5).until(element_present)
  tree = html.fromstring(driver.page_source)
  Name=tree.xpath('.//div[@class="table-dapp-name"]/text()')
  Category= tree.xpath('.//div[@class="column-flex column-category"]/a/span/text()')
  Balance= tree.xpath('.//div[@data-heading="Balance"]/div/span[2]/text()')
  User= tree.xpath('.//div[@data-heading="Users 24h"]/span/text()')
  Volume24=tree.xpath('.//div[@data-heading="Volume 24h"]/div/div/div[1]/text()')
  Volume7d= tree.xpath('.//div[@data-heading="Volume 7d"]/div/div[1]/text()')
  Txn24= tree.xpath('.//div[@data-heading="Txs 24h"]/div/span/text()')
  Txn7d= tree.xpath('.//div[@data-heading="Txs 7d"]/div/span/text()')
  platform=[]
  protocol=driver.find_elements_by_xpath(".//div[@data-heading='Protocol']/div")
  for x in protocol :
    platform.append(x.text)
  dapplinks = [link.get_attribute('href') for link in driver.find_elements_by_xpath("//div[@class='column-flex column-name']/a")]
  links.extend(dapplinks)
  df = df.append(pd.DataFrame(list(zip(Name,Category,Balance,User,Volume24,Volume7d,Txn24,Txn7d,platform)), columns=df.columns))

eachdapp= pd.DataFrame(columns=['github', 'smartContract'])
for link in links:
    driver.get(link)
    tree = html.fromstring(driver.page_source)
    if is_element_present(driver, '//div[@data-original-title="GitHub"]'):
    #driver.find_element_by_xpath('//a[@title="Github"]'):
       Github = tree.xpath('//div[@data-original-title="GitHub"]/a/@href')
    else:
        Github = 'null'
    smartContract=tree.xpath('//div[@class="card card-contracts"]/header/p/span/text()')
    eachdapp = eachdapp.append(pd.DataFrame([[Github,smartContract]], columns=eachdapp.columns))
df=df.drop(df.index[0])
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
x=os.path.dirname(os.path.abspath(__file__))
filename = x+"/dappRadar-"  + year +"-" + month + "-" + day
os.mkdir(filename)

# A general describe of the extracted data

result.describe(include=['object'])

# number of DApps in each platform
fig1 = plt.figure(1)
result['platform'].value_counts().plot(kind='bar',title='number of DApps in each platform')
fig1.tight_layout()
fig1.savefig(filename+'/dappsPlatform.png',dpi=1000)
plt.close(fig1)

#number of DApps in each category
fig2 = plt.figure(2)
result['category'].value_counts().plot(kind='bar',title='number of DApps in each category')
fig2.tight_layout()
fig2.savefig(filename+'/dappsCategory.png',dpi=1000)
plt.close(fig2)

#Total DApps balance for each platform
fig3 = plt.figure(3)
result.Balance = (result.Balance.replace(r'[kMB]+$', '', regex=True).astype(float) * result.Balance.str.extract(r'[\d\.]+([kMB]+)', expand=False).fillna(1).replace(['k','M', 'B'], [10**3, 10**6, 10**9]).astype(int))
df1=result.groupby('platform', as_index=False)['Balance'].sum()
plot = df1.plot(x='platform',kind='bar',title='Total DApps balance for each platform' )
fig3 = plot.get_figure()
fig3.tight_layout()
fig3.savefig(filename+'/dappsBalance.png',dpi=1000)
plt.close(fig3)

#Active users per blockchain platform
fig4 = plt.figure(4)
result.User = (result.User.replace(r'[kMB]+$', '', regex=True).astype(float) * result.User.str.extract(r'[\d\.]+([kMB]+)', expand=False).fillna(1).replace(['k','M', 'B'], [10**3, 10**6, 10**9]).astype(int))
df2=result.groupby('platform', as_index=False)['User'].sum()
plot= df2.plot(x='platform',kind='bar',title='Active users per blockchain platform' )
fig4 = plot.get_figure()
fig4.tight_layout()
fig4.savefig(filename+'/dappsUsers.png',dpi=1000)
plt.close(fig4)

#Daily volume for each blockchain platform
fig5 = plt.figure(5)
result.Volume24 = (result.Volume24.replace(r'[kMB]+$', '', regex=True).astype(float) * result.Volume24.str.extract(r'[\d\.]+([kMB]+)', expand=False).fillna(1).replace(['k','M', 'B'], [10**3, 10**6, 10**9]).astype(int))
df3=result.groupby('platform', as_index=False)['Volume24'].sum()
plot=df3.plot(x='platform',kind='bar',title='Daily volume for each blockchain platform' )
fig5 = plot.get_figure()
fig5.tight_layout()
fig5.savefig(filename+'/dappsVolume24.png',dpi=1000)
plt.close(fig5)

#Weekly volume for each blockchain platform
fig6 = plt.figure(6)
result.Volume7d = (result.Volume7d.replace(r'[kMB]+$', '', regex=True).astype(float) * result.Volume7d.str.extract(r'[\d\.]+([kMB]+)', expand=False).fillna(1).replace(['k','M', 'B'], [10**3, 10**6, 10**9]).astype(int))
df4=result.groupby('platform', as_index=False)['Volume7d'].sum()
plot=df4.plot(x='platform',kind='bar',title='Weekly volume for each blockchain platform' )
fig6 = plot.get_figure()
fig6.tight_layout()
fig6.savefig(filename+'/dappsVolume7d.png',dpi=1000)
plt.close(fig6)

#Daily Txns for each blockchain platform
fig7 = plt.figure(7)
result.Txn24 = (result.Txn24.replace(r'[kMB]+$', '', regex=True).astype(float) * result.Txn24.str.extract(r'[\d\.]+([kMB]+)', expand=False).fillna(1).replace(['k','M', 'B'], [10**3, 10**6, 10**9]).astype(int))
df5=result.groupby('platform', as_index=False)['Txn24'].sum()
plot=df5.plot(x='platform',kind='bar',title='Daily Txns for each blockchain platform' )
fig7 = plot.get_figure()
fig7.tight_layout()
fig7.savefig(filename+'/dappsTxn24.png',dpi=1000)
plt.close(fig7)

#Weekly Txns for each blockchain platform
fig8 = plt.figure(8)
result.Txn7d = (result.Txn7d.replace(r'[kMB]+$', '', regex=True).astype(float) * result.Txn7d.str.extract(r'[\d\.]+([kMB]+)', expand=False).fillna(1).replace(['k','M', 'B'], [10**3, 10**6, 10**9]).astype(int))
df6=result.groupby('platform', as_index=False)['Txn7d'].sum()
plot=df6.plot(x='platform',kind='bar',title='Weekly Txns for each blockchain platform' )
fig8 = plot.get_figure()
fig8.tight_layout()
fig8.savefig(filename+'/dappsTxn7d.png',dpi=1000)
plt.close(fig8)

#Convert smart contracts column to integer 
result['smartContract'] = result['smartContract'].astype(str)
result['smartContract'] = result['smartContract'].map(lambda x: x.lstrip("['").rstrip("']"))
result['smartContract'] = result['smartContract'].replace('', '0')
result['smartContract'] = result['smartContract'].astype(int)

#number of smart contracts for each blockchain platform
fig9 = plt.figure(9)
df7=result.groupby('platform', as_index=False)['smartContract'].sum()
plot=df7.plot(x='platform',kind='bar',title='number of smart contracts for each blockchain platform' )
fig9 = plot.get_figure()
fig9.tight_layout()
fig9.savefig(filename+'/smartcontracts.png',dpi=1000)
plt.close(fig9)

#save the dataframe to excel file
result.to_excel(filename+'/DappRadar.xlsx', index=False)






