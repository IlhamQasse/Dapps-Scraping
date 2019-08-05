# DApps-Scraping
This project scrapes the DApps websites and repositories such as the state of DApps and Dappradar. Moreover, it also can be used to run other website scraper projects from parsehub. You only need to change the app-key to access your projects in parsehub. 



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
For Mac users, please make sure you have wget installed in your system, use the following command to install it:

```bash
brew install wget 
```

Once the driver is downloaded, please add the path of the chrome driver to both scripts (DappRadar.py, stateDapps.py).
The path of the chrome driver is specified in the line (30) in both scripts, it should be changed to your own driver path.


## Usage

To scrape the required websites we have used the package Selenium.
We have created two scripts:

1. the first script is to crawl the DappRadar webpage. To run the script use the following comand:

```bash
python DappRadar.py
```

2. The second script scrapes the State of the Dapps website. The command to run the script is:

```bash
python stateDapps.py
```

The scraping time depends on the number of the pages, and it may take 1 to 2 hours to fully run the script.
Once the extraction are done, the scripts will generate plots from the extracted data and automatically save them in a folder with the website name and date of the run.

## Disclaimer
Be aware that web scraping is considered a bad practice. Please be advised that this was created for research and education purposes only.  

