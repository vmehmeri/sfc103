#!/bin/bash

apt-get update -y
apt-get install git curl -y
curl -fsSL https://get.docker.com/ | sh
docker build -t spn /vagrant/spn 
