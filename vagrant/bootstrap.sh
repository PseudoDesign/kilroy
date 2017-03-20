#!/usr/bin/env bash

sudo add-apt-repository -y ppa:fkrull/deadsnakes
apt-get update
apt-get install -y python3.5 python3-pip git
python3.5 -m pip install discord.py pyyaml
