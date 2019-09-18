uname -a | grep -q Linux

#version=76.0.3809.68
version=77.0.3865.40

if [ $? = 0 ]
then
  src=https://chromedriver.storage.googleapis.com/$version/chromedriver_linux64.zip
else
  src=https://chromedriver.storage.googleapis.com/$version/chromedriver_mac64.zip
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
