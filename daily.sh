cd /home/ubuntu/dapps-scraping
#python3 stateDapps.py 1
date >> daily.log
xvfb-run -a -s "-screen 0 1200x900x16" python3 DappRadar.py 1 >> daily.log
