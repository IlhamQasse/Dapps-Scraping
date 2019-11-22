# build »»» docker build -t dappsscraper .
# run   »»» docker run -ti dappsscraper

# workarounds:
# PYTHONPATH=/usr/lib/python3/dist-packages/ python3 DappRadar.py 1
# mkdir -p /opt/google/chrome/; ln -s /usr/bin/chromium /opt/google/chrome/google-chrome
# apt-get install libtk8.6

FROM python:3.7-slim

COPY download.sh DappRadar.py /
#COPY requirements.txt /

RUN apt-get update && apt-get install -y --no-install-recommends chromium chromium-sandbox xvfb xauth python3-lxml python3-pandas python3-matplotlib python3-selenium python3-openpyxl wget unzip
#RUN pip3 install -r requirements.txt
RUN /download.sh

CMD ["/bin/bash"]
