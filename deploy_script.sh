#!/bin/bash
apt update
apt install -y python3 python3-pip
pip3 install -r requirements.txt
export PUBLIC_IP=$(curl http://169.254.169.254/latest/meta-data/public-ipv4)
export PRIVATE_IP=$(curl http://169.254.169.254/latest/meta-data/local-ipv4)
export WEATHER_API_KEY=
python3 manage.py runserver $PRIVATE_IP:80 > /dev/null 2>&1
