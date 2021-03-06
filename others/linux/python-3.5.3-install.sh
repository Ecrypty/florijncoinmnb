#!/bin/sh
# from http://wyre-it.co.uk/blog/latestpython/
RELEASE=3.5.3
 
# install dependencies
sudo apt-get -y install git libbz2-dev liblzma-dev libsqlite3-dev libncurses5-dev libgdbm-dev zlib1g-dev libreadline-dev libssl-dev tk-dev
sudo apt-get -y install libudev-dev libusb-1.0-0-dev libfox-1.6-dev
sudo apt-get -y install autotools-dev autoconf automake libtool

# download and build Python
mkdir ~/python3
cd ~/python3
wget https://www.python.org/ftp/python/$RELEASE/Python-$RELEASE.tar.xz
tar xvf Python-$RELEASE.tar.xz
cd Python-$RELEASE
./configure
make

# this will install
# /usr/local/bin/python3.5
# /usr/local/bin/pip3.5
sudo make altinstall
sudo pip3.5 install virtualenv

# do below when install florijncoinmnb
# virtualenv -p python3.5 venv3
