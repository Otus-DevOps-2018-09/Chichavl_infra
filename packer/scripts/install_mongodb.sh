#!/bin/bash

# Add repo
apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv EA312927
bash -c 'echo "deb http://repo.mongodb.org/apt/ubuntu xenial/mongodb-org/3.2 multiverse" > /etc/apt/sources.list.d/mongodb-org-3.2.list'

# Install mongo package
apt update
apt install -y mongodb-org

# Start mongod and add it to system startup
systemctl start mongod
systemctl enable mongod
