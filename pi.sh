#!/bin/bash

sudo wget https://lancelot.netknights.it/NetKnights-Release.asc

sudo gpg --import --import-options show-only --with-fingerprint NetKnights-Release.asc

sudo mv NetKnights-Release.asc /etc/apt/trusted.gpg.d/
sudo add-apt-repository http://lancelot.netknights.it/community/noble/stable

sudo apt-get update -y

sudo apt install privacyidea-apache2 -y

sudo apt install expect -y

sudo cat > '/root/pisetup.sh' <<EOF
#!/usr/bin/expect -f
set timeout 10
set password "123"
set account "admin@localhost"
spawn sudo pi-manage admin add admin -e $account
expect "Password:"
send "$password\r"
expect "Repeat for confirmation:"
send "$password\r"
expect eof
EOF

sudo chmod +x /root/pisetup.sh
sudo ./root/pisetup.sh

