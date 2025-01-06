#!/bin/bash
sudo echo "root:123" | sudo chpasswd

sudo apt-get update -y && sudo apt-get upgrade -y

sudo rm -rf /etc/ssh/sshd_config.d/50-cloud-init.conf

sudo cat > '/etc/ssh/sshd_config.d/99-custom.conf' <<EOF
PasswordAuthentication yes
PermitRootLogin yes
EOF

sudo cat /home/vagrant/id_ed25519.pub > '/root/.ssh/authorized_keys'
sudo mv /home/vagrant/cert.pem /root/cert.pem
sudo mv /home/vagrant/key.pem /root/key.pem

sudo systemctl restart ssh.service

sudo apt-get install sshpass -y

openssl req -x509 -newkey rsa:2048 -keyout /root/key.pem -out /root/cert.pem -days 365 -nodes -subj "/C=VN/ST=TPHCM/L=ThuDuc/O=FPT/OU=FTELHCM/CN=stg.fpt.net"

curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh ./get-docker.sh