# DApps-Scraping
This project scrapes the DApps websites and repositories such as the state of DApps and Dappradar. Moreover, it also can be used to run other website scraper projects from parsehub. You only need to change the app-key to access your projects in parsehub. 


## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the required packages.

```bash
pip install -r requirements.txt
```

## Usage

To scrape the required websites we have used [parsehub](https://www.parsehub.com).
As input the user needs to input the Project-Token and the starting URL. 
You can change the api-key if you want to use your own projcts in parsehub.

Please use these project tokens to scrape the following websites:

| Project Token  | Website | Link Example |
| :---:   |  :---:  |  :---:   |
| tMh9JaUxNhyO  | DappRadar  | https://dappradar.com/rankings/protocol/iost |
| t10UDy7RkHR0  | State of the DApps  | https://www.stateofthedapps.com/rankings/platform/loom |



**Please note that you need to provide the link of the ranking page for each platform.**


To track the dapps status, you can compare the extracted data with previous extracted data. The comparison will return the details of newly added dapps and removed dapps. This is an automatic process that will ask for the file to compare with after extracting the new data. You can skip it if you are not interested in tracking the changes in the data.

to run the program, the following parameters are required: project token, url, and the file name to save the extracted data in
The command to run the program is:
```bash
python Dapps-scraper.py project-token url filename
```
for example
```bash
python Dapps-scraper.py tMh9JaUxNhyO  https://dappradar.com/rankings/protocol/iost iost.csv
```
## Disclaimer
Be aware that web scraping is considered a bad practice. Please be advised that this was created for research and education purposes only.  
