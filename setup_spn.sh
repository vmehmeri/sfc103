#!/bin/bash

apt-get update -y
apt-get install git curl -y
curl -fsSL https://get.docker.com/ | sh
docker build -t spn /vagrant/spn 
docker run -d --name von1 spn tail -f /dev/null
docker run -d --name von2 spn tail -f /dev/null