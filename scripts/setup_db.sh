#!/bin/bash

set -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
DB_NAME='kilroy'

if [[ $EUID -ne 0 ]]; then
    echo "This script must be run as root"
    exit 1
fi

# Include the "parse_yaml" function
. ${DIR}/parse_yaml.sh

apt-get update

# Install python packages
python3.5 -m pip install sqlalchemy pyaml pymysql

# Install MariaDB (debian jessie)
sudo apt-get install software-properties-common
sudo apt-key adv --recv-keys --keyserver hkp://keyserver.ubuntu.com:80 0xcbcb082a1bb943db
sudo add-apt-repository 'deb [arch=amd64,i386,ppc64el] http://nyc2.mirrors.digitalocean.com/mariadb/repo/10.2/ubuntu trusty main'
apt-get update
apt-get install -y mariadb-server
# Generate/get our keys
python3.5 ${DIR}/../kilroy/keys.py
eval $(parse_yaml ${DIR}/../.keys.yaml "key_")
if [ -z "$key_sql_user" ]; then
    echo "Error: unable to get sql_user key"
    exit 1
fi
if [ -z "$key_sql_remote_user" ]; then
    echo "Error: unable to get the sql_remote_user key"
    exit 1
fi
# Initalize our db
echo "Enter your MariaDB root password: "
read -s PASSWORD
mysql -u root -p"${PASSWORD}" -e "CREATE DATABASE IF NOT EXISTS $DB_NAME"
mysql -u root -p"${PASSWORD}" -e "CREATE USER IF NOT EXISTS 'sql_user'@'localhost' IDENTIFIED BY '${key_sql_user}';"
mysql -u root -p"${PASSWORD}" -e "GRANT CREATE, INSERT, SELECT ON ${DB_NAME}.* TO 'sql_user'@'localhost' IDENTIFIED BY '${key_sql_user}';"


