cd /home/ubuntu/dapps-scraping
##python3 stateDapps.py 1
#date >> daily.log
#xvfb-run -a -s "-screen 0 1200x900x16" python3 DappRadar.py 1 >> daily.log
#python3 -u DappRadar.py 1 | tee daily.log
xvfb-run -a -s "-screen 0 1200x900x16" python3 -u DappRadar.py 1 2>&1 | tee -a daily.log

# for safety
#kill `pidof chromedriver` 2>/dev/null
#kill -9 `pidof google-chrome chrome` 2>/dev/null
