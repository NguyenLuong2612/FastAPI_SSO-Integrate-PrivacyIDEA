#!/bin/bash

sudo mv /home/vagrant/backend /root/backend

sudo mv /home/vagrant/cert.pem /root/backend/cert.pem
sudo mv /home/vagrant/key.pem /root/backend/key.pem

sudo touch /root/backend/.env

sudo apt install python3.12 python3.12-venv python3-pip python-is-python3 -y

python3 -m venv /root/backend/env
source /root/backend/env/bin/activate
pip install -r /root/backend/requirements.txt

python3 -u /root/backend/handle.py
