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

#Below function check if a certin element is in the page or not (it used for social media links)
def is_element_present(driver, what):
    try:
        driver.find_element(By.XPATH, value=what)
    except NoSuchElementException as e:
        return False
    return True

#Start chrome driver and load the page
driver = webdriver.Chrome('/Users/elyhabaro/Downloads/Dapps-Scraping-master-2/chromedriver') #please change the path of the chrome driver
driver.get('https://www.stateofthedapps.com/rankings')
actions = ActionChains(driver)
eachdapp= pd.DataFrame(columns=['github', 'status', 'Date', 'license'])
currenturl=driver.current_url
#Access the source page of the loaded page and extrct the required data based on the xpath
tree = html.fromstring(driver.page_source)
pnumber=tree.xpath('//button[@class="button number last"]/span/text()')
pagen=int(pnumber[0])
dappNAme = tree.xpath('.//h4[@class="name"]/a/text()')
category = tree.xpath('.//div[@class="RankingTableCategory"]/a/text()')
users = tree.xpath('.//div[@class="table-data col-dau"]/div[1]/span[1]/text()')
Platform = tree.xpath('.//div[@class="RankingTablePlatform"]/a/text()')
Devact = tree.xpath('.//div[@class="table-data col-dev"]/div[1]/span[1]/text()')
Volume7d = tree.xpath('.//div[@class="RankingTableVolume"]/span[2]/text()')
df = pd.DataFrame(list(zip(dappNAme,category,users,Platform,Devact,Volume7d)), columns =['dappNAme','category','users','Platform','Devact','Volume7d'])
#Access each Dapp and extract more data
links = [link.get_attribute('href') for link in driver.find_elements_by_xpath("//h4[@class='name']/a")]
for link in links:
    driver.get(link)
    tree = html.fromstring(driver.page_source)
    if is_element_present(driver, '//a[@title="Github"]'):
    #driver.find_element_by_xpath('//a[@title="Github"]'):
       Github = tree.xpath('//a[@title="Github"]/@href')
       Github=Github[0]
    else:
        Github = 'null'
    status=tree.xpath('//div[@class="DappDetailBodyContentModulesStatus"]/strong/text()')
    Date=tree.xpath('//div[@class="DappDetailBodyContentModulesSubmitted"]/strong/text()')
    Slicense=tree.xpath('//p[@class="license-data"]/text()')
    eachdapp = eachdapp.append(pd.DataFrame([[Github,status[0],Date[0],Slicense[0]]], columns=eachdapp.columns))
#Go back to the previous ranking page
driver.get(currenturl)

#Extract data from the next pages 
for x in range(pagen-1):
  nextp=driver.find_element_by_xpath("//div[@class='last-wrapper']/button").click()
  element_present = EC.presence_of_element_located((By.XPATH, '//div[@class="last-wrapper"]/button'))
  WebDriverWait(driver, 5).until(element_present)
  currenturl=driver.current_url
  tree = html.fromstring(driver.page_source)
  dappNAme = tree.xpath('.//h4[@class="name"]/a/text()')
  category = tree.xpath('.//div[@class="RankingTableCategory"]/a/text()')
  users = tree.xpath('.//div[@class="table-data col-dau"]/div[1]/span[1]/text()')
  Platform = tree.xpath('.//div[@class="RankingTablePlatform"]/a/text()')
  Devact = tree.xpath('.//div[@class="table-data col-dev"]/div[1]/span[1]/text()')
  Volume7d = tree.xpath('.//div[@class="RankingTableVolume"]/span[2]/text()')
  links = [link.get_attribute('href') for link in driver.find_elements_by_xpath("//h4[@class='name']/a")]
  for link in links:
    driver.get(link)
    tree = html.fromstring(driver.page_source)
    if is_element_present(driver, '//a[@title="Github"]'):
    #driver.find_element_by_xpath('//a[@title="Github"]'):
       Github = tree.xpath('//a[@title="Github"]/@href')
       Github=Github[0]
    else:
        Github = 'null'
    status=tree.xpath('//div[@class="DappDetailBodyContentModulesStatus"]/strong/text()')
    Date=tree.xpath('//div[@class="DappDetailBodyContentModulesSubmitted"]/strong/text()')
    Slicense=tree.xpath('//p[@class="license-data"]/text()')
    eachdapp = eachdapp.append(pd.DataFrame([[Github,status[0],Date[0],Slicense[0]]], columns=eachdapp.columns))
  driver.get(currenturl)
  df = df.append(pd.DataFrame(list(zip(dappNAme,category,users,Platform,Devact,Volume7d)), columns=df.columns))

#Assign the extracted data to one data frame
df.reset_index(inplace=True, drop=True)
eachdapp.reset_index(inplace=True, drop=True)
result = pd.concat([df, eachdapp], axis=1)
print(result)
#Close and quit the chrome driver
driver.quit()
#

#Create folder to save figures and extracted data

today = datetime.datetime.now()
year = today.strftime("%Y")
month=today.strftime("%m")
day=today.strftime("%d")
path=os.path.dirname(os.path.abspath(__file__))
filename = path+"/stateofthedapp-"  + year +"-" + month + "-" + day
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

#Status of the DApps
fig3 = plt.figure(3)
result['status'].value_counts().plot(kind='bar',title='Status of the DApps')
fig3.tight_layout()
fig3.savefig(filename+'/dappsStatus.png',dpi=1000)
plt.close(fig3)

#Used software license
fig4 = plt.figure(4)
result['license'].value_counts().head(10).plot(kind='bar',title='Used software license')
fig4.tight_layout()
fig4.savefig(filename+'/dappslicense.png',dpi=1000)
plt.close(fig4)

#Active users per blockchain platform
result['users'] = result['users'].str.replace('-', '0')
result['users'] = result['users'].str.replace(',', '').astype(int)
df1=result.groupby('Platform', as_index=False)['users'].sum()
fig5 = plt.figure(5)
plot=df1.plot(x='Platform',kind='bar',title='Active users per blockchain platform')
fig5 = plot.get_figure()
fig5.tight_layout()
fig5.savefig(filename+'/dappsUsers.png',dpi=1000)
plt.close(fig5)

#Development activity of the DApps in each platform
result['Devact'] = result['Devact'].str.replace('-', '0')
result['Devact'] = result['Devact'].str.replace(',', '').astype(int)
df2=result.groupby('Platform', as_index=False)['Devact'].sum()
fig6 = plt.figure(6)
plot=df2.plot(x='Platform',kind='bar',title='Development activity of the DApps in each platform' )
fig6 = plot.get_figure()
fig6.tight_layout()
fig6.savefig(filename+'/dappsActivity.png',dpi=1000)
plt.close(fig6)

#Weekly volume for each blockchain platform
result['Volume7d'] = result['Volume7d'].str.replace('USD', '')
result['Volume7d'] = result['Volume7d'].str.replace('-', '0')
result['Volume7d'] = result['Volume7d'].str.replace(',', '').astype(int)
df3=result.groupby('Platform', as_index=False)['Volume7d'].sum()
fig7 = plt.figure(7)
plot=df3.plot(x='Platform',kind='bar',title='Weekly volume for each blockchain platform' )
fig7 = plot.get_figure()
fig7.tight_layout()
fig7.savefig(filename+'/dappsVolume.png',dpi=1000)
plt.close(fig7)

result['date'] = pd.to_datetime(result.Date)

#Platform EOS
df4=result.loc[result['Platform'] == 'EOS']
df4['count']=1
agg1 = df4.resample('M', on='date').sum()

#Platform Ethereum
df5=result.loc[result['Platform'] == 'Ethereum']
df5['count']=1
agg2 = df5.resample('M', on='date').sum()

#Platform POA
df6=result.loc[result['Platform'] == 'POA']
df6['count']=1
agg3 = df6.resample('M', on='date').sum()

# Platform Steem
df7=result.loc[result['Platform'] == 'Steem']
df7['count']=1
agg4 = df7.resample('M', on='date').sum()

#Plot
agg1['date'] = agg1.index.values
agg2['date'] = agg2.index.values
agg3['date'] = agg3.index.values
agg4['date'] = agg4.index.values
fig8, ax1 = plt.subplots(figsize=(16, 9))
ax1.set_xlabel('Date')
ax1.set_ylabel('number of new Dapps', color='k')
ax1.plot(agg2['date'], agg2['count'], color='r', label='Ethereum')
ax1.plot(agg1['date'], agg1['count'], color='b', label='EOS')
ax1.plot(agg3['date'], agg3['count'], color='g', label='POA')
ax1.plot(agg4['date'], agg4['count'], color='y', label='Steem')
ax1.tick_params(axis='y', labelcolor='k')
plt.xticks(rotation=90) 
fig8.tight_layout()  # otherwise the right y-label is slightly clipped
#plt.title('Comparison between Ethereum new DApps and new smart contracts ')
plt.legend()
fig8.savefig(filename+'/newDapps.png',dpi=1000)
plt.close(fig8)
