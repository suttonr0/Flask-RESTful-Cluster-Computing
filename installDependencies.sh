#!/bin/bash

echo "Starting to install dependencies"
echo "May need to run with sudo"
echo "--------------------------"
echo "(installDependencies.sh) Installing Python 3"
apt-get install python3
echo "--------------------------"
echo "(installDependencies.sh) Installing pip for Python 3"
apt-get install python3-pip
echo "--------------------------"
echo "(installDependencies.sh) Installing dependencies with pip"
pip install -r requirements.txt  ## -r otherwise pip tries to install a package called "requriements.txt"
echo "--------------------------"
echo "(installDependencies.sh) End of script"
