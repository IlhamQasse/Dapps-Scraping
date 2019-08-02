uname -a | grep -q Linux

if [ $? = 0 ]
then
  src=https://chromedriver.storage.googleapis.com/76.0.3809.68/chromedriver_linux64.zip
else
  src=https://chromedriver.storage.googleapis.com/76.0.3809.68/chromedriver_mac64.zip
fi

if [ ! -x chromedriver ]
then
  echo "Downloading."
  wget $src -O chromedriver.zip
  unzip chromedriver.zip
  rm -f chromedriver.zip
else
  echo "Already downloaded."
fi
