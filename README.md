# DApps-Scraping

The main objective of this project is to study and analyze the quality of the decentralised applications available in some public repositories. This project scrapes the DApps websites and repositories such as the state of DApps and Dappradar

The extracted datasets are available in Zenodo : https://zenodo.org/record/3382127. 


## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the required packages.

```bash
pip install -r requirements.txt
```
The used python package Selenium requires a chrome driver to be downloaded. Please downloaded following the below URL.

(https://chromedriver.chromium.org/downloads)

For Linux and Mac OS users, run the following script to download the chrome driver:

```bash
./download.sh 
```
#### Please make sure that the version of you chrome is 76, otherwise update your chrome or install the chrome driver for your version.

For Mac users, please make sure you have wget installed in your system, use the following command to install it:

```bash
brew install wget 
```

Once the driver is downloaded, please check the path of the chrome driver to both scripts (DappRadar.py, stateDapps.py).
if you have downloaded the chrome driver manually, please change the path specified in the codes to your own path. You don't have to change the path if you have used the script to download your driver.


## Usage

To scrape the required websites we have used the package Selenium.
We have created three scripts:

1. the first script is to crawl the DappRadar webpage. To run the script use the following comand:

```bash
python DappRadar.py
```
For testing purposes you can specify the number of pages you want to scrape. The command below crawles only three pages.  

```bash
python DappRadar.py 3 
```

2. The second script scrapes the State of the Dapps website. The command to run the script is:

```bash
python stateDapps.py
```
For testing purposes you can specify the number of pages you want to scrape. The command below crawles only three pages.  
```bash
python stateDapps.py 3
```

3. The third script scrapes the dapp.com website. The command to run the script is:

```bash
python dappcom.py
```
For testing purposes you can specify the number of pages you want to scrape. The command below crawles only three pages.  
```bash
python dappcom.py 3
```
The scraping time depends on the number of the pages, and it may take 1 to 2 hours to fully run the script.
Once the extraction are done, the scripts will generate plots from the extracted data and automatically save them in a folder with the website name and date of the run.

## Disclaimer
Be aware that web scraping is considered a bad practice. Please be advised that this was created for research and education purposes only.  

