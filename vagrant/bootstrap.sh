#!/usr/bin/env bash

sudo apt-get update
sudo apt-get upgrade
apt-get install -y python3-pip git
sudo add-apt-repository -y ppa:fkrull/deadsnakes
apt-get update
sudo apt-get install -y python3.5
python3.5 -m pip install discord.py pyyaml squalchemy
