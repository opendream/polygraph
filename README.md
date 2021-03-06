# Install mysql and create database
# username password dbname config in polygraph/settings.py or create polygraph/settings_local.py override
mysql -u root -e "CREATE DATABASE polygraph DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci";

apt-get install redis-server supervisor


apt-get install xvfb xserver-xephyr
# For OSX install XQuartz http://xquartz.macosforge.org/landing/

# If no firefox found, add this line to your /etc/apt/sources.list file
# deb http://packages.linuxmint.com debian import
apt-get install firefox

apt-get install xfonts-thai # append package for project language

# cp polygraph/supervisor.conf /etc/supervisor/conf.d/polygraph.conf 

mkdir -p /web/polygraph/lib/python2.7/dist-packages/

pip install -r requirements.txt
python manage.py syncdb
python manage.py migrate account
python manage.py migrate domain
python manage.py initial

# optional
python manage.py makesample

# import cv2

pip install numpy

## Mac
brew tap homebrew/science
brew install opencv

## Linux
apt-get install cmake libopencv-dev python-opencv


## localhost (virtualenv wrapper)
ln -s /usr/local/lib/python2.7/site-packages/cv2.so /usr/local/lib/python2.7/site-packages/cv.py ~/.virtualenvs/polygraph/lib/python2.7/site-packages

## production (virtualenv)
ln -s /usr/lib/pymodules/python2.7/cv2.so /usr/lib/pymodules/python2.7/cv.py /web/polygraph/lib/python2.7/site-packages
