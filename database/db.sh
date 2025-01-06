#!/bin/bash

sudo mv /home/vagrant/database /root/database

sudo apt install mysql-server -y

sudo sed -i "s/^bind-address\s*=.*$/bind-address = 0.0.0.0/" /etc/mysql/mysql.conf.d/mysqld.cnf
sudo systemctl restart mysql.service

sudo mysql -e "CREATE USER 'luongnv'@'10.128.0.1' IDENTIFIED BY '123';"
sudo mysql -e "GRANT ALL PRIVILEGES ON *.* TO 'luongnv'@'10.128.0.1' WITH GRANT OPTION;"
sudo mysql -e "FLUSH PRIVILEGES;"

sudo mysql -e "CREATE USER 'luongnv'@'10.128.0.20' IDENTIFIED BY '123';"
sudo mysql -e "GRANT ALL PRIVILEGES ON *.* TO 'luongnv'@'10.128.0.20' WITH GRANT OPTION;"
sudo mysql -e "FLUSH PRIVILEGES;"

sudo mysql -e "CREATE USER 'luongnv'@'10.128.0.23' IDENTIFIED BY '123';"
sudo mysql -e "GRANT ALL PRIVILEGES ON *.* TO 'luongnv'@'10.128.0.23' WITH GRANT OPTION;"
sudo mysql -e "FLUSH PRIVILEGES;"

sudo mysql -u root < /root/database/mydatabase.sql